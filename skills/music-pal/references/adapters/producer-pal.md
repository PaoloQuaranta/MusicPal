# Producer Pal adapter (offline)

Official references checked 2026-10-09:
[notation](https://producer-pal.org/features/midi-notation),
[tool reference](https://producer-pal.org/features/tools).
Producer Pal remains a separately installed Ableton integration. MusicPal does
not install it, connect to Live, or submit tool calls.

For material generated with MIDI Composer, first follow the
[MIDI import workflow](midi-composer.md). It retains track/channel identity,
clip length and non-note events outside the pattern, and requires an explicit
policy for programs, release velocity and other state before this serializer.

```python
from musicpal.notes import Note
from musicpal.interchange import from_tick_notes
from musicpal.producer_pal import render_notes
pattern = from_tick_notes({60: [Note(0, 96, 100)],
                           64: [Note(0, 96, 100)],
                           67: [Note(0, 96, 100)]}, ppq=96)
print(render_notes(pattern))
```

This yields three simultaneous pitches, spelled with Ableton's octave convention
(MIDI 60 is C3). Keep numeric pitch unchanged: a MusicPal bass range of MIDI
24–36 (do1–do2) is C0–C1 here, not C1–C2. See the
[pitch convention](../navigation.md#registri-e-nomi-delle-note).
The serializer emits verified `bar|beat` notation. Each event
restates its velocity, absolute note-value duration and unconditional probability
to avoid leaked prefix state. Internal quarter beats become meter-relative
positions; in 6/8, quarter beat 3 becomes bar 2 beat 1. Fractional positions use
note-value offsets and duration fractions preserve tuplets.

Lift has no documented mapping. A nondefault lift raises an error; explicitly
set `discard_lift=True` only after deciding that omission is acceptable. Identical
pitch+onset events raise an error because the backend's merge would overwrite one.
Intent, role and meter remain in the pattern; the notes string alone cannot
set clip metadata or express trailing silence/loop length. Set those separately
using the actual discovered schema. Empty output describes no new note events;
it is not an instruction to clear an existing clip.

For an explicitly requested future Live action:

1. Discover the installed tools and call `ppal-connect` first. Read the current
   returned skills, notation conventions, connection status and tool schemas.
2. Confirm that `bar|beat` is active (or explicitly arrange that notation using
   the installed integration's documented setting). Never feed this string to a
   client currently configured for MIDI JSON or Stark.
3. Read current tracks/clips and use returned IDs or paths. Documentation example
   IDs are illustrative, never real destinations. Establish actual clip meter,
   length, target and intended edit scope before preparing the write.
4. Prepare the current `ppal-create-clip` or `ppal-update-clip` call only from its
   discovered schema. Update merges by pitch+start; deleting, moving and replacing
   a region require the backend's documented editing mechanism. Do not mistake a
   whole new note list for replacement semantics.
5. Apply only the musical edit the user requested and read back the result.
6. Use the [final verification](../verifica-finale.md) to compare intent and
   implementation, including any planned filter automation or sidechain.
   Track/clip readback and transport state are technical checks; explicitly
   report whether the resulting audio was actually heard.

The module supports no transport/version-specific call wrapper and no MIDI JSON
or Stark serializer; use current Producer Pal skills for those notations.
