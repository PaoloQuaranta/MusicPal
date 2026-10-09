"""Exact, backend-neutral pitched events. One beat always means a quarter note."""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from typing import Mapping, Iterable


def _integer(value, name, minimum, maximum=None):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum or (maximum is not None and value > maximum):
        raise ValueError(f"{name} must be an integer in {minimum}..{maximum or 'unbounded'}")
    return value


def _fraction(value):
    if isinstance(value, bool):
        raise ValueError("beat values must be numeric, not boolean")
    # Decimal text avoids manufacturing a binary float's approximation.
    return Fraction(str(value)) if isinstance(value, float) else Fraction(value)


@dataclass(frozen=True)
class BeatNote:
    pitch: int
    onset: Fraction
    duration: Fraction
    velocity: int = 64
    lift: int = 64

    def __post_init__(self):
        _integer(self.pitch, "pitch", 0, 127)
        _integer(self.velocity, "velocity", 1, 127)
        _integer(self.lift, "lift", 0, 127)
        object.__setattr__(self, "onset", _fraction(self.onset))
        object.__setattr__(self, "duration", _fraction(self.duration))
        if self.onset < 0 or self.duration <= 0:
            raise ValueError("onset must be nonnegative and duration positive")


@dataclass(frozen=True)
class MusicalPattern:
    notes: tuple[BeatNote, ...]
    ppq: int
    meter: tuple[int, int] = (4, 4)
    intent: str = ""
    role: str = ""

    def __post_init__(self):
        _integer(self.ppq, "ppq", 1)
        object.__setattr__(self, "notes", tuple(self.notes))
        object.__setattr__(self, "meter", tuple(self.meter))
        if len(self.meter) != 2:
            raise ValueError("meter must contain numerator and denominator")
        numerator, denominator = self.meter
        _integer(numerator, "meter numerator", 1)
        _integer(denominator, "meter denominator", 1)
        if denominator & (denominator - 1):
            raise ValueError("meter denominator must be a power of two")
        if not all(isinstance(note, BeatNote) for note in self.notes):
            raise TypeError("notes must contain BeatNote instances")
        if not isinstance(self.intent, str) or not isinstance(self.role, str):
            raise TypeError("intent and role must be text")

    @property
    def beats_per_bar(self):
        return Fraction(4 * self.meter[0], self.meter[1])

    def to_dict(self):
        """JSON-safe exact rationals as strings (for example '1/3')."""
        return {"ppq": self.ppq, "meter": list(self.meter), "intent": self.intent,
                "role": self.role, "notes": [
                    {"pitch": n.pitch, "onset": str(n.onset), "duration": str(n.duration),
                     "velocity": n.velocity, "lift": n.lift} for n in self.notes]}

    @classmethod
    def from_dict(cls, data):
        allowed = {"ppq", "meter", "intent", "role", "notes"}
        if set(data) - allowed:
            raise ValueError("unknown pattern fields must be handled by an adapter")
        notes = []
        for item in data["notes"]:
            if set(item) - {"pitch", "onset", "duration", "velocity", "lift"}:
                raise ValueError("unknown note state must be handled by an adapter")
            notes.append(BeatNote(**item))
        return cls(tuple(notes), data["ppq"], tuple(data.get("meter", (4, 4))),
                   data.get("intent", ""), data.get("role", ""))


def _check_conditions(note):
    """Accept exactly the neutral model; never flatten arbitrary backend objects."""
    from .notes import Note
    backend_fields = ('condition', 'probability', 'iterance_divisor',
                      'iterance_steps', 'iterance', 'fill', 'fill_mode')
    if any(hasattr(note, field) for field in backend_fields):
        raise ValueError('backend note state requires an explicit semantic adapter')
    if type(note) is not Note:
        raise TypeError('expected an exact musicpal.notes.Note; adapt backend objects first')
    extra = set(vars(note)) - {'pos', 'length', 'velocity', 'lift'}
    if extra:
        raise ValueError(f'unsupported note metadata: {sorted(extra)}')


def from_tick_notes(rows: Mapping[int, Iterable], *, ppq: int,
                    meter=(4, 4), intent="", role="") -> MusicalPattern:
    """Convert pitch -> Note rows; PPQ is mandatory, never inferred from a bar."""
    _integer(ppq, "ppq", 1)
    events = []
    for pitch, row in rows.items():
        _integer(pitch, "pitch", 0, 127)
        for note in row:
            _check_conditions(note)
            _integer(note.pos, "pos", 0)
            _integer(note.length, "length", 1)
            events.append(BeatNote(pitch, Fraction(note.pos, ppq),
                                   Fraction(note.length, ppq), note.velocity, note.lift))
    events.sort(key=lambda n: (n.onset, n.pitch, n.duration, n.velocity))
    return MusicalPattern(tuple(events), ppq, meter, intent, role)


def to_tick_notes(pattern: MusicalPattern, *, ppq: int | None = None):
    """Return neutral Note rows. Reject unrepresentable timing rather than quantize."""
    from .notes import Note
    target = pattern.ppq if ppq is None else _integer(ppq, "ppq", 1)
    rows = {}
    for event in pattern.notes:
        pos, length = event.onset * target, event.duration * target
        if pos.denominator != 1 or length.denominator != 1:
            raise ValueError("timing is not integral at target PPQ; choose a finer PPQ")
        rows.setdefault(event.pitch, []).append(
            Note(int(pos), int(length), event.velocity, event.lift))
    for row in rows.values():
        row.sort(key=lambda note: note.pos)
    return rows
