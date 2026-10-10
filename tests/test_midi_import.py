"""Synthetic SMF fixtures: no installed MCP server, DAW or private material."""
import importlib.util
import json
import struct
import subprocess
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path


def vlq(value):
    result = [value & 127]
    while value >> 7:
        value >>= 7
        result.insert(0, (value & 127) | 128)
    return bytes(result)


def event(delta, data):
    return vlq(delta) + data


def smf(*tracks, ppq=480, fmt=None):
    header = b'MThd' + struct.pack('>IHHH', 6, int(len(tracks) > 1) if fmt is None else fmt,
                                  len(tracks), ppq)
    return header + b''.join(b'MTrk' + struct.pack('>I', len(t)) + t for t in tracks)


END = b'\xff\x2f\x00'
NOTE = event(0, b'\x90\x3c\x64') + event(160, b'\x80\x3c\x25')


class MidiImportTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(importlib.util.find_spec('musicpal.midi_import'),
                             'The loss-aware MIDI import bridge is missing')
        from musicpal.midi_import import read_bytes
        self.read = read_bytes

    def test_exact_notes_release_velocity_channels_and_tail(self):
        conductor = event(0, b'\xff\x51\x03\x07\xa1\x20') + event(0, b'\xff\x58\x04\x06\x03\x18\x08') + event(1440, END)
        part = event(0, b'\xff\x03\x04Lead') + NOTE + event(0, b'\x99\x24\x50') + event(80, b'\x99\x24\x00') + event(240, END)
        song = self.read(smf(conductor, part))
        self.assertEqual(song.length_beats, 3)
        self.assertEqual(song.tracks[1].end_tick, 480)
        parts = song.patterns()
        self.assertEqual([(p.track_index, p.name, p.channel, p.length_beats) for p in parts],
                         [(1, 'Lead', 0, 3), (1, 'Lead', 9, 3)])
        note = parts[0].pattern.notes[0]
        self.assertEqual((note.pitch, note.onset, note.duration, note.velocity, note.lift),
                         (60, 0, Fraction(1, 3), 100, 37))
        self.assertEqual(parts[1].pattern.notes[0].lift, 64)
        self.assertEqual(parts[0].pattern.meter, (6, 8))
        manifest = json.loads(json.dumps(song.to_dict()))
        self.assertEqual(manifest['tracks'][1]['notes'][0]['duration'], '1/3')
        self.assertEqual(manifest['tracks'][0]['events'][0]['data_hex'], '07a120')

    def test_program_changes_require_explicit_omission(self):
        song = self.read(smf(event(0, b'\xc0\x20') + NOTE + event(0, END)))
        with self.assertRaisesRegex(ValueError, 'program_change'):
            song.patterns()
        self.assertEqual(len(song.patterns(omit_events={'program_change'})), 1)
        self.assertEqual(song.tracks[0].events[0].data, b'\x20')

    def test_controls_and_unknown_metadata_are_retained_and_guarded(self):
        for message, kind in [(b'\xb0\x40\x7f', 'control_change'),
                              (b'\xe0\x00\x50', 'pitch_bend'),
                              (b'\xa0\x3c\x20', 'poly_pressure'),
                              (b'\xd0\x20', 'channel_pressure'),
                              (b'\xf0\x02\x01\xf7', 'sysex'),
                              (b'\xff\x59\x02\x00\x00', 'meta_59')]:
            with self.subTest(kind=kind):
                song = self.read(smf(event(0, message) + NOTE + event(0, END)))
                with self.assertRaisesRegex(ValueError, kind):
                    song.patterns()
                self.assertTrue(song.patterns(omit_events={kind}))

    def test_tempo_and_meter_changes_are_not_flattened(self):
        for change in [b'\xff\x51\x03\x06\x1a\x80', b'\xff\x58\x04\x03\x02\x18\x08']:
            song = self.read(smf(NOTE + event(10, change) + event(0, END)))
            self.assertTrue(song.tracks[0].events)
            with self.assertRaisesRegex(ValueError, 'map'):
                song.patterns()

    def test_explicit_length_extends_silence_but_never_truncates(self):
        data = smf(NOTE + event(320, END))
        song = self.read(data, length_beats='128')
        self.assertEqual(song.patterns()[0].length_beats, 128)
        self.assertEqual(song.tracks[0].end_tick, 480)
        with self.assertRaisesRegex(ValueError, 'length'):
            self.read(data, length_beats=Fraction(1, 2))

    def test_running_status_and_implicit_release(self):
        track = event(0, b'\x90\x3c\x64') + event(240, b'\x3c\x00') + event(0, END)
        note = self.read(smf(track)).patterns()[0].pattern.notes[0]
        self.assertEqual((note.duration, note.lift), (Fraction(1, 2), 64))

    def test_malformed_or_ambiguous_notes_are_rejected(self):
        tracks = [event(0, b'\x90\x3c\x64') + event(480, END),
                  event(0, b'\x80\x3c\x00') + event(0, END),
                  event(0, b'\x90\x3c\x64') + event(0, b'\x80\x3c\x00') + event(0, END),
                  event(0, b'\x90\x3c\x64') + event(20, b'\x90\x3c\x50') + event(480, END),
                  NOTE, NOTE + event(0, END) + event(0, END),
                  b'\x00\x90\x3c', b'\x81', b'\x00\xff\x03\x05abc',
                  b'\x00\xf0\x03a', b'\x00\xf2\x00\x00',
                  b'\x00\x90\x80\x01', b'\x00\xff\x51\x03\x00\x00\x00']
        for track in tracks:
            with self.subTest(track=track), self.assertRaises(ValueError):
                self.read(smf(track))

    def test_bad_container_or_unsupported_timebase_is_rejected(self):
        good = smf(NOTE + event(0, END))
        for data in [good[:-1], good + b'x', good[:10],
                     smf(NOTE + event(0, END), ppq=0),
                     smf(NOTE + event(0, END), ppq=0xe728),
                     smf(NOTE + event(0, END), fmt=2),
                     good[:10] + b'\x00\x02' + good[12:],
                     good + b'JUNK\x00\x00\x00\x00']:
            with self.subTest(data=data), self.assertRaises(ValueError):
                self.read(data)

    def test_producer_pal_requires_explicit_release_policy(self):
        from musicpal.producer_pal import render_notes
        pattern = self.read(smf(NOTE + event(0, END))).patterns()[0].pattern
        with self.assertRaises(ValueError):
            render_notes(pattern)
        output = render_notes(pattern, discard_lift=True)
        self.assertIn('v100', output)
        self.assertIn('C3', output)

    def test_defaults_empty_tracks_and_omission_typos(self):
        song = self.read(smf(event(1920, END), NOTE + event(0, END)))
        self.assertEqual(song.tempo_us_per_quarter, 500000)
        self.assertEqual(song.meter, (4, 4))
        self.assertEqual(len(song.tracks), 2)
        self.assertEqual(len(song.patterns()), 1)
        self.assertEqual(song.patterns()[0].length_beats, 4)
        for omission in [{'program_changes'}, {'tempo'}, 'control_change']:
            with self.subTest(omission=omission), self.assertRaises(ValueError):
                song.patterns(omit_events=omission)

    def test_cli_manifest_and_refusal_to_overwrite_source(self):
        root = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory(dir=root) as folder:
            source, output = Path(folder) / 'idea.mid', Path(folder) / 'audit.json'
            original = smf(NOTE + event(0, END))
            source.write_bytes(original)
            result = subprocess.run([sys.executable, '-m', 'musicpal.midi_import', str(source),
                                     '--length-beats', '4', '--output', str(output)],
                                    cwd=root, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = json.loads(output.read_text(encoding='utf-8'))
            self.assertEqual(manifest['length_beats'], '4')
            self.assertEqual(manifest['tracks'][0]['notes'][0]['velocity'], 100)
            result = subprocess.run([sys.executable, '-m', 'musicpal.midi_import', str(source),
                                     '--output', str(source)], cwd=root, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(source.read_bytes(), original)


if __name__ == '__main__':
    unittest.main()
