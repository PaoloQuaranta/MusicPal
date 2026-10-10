# MusicPal

Musical knowledge and Python tools, independent of a DAW or hardware device.
Extracted from [DelugePal](https://github.com/PaoloQuaranta/DelugePal), with
source provenance retained. Use the **music-pal** skill for musical decisions
and either Producer Pal (Ableton Live) or DelugePal to realize them.

The skill contains seven repertoire cards and 46 focused instructions, sources,
worked examples and explicit evidence limits. This is accumulated, partial
knowledge: classical, baroque and early-music repertoire coverage is not claimed
complete. Start at `skills/music-pal/SKILL.md`, then load only relevant references.

## Install

Python 3.10 or newer; no third-party runtime dependencies. From this checkout:

```powershell
python -m pip install -e .
python -m unittest discover -s tests
```

The build backend is setuptools. The skill itself is plain Markdown and can be
used without Python. Install it for Codex independently of any project:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/install_skill.ps1
```

On Windows the default is a junction: the skill remains on D: and the Codex
skills directory contains only the link. `-Destination <path>` supports other
skill locations; `-Mode Copy` makes a self-contained copy. Existing unrelated
skills are never overwritten. Reload skills/start a new chat if the client has
already cached its skill catalog. The repository folder can be installed as a
skill through `skills/music-pal`; the Python library is installed separately.

## Python example

```python
from musicpal import musica as MU
from musicpal.interchange import from_tick_notes
from musicpal.producer_pal import render_notes

notes = MU.armonia('Dm7 | G7 | Cmaj7', registro='do4',
                   durata='1/1', tick_per_battuta=384)
pattern = from_tick_notes(notes, ppq=96, meter=(4, 4),
                          intent='ii–V–I', role='accompaniment')
print(render_notes(pattern))
```

The internal tick resolution is explicit; 96 PPQ is a historical default,
not a hardware dependency. Interchange events use exact fractions of a quarter
note. For note-value constructors, legacy `tick_per_battuta` means `4 * ppq`, even
in 3/4 or 6/8; density analysis uses actual bar length and `comping` currently
assumes 4/4. See the [timing contract](skills/music-pal/references/adapters/contract.md). Numeric MIDI pitch is authoritative: middle C is 60, even when a backend
labels its octave differently. Conditional device notes must be converted
explicitly by their backend; unsupported state is not silently discarded.

The library includes pitch/rhythm/harmony, voice leading, comping, counterpoint,
dynamics and interaction analysis, plus MIDI, Groove MIDI, Weimar Jazz and Jazz
Transformer corpus readers. Datasets, third-party books, presets and private
songs are not distributed. Corpus paths must be provided explicitly.

## MIDI Composer

The skill can now use the separately installed MIDI Composer MCP tools to build
melodies, harmony, accompaniment and whole-song arrangements. MusicPal supplies
the musical decisions and checks the generated result before handing it to an
executor. Read the [workflow](skills/music-pal/references/adapters/midi-composer.md).
Neither the Python package nor the skill requires the MCP server to be available.

The MIDI reader inherited from DelugePal is already in `musicpal.midi`.
For generated material, `musicpal.midi_import` adds a strict import path into
the neutral interchange model, sharing the existing binary-reading helpers:

```python
from musicpal.midi_import import read
from musicpal.producer_pal import render_notes

song = read("idea.mid", length_beats=4)  # Explicit phrase length, including rests
print(song.to_dict())                  # Inspect every track and non-note event
# Example policy: GM programs are replaced by explicitly assigned DAW instruments.
for part in song.patterns(omit_events={"program_change"}):
    # Example policy: accept omission of release velocity in Producer Pal notation.
    print(part.track_index, part.channel, part.length_beats)
    print(render_notes(part.pattern, discard_lift=True))
```

Only list event kinds actually present and deliberately omitted. The import
preserves pitch, exact timing, attack/release velocity, channels, track ends and
all non-note payloads in an audit manifest. Pattern conversion rejects unhandled
CCs, programs, pitch bend and other unsupported state. Variable tempo/meter maps
remain available for inspection but cannot be flattened into these patterns.
Malformed notes are rejected rather than repaired. The legacy corpus-reading API
is retained. No external MIDI package, Deluge imports or device calls are added.

For a JSON audit without device access:

```powershell
python -m musicpal.midi_import idea.mid --length-beats 4 --output idea.audit.json
```

Keep the original MIDI and generation arguments. Set tempo, meter, clip length
and instruments separately in the executor; the note string does not set them.
An imported MIDI or an offline serialization test is not an audio listening test.

## Producer Pal / Ableton Live

Read [the bridge guide](skills/music-pal/references/adapters/producer-pal.md).
MusicPal creates musical material and can render Producer Pal notation offline.
Producer Pal itself supplies the connection and Live editing tools. Begin with
its actual connection handshake and current schemas; read track/clip IDs from
Live before using them. This extraction does not install Producer Pal or edit a
Live Set, and offline tests are not a live integration or listening test.

Official references: [Producer Pal guide](https://producer-pal.org/guide),
[MIDI notation](https://producer-pal.org/features/midi-notation),
[tool reference](https://producer-pal.org/features/tools).

## DelugePal

Install this checkout into DelugePal's Python environment:

```powershell
D:/DelugePal/.venv/Scripts/python.exe -m pip install -e D:/MusicPal
```

Use `music-pal` for musical choices and `deluge-pal` for the device. Legacy
`delugexml.musica`, `midi`, `groove`, `wjazz` and `jtd` calls delegate here.
Deluge XML, raw note conditions, presets, validation, automation and SysEx
remain in DelugePal. See [the adapter guide](skills/music-pal/references/adapters/deluge-pal.md).

## Provenance and license

GPL-3.0; see [LICENSE](LICENSE). Original authorship: Paolo Quaranta and
DelugePal contributors. Source baseline:
`cbf99ff305beed355f2a27fc83499665c8d102e3`.
The skill's `provenance/` directory preserves the original public knowledge
files and a migration manifest; these are immutable evidence, not active
instructions. The manifest's `neutral_sha256` values record the extraction
baseline; maintained references can evolve while retaining their source links.
Tests verify original snapshot hashes, source links and evidence coverage.
Source-specific licenses and attribution remain in the references.
The new repository contains no private corpus or inherited Git history.
