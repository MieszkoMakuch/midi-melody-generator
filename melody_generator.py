#!/usr/bin/env python
import random
from enum import Enum

from melody_properties import MelodyProperties
from chords import Chord, Chords, ChordSeq
from pyknon import genmidi
from pyknon.music import NoteSeq


class RhythmGenerator:
    class RhythmTypes(Enum):
        LEFT = 1
        RIGHT = 2

    def __init__(self, chords, rhythm_type, subdivided=32):
        self.chords = chords
        self.subdivided = subdivided
        self.rhythms_right = [self.rhythm_4_40_right,
                              self.rhythm_6_17_right,
                              self.rhythm_heart_and_soul_right,
                              self.rhythm_8th_note_pattern_right,
                              self.rhythm_16th_note_pattern_right]

        self.rhythms_left = [self.rhythm_4_40_left,
                             self.rhythm_6_17_left,
                             self.rhythm_heart_and_soul_left,
                             self.rhythm_constant_chord_left]

        if rhythm_type == self.RhythmTypes.LEFT:
            self.rhythm_pattern = random.choice(self.rhythms_left)
            print("Chosen rhythm: " + self.rhythm_pattern.__name__)
        elif rhythm_type == self.RhythmTypes.RIGHT:
            self.rhythm_pattern = random.choice(self.rhythms_right)
            print("Chosen rhythm: " + self.rhythm_pattern.__name__)
        else:
            raise AttributeError("RhythmGenerator does not accept this rhythm_type")

    def generate_note_seq(self) -> [NoteSeq]:
        note_seq = []
        for chord in self.chords:
            note_seq += self.rhythm_pattern(chord)
        return [chord for chord in note_seq]

    def get_rhythm_pattern(self, left: bool):
        if left:
            rhythm = random.choice(self.rhythms_left)
        else:
            rhythm = random.choice(self.rhythms_right)
        return rhythm

    # def generate_rhythm(self):
    def rhythm_4_40_left(self, chord: Chord) -> [Chord]:
        first_note = Chord([chord.first_note.octave_shift(-1)])
        left_hand_seq = []
        silence = Chords.silence

        left_hand_seq.append(first_note.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(first_note.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(silence.stretch_dur(4 / self.subdivided))

        return left_hand_seq

    def rhythm_4_40_right(self, chord: Chord) -> [Chord]:
        rhythm = []
        new_chord = chord
        silence_chord = Chords.silence

        rhythm.append(silence_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(4 / self.subdivided))

        return rhythm

    def rhythm_6_17_left(self, chord: Chord) -> [Chord]:
        rhythm = []
        new_chord = NoteSeq()

        new_chord.append(chord.first_note.octave_shift(-1))
        new_chord.append(chord.first_note.octave_shift(-2))

        # sum = 21
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(8 / self.subdivided))
        return rhythm

    def rhythm_6_17_right(self, chord: Chord) -> [Chord]:
        rhythm = []
        new_chord = chord

        # sum = 21
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(8 / self.subdivided))
        return rhythm

    def rhythm_heart_and_soul_left(self, chord: Chord) -> [NoteSeq]:
        first_note = Chord([chord.first_note.octave_shift(-1)])
        silence = Chords.silence
        left_hand_seq = []

        left_hand_seq.append(first_note.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(first_note.stretch_dur(12 / self.subdivided))
        left_hand_seq.append(first_note.stretch_dur(4 / self.subdivided))
        left_hand_seq.append(first_note.stretch_dur(12 / self.subdivided))
        return left_hand_seq

    def rhythm_heart_and_soul_right(self, chord: Chord) -> [NoteSeq]:
        rhythm = []
        new_chord = chord
        silence_chord = NoteSeq("R")

        # sum = 11
        rhythm.append(silence_chord.stretch_dur(8 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(8 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))

        return rhythm

    '''someone like you'''

    def rhythm_16th_note_pattern_right(self, chord: Chord) -> [NoteSeq]:
        # works best with divide_by = 20
        chord = chord.stretch_dur(2 / self.subdivided)
        l1 = [NoteSeq([chord[0]])] + [NoteSeq([chord[1]])]
        l2 = [NoteSeq([chord[2]])] + [NoteSeq([chord[1]])]

        rhythm = []
        for i in range(0, 4):
            rhythm += l1 + l2

        return rhythm

    def rhythm_8th_note_pattern_right(self, chord: Chord) -> [NoteSeq]:
        rhythm = []
        for i in range(0, 4):
            rhythm += [chord.top().stretch_dur(4 / self.subdivided)] + [chord.bottom().stretch_dur(4 / self.subdivided)]
        return rhythm

    def rhythm_constant_chord_left(self, chord: Chord) -> [NoteSeq]:
        first_note = chord.first_note.stretch_dur(32 / self.subdivided)
        rhythm = [Chord([first_note.octave_shift(-1)] + [first_note.octave_shift(-2)])]
        return rhythm


class MelodyGenerator:
    def __init__(self, mood=None, speed=None, instrument=None, file_dest=None):
        if mood is None:
            self.mood = MelodyProperties.Moods.HAPPY
        else:
            self.mood = MelodyProperties.Moods[mood]

        if speed is None:
            self.speed = MelodyProperties.Speeds.MEDIUM
        else:
            self.speed = MelodyProperties.Speeds[speed]

        if instrument is None:
            self.instrument = random.choice([1, 3])
        else:
            self.instrument = MelodyProperties.Instruments[instrument]

        if file_dest is None:
            self.file_dest = "midi/melodyMG.mid"
        else:
            self.file_dest = file_dest

    def generate_midi_melody(self):
        midi = genmidi.Midi(1, tempo=self.speed.value, instrument=self.instrument)
        print("Instrument: " + MelodyProperties.Instruments(self.instrument).name)

        octave_shift = -1
        chord_seq = ChordSeq(mood=self.mood).octave_shift(octave_shift).__mul__(2)
        print("Chord sequence: " + chord_seq.verbose)

        right_hand_seq = RhythmGenerator(chord_seq, RhythmGenerator.RhythmTypes.RIGHT).generate_note_seq()
        left_hand_seq = RhythmGenerator(chord_seq, RhythmGenerator.RhythmTypes.LEFT).generate_note_seq()

        midi.seq_chords(right_hand_seq)
        midi.seq_chords(left_hand_seq)
        midi.write(self.file_dest)
        print("Melody generated")
