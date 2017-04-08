# MIDI melody generator
Program creates chord progression then chooses one of the fundamental rhythms patterns to compose and generate a MIDI file.

## Usage
#### Download or clone this repository:
```bash
  $ git clone https://github.com/MieszkoMakuch/midi-melody-generator
  $ cd midi-melody-generator
```
#### Run main.py using pyton3:
```bash
  $ python3 main.py
```
#### Customizing your melody
To customize your melody you can specify the arguments listed below. When the argument is not specified it will be chosen randomly or by default.
```bash
  -h, --help            show this help message and exit
  -d , --destination    Choose MIDI file destination (default "melody.mid")
  -m , --mood           Choose mood of the melody
  -s , --speed          Choose speed of the melody
  -l , --length         Choose how many times the chord sequence will be
                        repeated
  -in , --instrumentName 
                        Choose name of the instrument
  -iv , --instrumentValue 
                        Choose value of the instrument (0, 1, 2, ..., 127)
```

#### Usage example:
```bash
  $ python3 main.py --destination myMelody.mid --mood HAPPY -in AcousticGrandPiano

###############################################################
 Melody has been successfully generated!
 Melody properties:

	Destination:        myMelody.mid
	Mood:               HAPPY
	Octave shift:       0
	Length multiply:    3
	Instrument:         AcousticGrandPiano
	Left hand rhythm:   rhythm_constant_chord_left
	Right hand rhythm:  rhythm_4_40_right
	Chord sequence:     <ChordSeq: [I-octave_shift(0), vi-octave_shift(0),
                        iii-octave_shift(0), V-octave_shift(0)]>
###############################################################
```

## How does it work?

#### Melody is being composed:
1. Program chooses scale based on the mood:
	- major scale for HAPPY mood
    - minor scale for SAD mood
2. Program creates chord progression based on one of the formula I \_ \_ IV or V
	I \_ \_ IV or V means: first chord in chord progression is always I, last chord in chord progression is either IV or V (cadence chords), two chords between them are chosen randomly. More about chord progression: https://www.youtube.com/watch?v=lY_llceEGFI

3. Program chooses one of the fundamental rhythm patterns for left and right hand and applies generated chord progression to this rhythms. More about rhythm patterns: https://www.youtube.com/watch?v=X1coZlJRrx8

#### MIDI file is being generated:
Slightly modified version of pyknon library (https://github.com/kroger/pyknon) is used to generate and save a MIDI file.

## Compatibility
Python 3 is required.