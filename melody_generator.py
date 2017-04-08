#!/usr/bin/env python
import random
from enum import Enum

from chords import Chord, Chords, ChordSeq
from melody_properties import MelodyProperties
from pyknon import genmidi
from pyknon.music import NoteSeq

""""Module responsible for melody generation (midi file generation)"""


class MelodyGenerator:
    """Class responsible for generating melody (midi file)."""

    def __init__(self, mood=None, speed=None, instrument=None, file_dest=None,
                 octave_shift=None, chord_seq=None, multiply_length=None):
        """All parameters are optional, if parameter is not specified
        it will be chosen randomly or by default"""

        if mood is None:
            self.mood = random.choice(list(MelodyProperties.Moods))
        else:
            self.mood = MelodyProperties.Moods[mood]

        if speed is None:
            self.speed = MelodyProperties.Speeds.MEDIUM
        else:
            self.speed = MelodyProperties.Speeds[speed]

        if instrument is None:
            self.instrument = random.choice([0, 2, 3])
        else:
            self.instrument = MelodyProperties.Instruments[instrument]

        if file_dest is None:
            self.file_dest = "melody.mid"
        else:
            self.file_dest = file_dest

        if octave_shift is None:
            if self.mood == MelodyProperties.Moods.HAPPY:
                octave_range = range(0, 2)
            elif self.mood == MelodyProperties.Moods.SAD:
                octave_range = range(-2, 1)
            else:
                octave_range = range(-1, 1)
            self.octave_shift = random.choice(octave_range)
        else:
            self.octave_shift = octave_shift

        if multiply_length is None:
            self.multiply_length = 3
        else:
            self.multiply_length = multiply_length

        if chord_seq is None:
            self.chord_seq = ChordSeq(mood=self.mood).octave_shift(self.octave_shift)
        elif isinstance(chord_seq, ChordSeq):
            self.chord_seq = chord_seq
        else:
            raise AttributeError("MelodyGenerator does not accept this type of argument")

        self.left_hand_rhythm = RhythmGenerator(self.chord_seq.__mul__(self.multiply_length),
                                                RhythmGenerator.RhythmTypes.LEFT_HAND)
        self.right_hand_rhythm = RhythmGenerator(self.chord_seq.__mul__(self.multiply_length),
                                                 RhythmGenerator.RhythmTypes.RIGHT_HAND)

    def generate_midi_melody(self):
        """Generates melody based on given parameters"""
        midi = genmidi.Midi(1, tempo=self.speed.value, instrument=self.instrument)
        midi.seq_chords(self.right_hand_rhythm.generate_note_seq())
        midi.seq_chords(self.left_hand_rhythm.generate_note_seq())
        midi.write(self.file_dest)

    def print_properties(self):
        divider = "\n###############################################################\n"
        print(divider)
        print("Melody has been successfully generated!")
        print("Melody properties: \n")
        print("\tDestination: \t\t%s" % self.file_dest)
        print("\tMood: \t\t\t%s" % MelodyProperties.Moods(self.mood).name)
        print("\tOctave shift: \t\t%i" % self.octave_shift)
        print("\tLength multiply: \t%i" % self.multiply_length)
        print("\tInstrument: \t\t%s" % MelodyProperties.Instruments(self.instrument).name)
        print("\tLeft hand rhythm: \t%s" % self.left_hand_rhythm.rhythm_pattern.__name__)
        print("\tRight hand rhythm: \t%s" % self.right_hand_rhythm.rhythm_pattern.__name__)
        print("\tChord sequence: \t%s" % self.chord_seq.verbose)
        print(divider)


class RhythmGenerator:
    """Class responsible for generating rhythm based on the given ChordSeq."""

    class RhythmTypes(Enum):
        LEFT_HAND = 1
        RIGHT_HAND = 2

    def __init__(self, chords, rhythm_type, subdivided=32):
        self.chords = chords
        self.subdivided = subdivided
        self.rhythms_right = [self.rhythm_4_40_right,
                              self.rhythm_6_17_right,
                              self.rhythm_heart_and_soul_right,
                              self.rhythm_8th_note_subdivided_right,
                              self.rhythm_16th_note_subdivided_right]

        self.rhythms_left = [self.rhythm_4_40_left,
                             self.rhythm_6_17_left,
                             self.rhythm_heart_and_soul_left,
                             self.rhythm_constant_chord_left]

        if rhythm_type == self.RhythmTypes.LEFT_HAND:
            self.rhythm_pattern = random.choice(self.rhythms_left)
        elif rhythm_type == self.RhythmTypes.RIGHT_HAND:
            self.rhythm_pattern = random.choice(self.rhythms_right)
        else:
            raise AttributeError("RhythmGenerator does not accept this rhythm_type")

    def generate_note_seq(self) -> [NoteSeq]:
        """Generates note sequence based on given chord sequence and rhythm pattern"""
        note_seq = []
        for chord in self.chords:
            note_seq += self.rhythm_pattern(chord)
        return [chord for chord in note_seq]

    # Definitions of basic rhythms patterns
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

        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(8 / self.subdivided))
        return rhythm

    def rhythm_6_17_right(self, chord: Chord) -> [Chord]:
        rhythm = []
        new_chord = chord

        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(12 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(8 / self.subdivided))
        return rhythm

    def rhythm_heart_and_soul_left(self, chord: Chord) -> [NoteSeq]:
        first_note = Chord([chord.first_note.octave_shift(-1)])
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

        rhythm.append(silence_chord.stretch_dur(8 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(silence_chord.stretch_dur(8 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))
        rhythm.append(new_chord.stretch_dur(4 / self.subdivided))

        return rhythm

    def rhythm_16th_note_subdivided_right(self, chord: Chord) -> [NoteSeq]:
        # works best with subdivided = 20
        chord = chord.stretch_dur(2 / self.subdivided)
        l1 = [NoteSeq([chord[0]])] + [NoteSeq([chord[1]])]
        l2 = [NoteSeq([chord[2]])] + [NoteSeq([chord[1]])]

        rhythm = []
        for i in range(0, 4):
            rhythm += l1 + l2

        return rhythm

    def rhythm_8th_note_subdivided_right(self, chord: Chord) -> [NoteSeq]:
        rhythm = []
        for i in range(0, 4):
            rhythm += [chord.top().stretch_dur(4 / self.subdivided)] + [chord.bottom().stretch_dur(4 / self.subdivided)]
        return rhythm

    def rhythm_constant_chord_left(self, chord: Chord) -> [NoteSeq]:
        first_note = chord.first_note.stretch_dur(32 / self.subdivided)
        rhythm = [Chord([first_note.octave_shift(-1)] + [first_note.octave_shift(-2)])]
        return rhythm
