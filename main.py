from arg_parser import parse_arguments
from melody_generator import MelodyGenerator

if __name__ == '__main__':
    args = parse_arguments()
    midi = MelodyGenerator(file_dest=args.file_dest, mood=args.mood,
                           speed=args.speed, instrument=args.instrumentName, multiply_length=args.length)
    midi.generate_midi_melody()
    midi.print_properties()
