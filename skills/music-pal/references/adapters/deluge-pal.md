# DelugePal adapter boundary

Use MusicPal for theory, groove, composition and neutral events. Use the separate
DelugePal repository/skill for Synthstrom Deluge XML, SD layout, sample paths,
preset lookup, song structure, hardware audition and conditional note encoding.
MusicPal imports no `delugexml` modules and knows no SD-card path.

A musical pattern can be handed off as `pattern.to_dict()` with explicit PPQ and
meter, or as neutral `to_tick_notes(pattern, ppq=...)` rows. The DelugePal side
must map numeric pitches to the actual target's melodic note rows or chosen kit
rows, construct its own device Note objects, retain lift, and choose a destination
through its existing song/template validation workflow. Drum role labels do not
imply universal drum-row IDs. Ask the DelugePal skill for the current device and
song constraints when the user requests hardware output.

When importing existing Deluge events, first convert them with DelugePal's
`delugexml.music_bridge.to_musical` semantic adapter, then use
`from_tick_notes(rows, ppq=...)`. The neutral core rejects backend fields even
when they contain default values and never interprets raw device encodings.
Keep conditional state in the Deluge adapter or realize it explicitly into
a deterministic event list.
This interchange cannot preserve raw device blobs, locks or song structure.

Choosing a 384-tick bar assumes 4/4 at PPQ 96. A 6/8 bar at PPQ 96 is 288 ticks;
use the destination's actual PPQ. For legacy note-value constructors pass
`tick_per_battuta=4 * ppq` even in 6/8; density analysis instead needs actual bar
length. `comping` currently assumes 4/4. See the per-operation timing table in
[the contract](contract.md); do not apply one interpretation to every API. Neither
conversion nor exporting a neutral description writes to an SD card.
