import argparse

from melody_properties import MelodyProperties


def parse_arguments():
    """Function responsible for parsing arguments"""

    mood_choices = [x.name for x in MelodyProperties.Moods]
    speed_choices = [x.name for x in MelodyProperties.Speeds]
    instrument_name_choices = [x.name for x in MelodyProperties.Instruments]
    instrument_value_choices = [x.value for x in MelodyProperties.Instruments]

    parser = argparse.ArgumentParser(description="Generate narcotic MIDI melody")
    parser.add_argument("-d", "--destination", dest="file_dest", metavar="", default=None,
                        help="Choose MIDI file destination (default \"melody.mid\")")
    parser.add_argument("-m", "--mood", metavar="", choices=mood_choices, default=None,
                        help="Choose mood of the melody")
    parser.add_argument("-s", "--speed", metavar="", default=None,
                        help="Choose speed of the melody", choices=speed_choices)
    parser.add_argument("-l", "--length", metavar="", type=int, choices=range(1, 60), default=None,
                        help="Choose how many times the chord sequence will be repeated")

    # Instrument may be specified either by its name or by its value (MIDI Program Change or "PC#")
    instrument = parser.add_mutually_exclusive_group()
    instrument.add_argument("-in", "--instrumentName", metavar="", default=None,
                            help="Choose name of the instrument", choices=instrument_name_choices)
    instrument.add_argument("-iv", "--instrumentValue", metavar="", default=None, type=int,
                            help="Choose value of the instrument", choices=instrument_value_choices)

    args = parser.parse_args()

    # check if file_dest has valid extension (.mid or .midi)
    if args.file_dest and not args.file_dest.endswith(".mid") and not args.file_dest.endswith(".midi"):
        args.file_dest += ".mid"

    # if instrument was chosen by value assign its name
    if args.instrumentValue is not None:
        args.instrumentName = MelodyProperties.Instruments(args.instrumentValue).name

    return args
