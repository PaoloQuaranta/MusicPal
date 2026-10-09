"""Explicit ticks per quarter-note (PPQ); 96 is a configurable default."""
from fractions import Fraction

DEFAULT_PPQ = 96

def convert_ticks(value: int, source_ppq: int, target_ppq: int) -> int:
    """Rescale ticks, rounding half to even; use Fraction for exact beat times.

    A 4/4 bar contains four quarter notes, hence four times PPQ ticks.
    MIDI converters separately report rounding and clamp note length to one.
    """
    if any(isinstance(p, bool) or not isinstance(p, int) or p <= 0
           for p in (source_ppq, target_ppq)):
        raise ValueError('PPQ must be positive integers')
    return round(Fraction(value) * target_ppq / source_ppq)
