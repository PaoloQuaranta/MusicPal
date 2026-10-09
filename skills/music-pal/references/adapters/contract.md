# Backend-neutral interchange

MusicPal owns musical decisions and note events; each backend owns its device state,
transport and files. `musicpal.interchange` uses numeric MIDI pitches (0..127),
velocity (1..127) and lift (0..127). `BeatNote.onset` is zero-based and `duration`
is positive. Both are exact `fractions.Fraction` values in **quarter-note beats**,
regardless of meter. Rests are gaps; chords share an onset. Pickups before zero
are outside this minimal contract.

`MusicalPattern(notes, ppq, meter=(4,4), intent='', role='')` retains explicit PPQ,
meter and optional text describing musical intent/part role. Meter denominators
must be powers of two. A 6/8 bar contains 3 internal quarter beats. The musical
APIs retain a historical `tick_per_battuta` name whose meaning depends on the
operation:

| Operation | Meaning of `tick_per_battuta` |
|---|---|
| `durata_in_tick`, `melodia`, `linea`, `accordi`, `armonia`, the 16-step grid in `passi`, `applica_groove` | Four-quarter reference grid, `4 * ppq`, regardless of the actual meter |
| Density and reaction analysis (`reazione`, `_densita_per_battuta`) | Actual bar length in ticks for the material being counted |
| `comping` | A 4/4 bar with eight eighth-note slots; non-4/4 comping is not implemented |

For note-value constructors at PPQ 96, pass 384 even in 3/4 or 6/8, and set
`meter=(6, 8)` on the interchange pattern. A 6/8 bar ends at 288 ticks, while
`durata='1/4'` must still last 96 ticks. Passing 288 to `melodia` as
`tick_per_battuta` would shorten note values incorrectly; passing 288 to density
analysis instead is correct for a 6/8 bar. Arrange actual bar boundaries separately.
For comping outside 4/4 use explicitly timed chord events; do not relabel a
4/4 result as a different meter.

```python
from musicpal.notes import Note
from musicpal.interchange import from_tick_notes, to_tick_notes
pattern = from_tick_notes({60: [Note(32, 64, 90)]}, ppq=96,
                          meter=(4, 4), role='melody')
assert str(pattern.notes[0].onset) == '1/3'
assert to_tick_notes(pattern)[60][0].pos == 32
```

`to_dict()` produces JSON-safe rational strings such as `"1/3"`; `from_dict()`
restores them exactly. No float timing is emitted. Float inputs are interpreted
via decimal text, so pass Fraction for tuplets. `to_tick_notes` rejects timings
that are not integral at the requested PPQ; choose a finer PPQ or deliberately
quantize before conversion. Conversion never silently rounds.

Tick imports accept exactly the neutral `musicpal.notes.Note` model with its four
fields; extra attributes, subclasses and arbitrary backend objects are rejected.
Backend state has no universal musical meaning. Tick imports reject the presence of
backend probability/condition, iterance and fill fields, including default values; neutral JSON
imports reject unknown note fields. Convert legacy objects with their backend semantic adapter (DelugePal exposes
`delugexml.music_bridge.to_musical`) before interchange. Keep conditional originals
in their backend or explicitly realize them as deterministic note events.
No raw device condition bytes belong to this contract.
