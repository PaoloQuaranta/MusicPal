"""Offline Producer Pal bar|beat note serializer; no network or Live mutations.

Syntax source: https://producer-pal.org/features/midi-notation
Do not submit this string until ppal-connect confirms the current notation/skills.
"""
from fractions import Fraction
from .interchange import MusicalPattern


_PITCH_CLASSES = ("C", "Db", "D", "Eb", "E", "F", "Gb", "G", "Ab", "A", "Bb", "B")


def _note_value(quarter_beats):
    whole = Fraction(quarter_beats) / 4
    numerator = "" if whole.numerator == 1 else str(whole.numerator)
    return f"n{numerator}/{whole.denominator}"


def _position(onset, meter):
    numerator, denominator = meter
    bar_length = Fraction(4 * numerator, denominator)
    bar = onset // bar_length
    within = onset - bar * bar_length
    meter_beat = Fraction(4, denominator)
    beat = within // meter_beat
    offset = within - beat * meter_beat
    suffix = "" if offset == 0 else "+" + _note_value(offset)
    return f"{bar + 1}|{beat + 1}{suffix}"


def render_notes(pattern: MusicalPattern, *, notation="bar-beat", discard_lift=False) -> str:
    """Render pitches, exact positions/durations and velocities in bar|beat.

    Meter beats follow the denominator (6/8: six eighths); internal beats are
    quarters. Every note resets velocity, duration and probability. Lift has
    no documented mapping: nondefault values require explicit discard_lift.
    Producer Pal merges at pitch+start, so ambiguous duplicates are rejected.
    """
    if notation not in ("bar-beat", "bar|beat"):
        raise ValueError("only verified bar|beat notation is supported")
    if not isinstance(discard_lift, bool):
        raise TypeError("discard_lift must be boolean")
    seen = set()
    lines = []
    for note in sorted(pattern.notes, key=lambda n: (n.onset, n.pitch)):
        identity = (note.pitch, note.onset)
        if identity in seen:
            raise ValueError("duplicate pitch+onset would be overwritten by Producer Pal")
        seen.add(identity)
        if note.lift != 64 and not discard_lift:
            raise ValueError("Producer Pal notation has no lift mapping; explicitly discard_lift")
        pitch = _PITCH_CLASSES[note.pitch % 12] + str(note.pitch // 12 - 2)
        lines.append(f"v{note.velocity} {_note_value(note.duration)} p1 {pitch} {_position(note.onset, pattern.meter)}")
    return "\n".join(lines)
