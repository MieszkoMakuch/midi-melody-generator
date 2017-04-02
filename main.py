import argparse

from MIDIMelody import MIDIMelody
from melody_generator import MelodyGenerator


def parse_arguments():
    mood_choices = [x.name for x in MIDIMelody.Moods]
    speed_choices = [x.name for x in MIDIMelody.Speeds]
    instrument_name_choices = [x.name for x in MIDIMelody.Instruments]
    instrument_value_choices = [x.value for x in MIDIMelody.Instruments]

    parser = argparse.ArgumentParser(description="Generate narcotic MIDI melody")
    parser.add_argument("-d", "--destination", dest="file_dest", metavar="", default=None,
                        help="Choose MIDI file destination (default \"midi/melody.mid\")")
    parser.add_argument("-m", "--mood", metavar="", choices=mood_choices, default=None,
                        help="Choose mood of the melody")
    parser.add_argument("-s", "--speed", metavar="", default=None,
                        help="Choose speed of the melody", choices=speed_choices)

    instrument = parser.add_mutually_exclusive_group()
    instrument.add_argument("-in", "--instrumentName", metavar="", default=None,
                            help="Choose name of the instrument", choices=instrument_name_choices)
    instrument.add_argument("-iv", "--instrumentValue", metavar="", default=None, type=int,
                            help="Choose value of the instrument", choices=instrument_value_choices)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.file_dest and not args.file_dest.endswith(".mid") and not args.file_dest.endswith(".midi"):
        args.file_dest += ".mid"

    # if instrument was chosen by value assign its name
    if args.instrumentValue is not None:
        args.instrumentName = MIDIMelody.Instruments(args.instrumentValue).name

    melody_generator = MelodyGenerator(file_dest=args.file_dest, mood=args.mood,
                                       speed=args.speed, instrument=args.instrumentName)

    melody_generator.generate_midi_melody()
