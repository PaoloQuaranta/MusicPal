"""Tests runnable from MusicPal with no DelugePal import or dataset."""
import dataclasses
import struct
import sys
import unittest

from musicpal import Note, DEFAULT_PPQ, convert_ticks
from musicpal import musica as MU, midi, groove, wjazz, jtd


class Core(unittest.TestCase):
    def test_import_is_standalone(self):
        self.assertFalse(any(name.startswith('delugexml') for name in sys.modules))
        self.assertEqual([f.name for f in dataclasses.fields(Note)],
                         ['pos', 'length', 'velocity', 'lift'])

    def test_pitch_chord_and_timebase(self):
        self.assertEqual(MU.altezza('do4'), 60)
        self.assertEqual(MU.altezza('Bb3'), 58)
        self.assertEqual(MU.sigla('Cm7').intervalli, (0, 3, 7, 10))
        self.assertEqual(convert_ticks(480, 480, DEFAULT_PPQ), 96)
        self.assertEqual(convert_ticks(1, 192, 96), 0)
        with self.assertRaises(ValueError):
            convert_ticks(2, 0, 96)

    def test_rhythm_and_note_mutability(self):
        notes = MU.passi('X.x.')
        self.assertEqual([(n.pos, n.velocity) for n in notes], [(0, 110), (48, 90)])
        first = notes[0]
        MU.applica_microtiming(notes, [2, -2])
        self.assertIs(notes[0], first)
        self.assertEqual([n.pos for n in notes], [2, 46])
        slow = MU.passi('X.x.', tick_per_battuta=192)
        self.assertEqual(slow[1].pos, 24)

    def test_density_and_interaction(self):
        a = [Note(0, 24), Note(192, 24)]
        b = [Note(96, 24), Note(288, 24)]
        self.assertEqual(MU._densita_per_battuta(a), [2])
        result = MU.interazione(a, b, celle=4)
        self.assertEqual(result.presenza, [1, 0, 1, 0])
        self.assertEqual(result.correlazione, -1)

    def test_midi_bytes_and_rounding(self):
        track = b'\x00\x90\x3c\x64\x60\x80\x3c\x00\x00\xff\x2f\x00'
        data = b'MThd'+struct.pack('>IHHH',6,0,1,96)+b'MTrk'+struct.pack('>I',len(track))+track
        parsed = midi.leggi_bytes(data)
        part, report = midi.melodia(parsed, tick_per_movimento=48)
        self.assertEqual(part[60][0], Note(0, 48, 100))
        self.assertTrue(report.esatta)
        _, report = midi._converti([midi.NotaMidi(1, 5, 60, 80, 0)], 480, 96)
        self.assertFalse(report.esatta)

    def test_groove_explicit_timebases_and_tuple_compatibility(self):
        profile = groove.profilo_da_colpi(
            {'kick': [(124, 100)]}, 480, origine_fissa=0,
            levare_fisso=.5, taglio='vicino')
        self.assertEqual(len(profile), 7)
        self.assertEqual(len(groove.Passo(1, 100, 4, 1)), 4)
        self.assertAlmostEqual(profile.passi['kick'][0].scarto, 4)
        notes = MU.passi('.x..')
        MU.applica_groove(notes, profile, 'kick', profile_ppq=480)
        self.assertEqual(notes[0].pos, 25)
        target = MU.passi('.x..', tick_per_battuta=1920)
        MU.applica_groove(target, profile, 'kick', profile_ppq=480,
                         tick_per_battuta=1920)
        self.assertEqual(target[0].pos, 124)
        profile96 = groove.Profilo('', '', '', 0, None, 1,
                                   {'kick': [groove.Passo(1, 100, 4, 1)]})
        target = MU.passi('.x..', tick_per_battuta=1920)
        MU.applica_groove(target, profile96, 'kick', tick_per_battuta=1920)
        self.assertEqual(target[0].pos, 140)
        with self.assertRaises(ValueError):
            MU.applica_groove([], profile, 'kick', profile_ppq=0)

    def test_quarter_duration_is_independent_of_six_eight_meter(self):
        from musicpal.interchange import from_tick_notes, to_tick_notes
        duration = MU.durata_in_tick('1/4', tick_per_battuta=384)
        self.assertEqual(duration, 96)
        pattern = from_tick_notes({60: [Note(0, duration)]}, ppq=96, meter=(6, 8))
        self.assertEqual(pattern.notes[0].duration, 1)
        self.assertEqual(pattern.beats_per_bar, 3)
        self.assertEqual(to_tick_notes(pattern)[60][0].length, 96)

    def test_dynamic_copy_and_swing(self):
        n = Note(0, 24, 90, 52)
        result = MU.dinamica({60: [n]}, .5)
        self.assertEqual(result[60][0], Note(0, 24, 45, 52))
        self.assertEqual(n.velocity, 90)
        self.assertAlmostEqual(MU.in_bur(MU.da_bur(2)), 2)
        self.assertEqual(groove.levare_da_posizioni([0, 48, 96, 144], 96), [0.5, 0.5])


if __name__ == '__main__':
    unittest.main()
