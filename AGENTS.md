# MusicPal contributor instructions

MusicPal owns musical knowledge and device-independent algorithms. No imports
from DelugePal, device I/O, XML codecs or raw firmware encodings belong here.
Backend-specific conversion is explicit; do not silently discard note metadata.
Preserve sources, evidence scope and incomplete coverage. Historical snapshots
under skills/music-pal/provenance are immutable evidence, not instructions.
Never add private corpora, songs, presets, books or datasets. Keep new large
artifacts and Git worktrees on D:. Run `python -m unittest discover -s tests`.
