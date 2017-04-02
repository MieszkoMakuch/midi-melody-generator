from arg_parser import parse_arguments
from melody_generator import MelodyGenerator

if __name__ == '__main__':
    args = parse_arguments()
    melody_generator = MelodyGenerator(file_dest=args.file_dest, mood=args.mood,
                                       speed=args.speed, instrument=args.instrumentName)
    melody_generator.generate_midi_melody()

# TODO - parametrize: octave_shift, melody length
