import json
import unittest
from fractions import Fraction
from types import SimpleNamespace

from musicpal.notes import Note
from musicpal.interchange import BeatNote, MusicalPattern, from_tick_notes, to_tick_notes
from musicpal.producer_pal import render_notes


class InterchangeTests(unittest.TestCase):
    def test_exact_tick_and_json_roundtrip(self):
        rows = {60: [Note(32, 64, 91, 52)], 67: [Note(32, 32, 75)]}
        pattern = from_tick_notes(rows, ppq=96, intent="triplet pickup", role="melody")
        self.assertEqual(pattern.notes[0].onset, Fraction(1, 3))
        self.assertEqual(pattern.notes[0].duration, Fraction(2, 3))
        restored = MusicalPattern.from_dict(json.loads(json.dumps(pattern.to_dict())))
        self.assertEqual(pattern, restored)
        self.assertEqual(to_tick_notes(restored), rows)
        self.assertEqual(to_tick_notes(restored, ppq=192)[60][0].pos, 64)

    def test_chord_rest_and_boundary(self):
        pattern = from_tick_notes({60: [Note(0, 96), Note(384, 24)],
                                   64: [Note(0, 96)], 67: [Note(0, 96)]}, ppq=96)
        lines = render_notes(pattern).splitlines()
        self.assertEqual(lines[:3], ["v64 n/4 p1 C3 1|1", "v64 n/4 p1 E3 1|1", "v64 n/4 p1 G3 1|1"])
        self.assertEqual(lines[3], "v64 n/16 p1 C3 2|1")
        self.assertEqual(len(lines), 4)  # The rest is an absence, not a note.

    def test_six_eight_positions_and_duration(self):
        pattern = from_tick_notes({60: [Note(240, 96), Note(288, 96), Note(320, 32)]}, ppq=96, meter=(6, 8))
        self.assertEqual(render_notes(pattern).splitlines(), [
            "v64 n/4 p1 C3 1|6", "v64 n/4 p1 C3 2|1",
            "v64 n/12 p1 C3 2|1+n/12"])
        self.assertEqual(pattern.beats_per_bar, 3)

    def test_three_four_boundary(self):
        pattern = from_tick_notes({61: [Note(288, 144)]}, ppq=96, meter=(3, 4))
        self.assertEqual(render_notes(pattern), "v64 n3/8 p1 Db3 2|1")

    def test_reject_conditional_legacy_note(self):
        defaults = dict(pos=0, length=24, velocity=64, lift=64,
                        condition=20, probability=100, iterance_divisor=0,
                        iterance_steps=0, iterance=None, fill=0, fill_mode="off")
        with self.assertRaisesRegex(ValueError, "backend"):
            from_tick_notes({60: [SimpleNamespace(**defaults)]}, ppq=96)
        for field, value in (("condition", 5), ("probability", 25),
                             ("iterance_divisor", 4), ("iterance_steps", 8),
                             ("iterance", "4of4"), ("fill", 2), ("fill_mode", "fill")):
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "backend"):
                from_tick_notes({60: [SimpleNamespace(**(defaults | {field: value}))]}, ppq=96)

    def test_tick_import_never_drops_extra_metadata(self):
        note = Note(0, 96)
        note.pressure = 77
        with self.assertRaisesRegex(ValueError, 'metadata'):
            from_tick_notes({60: [note]}, ppq=96)
        generic = SimpleNamespace(pos=0, length=96, velocity=64, lift=64, channel=2)
        with self.assertRaises(TypeError):
            from_tick_notes({60: [generic]}, ppq=96)
        class ExpressiveNote(Note):
            pressure = 77
        with self.assertRaises(TypeError):
            from_tick_notes({60: [ExpressiveNote(0, 96)]}, ppq=96)

    def test_reject_unknown_state_and_invalid_values(self):
        data = MusicalPattern((), 96).to_dict()
        data["notes"] = [dict(pitch=60, onset="0", duration="1", condition=5)]
        with self.assertRaisesRegex(ValueError, "unknown note"):
            MusicalPattern.from_dict(data)
        for ppq in (0, -1, True, 96.0):
            with self.subTest(ppq=ppq), self.assertRaises(ValueError):
                from_tick_notes({}, ppq=ppq)
        for kwargs in (dict(pitch=128), dict(velocity=0), dict(onset=-1), dict(duration=0)):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                BeatNote(**(dict(pitch=60, onset=0, duration=1) | kwargs))
        with self.assertRaises(ValueError):
            MusicalPattern((), 96, (3, 3))

    def test_finer_ppq_required_for_triplets(self):
        pattern = MusicalPattern((BeatNote(60, Fraction(1, 3), Fraction(1, 3)),), 96)
        with self.assertRaisesRegex(ValueError, "integral"):
            to_tick_notes(pattern, ppq=100)

    def test_lift_and_merge_collisions_are_explicit(self):
        pattern = MusicalPattern((BeatNote(60, 0, 1, lift=52),), 96)
        with self.assertRaisesRegex(ValueError, "lift"):
            render_notes(pattern)
        self.assertEqual(render_notes(pattern, discard_lift=True), "v64 n/4 p1 C3 1|1")
        with self.assertRaisesRegex(ValueError, "duplicate"):
            render_notes(MusicalPattern((BeatNote(60, 0, 1), BeatNote(60, 0, 2)), 96))
        with self.assertRaisesRegex(ValueError, "verified"):
            render_notes(pattern, notation="stark")

    def test_empty_pattern(self):
        self.assertEqual(render_notes(MusicalPattern((), 96)), "")
        self.assertEqual(to_tick_notes(MusicalPattern((), 96)), {})


if __name__ == "__main__":
    unittest.main()
