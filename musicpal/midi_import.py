"""Strict SMF-to-interchange bridge, including MIDI Composer output.

The older ``midi.leggi`` API remains a permissive corpus reader. This path
shares its binary helpers but rejects repairs and retains non-note events.
It performs no MCP/device I/O and needs no third-party MIDI package.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
import hashlib
from pathlib import Path
import struct

from .interchange import BeatNote, MusicalPattern, _fraction
from .midi import _chunks, _vlq


@dataclass(frozen=True)
class MidiEvent:
    tick: int
    kind: str
    data: bytes
    channel: int | None = None


@dataclass(frozen=True)
class MidiNote:
    channel: int
    note: BeatNote


@dataclass(frozen=True)
class MidiTrack:
    index: int
    name: str | None
    end_tick: int
    notes: tuple[MidiNote, ...]
    events: tuple[MidiEvent, ...]


@dataclass(frozen=True)
class MidiPart:
    track_index: int
    name: str | None
    channel: int
    pattern: MusicalPattern
    length_beats: Fraction


@dataclass(frozen=True)
class MidiSong:
    format: int
    ppq: int
    tracks: tuple[MidiTrack, ...]
    length_beats: Fraction
    source_sha256: str

    def _constant(self, kind, default, decode):
        events = [e for t in self.tracks for e in t.events if e.kind == kind]
        values = {decode(e.data) for e in events}
        if not events or min(e.tick for e in events) > 0:
            values.add(default)
        if len(values) != 1:
            raise ValueError(f'{kind} map changes: handle the full MIDI map before pattern conversion')
        return values.pop()

    @property
    def tempo_us_per_quarter(self):
        """Constant tempo, or raise for a changing map. MIDI default: 500000."""
        return self._constant('tempo', 500000, lambda b: int.from_bytes(b, 'big'))

    @property
    def meter(self):
        """Constant meter, or raise for a changing map. MIDI default: 4/4."""
        return self._constant('meter', (4, 4), lambda b: (b[0], 1 << b[1]))

    def patterns(self, *, omit_events=()) -> tuple[MidiPart, ...]:
        """Split by original track AND channel; retain exact timing and lift.

        Inspect ``tracks[].events`` first. Non-note state cannot fit in a
        MusicalPattern; omission must name each event kind explicitly. The
        original events remain in this object even after an allowed omission.
        Tempo, clip length, track/channel routing are the caller's responsibility.
        Variable tempo/meter maps cannot be flattened with this method.
        """
        if isinstance(omit_events, str):
            raise ValueError('omit_events must be a collection of event kind names')
        allowed = {'tempo', 'meter', 'track_name', 'end_of_track'}
        omitted = set(omit_events)
        present = {e.kind for t in self.tracks for e in t.events}
        if omitted - (present - allowed):
            raise ValueError(f'unknown or protected omit_events: {sorted(omitted - (present - allowed))}')
        unsupported = present - allowed - omitted
        if unsupported:
            raise ValueError(f'non-note MIDI events require explicit handling or omit_events: {sorted(unsupported)}')
        self.tempo_us_per_quarter  # Validate the map, never quietly flatten it.
        meter = self.meter
        return tuple(
            MidiPart(t.index, t.name, channel,
                     MusicalPattern(tuple(n.note for n in t.notes if n.channel == channel),
                                    self.ppq, meter), self.length_beats)
            for t in self.tracks for channel in sorted({n.channel for n in t.notes}))

    def to_dict(self):
        """Audit manifest; exact quarter beats and all non-note payloads as hex."""
        return {
            'format': self.format, 'ppq': self.ppq, 'length_beats': str(self.length_beats),
            'source_sha256': self.source_sha256,
            'tracks': [
                {'index': t.index, 'name': t.name, 'end_tick': t.end_tick,
                 'notes': [{'channel': n.channel, 'pitch': n.note.pitch,
                            'onset': str(n.note.onset), 'duration': str(n.note.duration),
                            'velocity': n.note.velocity, 'lift': n.note.lift} for n in t.notes],
                 'events': [{'tick': e.tick, 'kind': e.kind, 'channel': e.channel,
                             'data_hex': e.data.hex()} for e in t.events]}
                for t in self.tracks]}


def _track(data, index, ppq):
    i = tick = 0
    running = None
    opened = {}
    notes, events = [], []
    name = None
    ended = False

    def take(size):
        nonlocal i
        if i + size > len(data):
            raise ValueError(f'track {index}: truncated event at byte {i}')
        result = data[i:i + size]
        i += size
        return result

    while i < len(data):
        delta, i = _vlq(data, i)
        tick += delta
        status = take(1)[0]
        if status < 128:
            if running is None:
                raise ValueError(f'track {index}: data without running status')
            i -= 1
            status = running
        if status == 0xff:
            running = None
            kind = take(1)[0]
            size, i = _vlq(data, i)
            payload = take(size)
            label = {3: 'track_name', 0x2f: 'end_of_track', 0x51: 'tempo', 0x58: 'meter'}.get(kind, f'meta_{kind:02x}')
            if kind == 3 and name is None:
                name = payload.decode('latin-1')
            if kind == 0x51 and (size != 3 or not int.from_bytes(payload, 'big')):
                raise ValueError(f'track {index}: invalid tempo')
            if kind == 0x58 and (size != 4 or not payload[0] or payload[1] > 7):
                raise ValueError(f'track {index}: unsupported or invalid meter')
            events.append(MidiEvent(tick, label, payload))
            if kind == 0x2f:
                if size or i != len(data):
                    raise ValueError(f'track {index}: invalid end-of-track or data after it')
                ended = True
                break
            continue
        if status in (0xf0, 0xf7):
            running = None
            size, i = _vlq(data, i)
            # Include F0/F7 to preserve the distinction between SysEx packets.
            events.append(MidiEvent(tick, 'sysex', bytes([status]) + take(size)))
            continue
        if not 0x80 <= status <= 0xef:
            raise ValueError(f'track {index}: unsupported status {status:#x}')
        running = status
        command, channel = status & 0xf0, status & 15
        payload = take(1 if command in (0xc0, 0xd0) else 2)
        if any(b >= 128 for b in payload):
            raise ValueError(f'track {index}: invalid channel event data')
        key = (channel, payload[0])
        if command == 0x90 and payload[1]:
            if key in opened:
                raise ValueError(f'track {index}: overlapping same-pitch notes on channel {channel}')
            opened[key] = (tick, payload[1])
        elif command in (0x80, 0x90):
            if key not in opened:
                raise ValueError(f'track {index}: note-off without note-on')
            start, velocity = opened.pop(key)
            if tick <= start:
                raise ValueError(f'track {index}: zero-length note')
            # Note-on velocity 0 is implicit note-off, with standard lift 64.
            lift = payload[1] if command == 0x80 else 64
            notes.append(MidiNote(channel, BeatNote(payload[0], Fraction(start, ppq),
                             Fraction(tick - start, ppq), velocity, lift)))
        else:
            label = {0xa0: 'poly_pressure', 0xb0: 'control_change', 0xc0: 'program_change',
                     0xd0: 'channel_pressure', 0xe0: 'pitch_bend'}[command]
            events.append(MidiEvent(tick, label, payload, channel))
    if not ended or opened:
        raise ValueError(f'track {index}: missing end-of-track or unclosed notes')
    notes.sort(key=lambda n: (n.note.onset, n.channel, n.note.pitch))
    return MidiTrack(index, name, tick, tuple(notes), tuple(events))


def read_bytes(data: bytes, *, length_beats=None) -> MidiSong:
    """Read format 0/1 PPQ MIDI. No rounding, note repair, or silent event loss.

    ``length_beats`` may extend the common clip length to retain intended final
    silence absent from a renderer's EOT. It cannot truncate any source track.
    Keep the original file: this manifest is semantic, not a byte-exact SMF codec.
    """
    chunks = list(_chunks(data))
    if not chunks or chunks[0][0] != b'MThd' or len(chunks[0][1]) != 6:
        raise ValueError('invalid MIDI header (expected six-byte MThd)')
    fmt, count, ppq = struct.unpack('>HHH', chunks[0][1])
    if fmt not in (0, 1) or not count or (fmt == 0 and count != 1):
        raise ValueError('only synchronous SMF format 0/1 is supported')
    if not 0 < ppq < 0x8000:
        raise ValueError('only positive PPQ timebases are supported, not SMPTE')
    if len(chunks) != count + 1 or any(kind != b'MTrk' for kind, _ in chunks[1:]):
        raise ValueError('track count mismatch or unsupported MIDI chunks')
    tracks = tuple(_track(body, i, ppq) for i, (_, body) in enumerate(chunks[1:]))
    actual = Fraction(max(t.end_tick for t in tracks), ppq)
    length = actual if length_beats is None else _fraction(length_beats)
    if length < actual or length < 0:
        raise ValueError('requested length would truncate source MIDI')
    return MidiSong(fmt, ppq, tracks, length, hashlib.sha256(data).hexdigest())


def read(path: str | Path, *, length_beats=None) -> MidiSong:
    """Read a local SMF, preserving a digest of the source for audit/revision."""
    return read_bytes(Path(path).read_bytes(), length_beats=length_beats)


def main():
    """Write an inspection manifest; never write to a DAW or change the MIDI."""
    import argparse
    import json

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('midi_file')
    parser.add_argument('--length-beats', help='Explicit common clip length in quarter beats')
    parser.add_argument('--output', type=Path, help='New JSON manifest (refuses overwrite)')
    args = parser.parse_args()
    try:
        result = json.dumps(read(args.midi_file, length_beats=args.length_beats).to_dict(), indent=2)
        if args.output:
            with args.output.open('x', encoding='utf-8') as output:
                output.write(result + '\n')
        else:
            print(result)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
