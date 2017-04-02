import argparse

from MIDIMelody import MIDIMelody
from melody_generator import MelodyGenerator


def parse_arguments():
    parser = argparse.ArgumentParser(description="Generate narcotic MIDI melody")
    parser.add_argument("-d", "--destination", dest="file_dest", metavar="",
                        help="Choose MIDI file destination (default \"midi/melody.mid\")")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()
    if args.file_dest:
        MelodyGenerator(file_dest=args.file_dest).generate_midi_melody
    else:
        melody_generator = MelodyGenerator(MIDIMelody.Moods.HAPPY)
        melody_generator.generate_midi_melody()
