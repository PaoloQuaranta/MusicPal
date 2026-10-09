"""Standalone musical composition and analysis, using only the standard library."""
from .notes import Note
from .timebase import DEFAULT_PPQ, convert_ticks
__all__ = ['Note', 'DEFAULT_PPQ', 'convert_ticks']
