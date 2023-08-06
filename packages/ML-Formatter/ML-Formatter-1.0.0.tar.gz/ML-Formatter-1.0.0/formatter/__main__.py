import argparse
import logging
import os

from formatter.deepspeech import DeepSpeech


class ReadableDir(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        prospective_dir = values
        if not os.path.isdir(prospective_dir):
            raise argparse.ArgumentError(
                self, "{0} is not a valid path".format(prospective_dir)
            )
        if os.access(prospective_dir, os.R_OK):
            setattr(namespace, self.dest, prospective_dir)
        else:
            raise argparse.ArgumentError(
                self, "{0} is not a readable dir".format(prospective_dir)
            )


parser = argparse.ArgumentParser(
    description="Given a set of media, create and output to the required spec of certain ML programs"
)
# parser.add_argument(
#    "-v",
#    "--verbosity",
#    type=int,
#    default=0,
#    choices=[0, 1, 2, 3, 4, 5],
#    help="Increase output verbosity",
# )
log_level = parser.add_mutually_exclusive_group()
log_level.add_argument("-v", "--verbose", action="store_true")
log_level.add_argument("-q", "--quiet", action="store_true")
parser.add_argument(
    "--dont-shuffle",
    action="store_true",
    help="Don't shuffle before splitting into runs",
)
parser.add_argument(
    "--train",
    default=0.7,
    type=float,
    help="Training part of train/test/val split. Out of 1",
)
parser.add_argument(
    "--test",
    default=0.2,
    type=float,
    help="Testing part of train/test/val split. Out of 1",
)
parser.add_argument(
    "--val",
    default=0.1,
    type=float,
    help="Validation part of train/test/val split. Out of 1",
)
parser.add_argument(
    "--parser",
    choices=["deepspeech"],
    default="deepspeech",
    help="The format you wish to receive as output",
)
parser.add_argument(
    "--media_type",
    choices=["wav"],
    default="wav",
    help="The file extension of media files",
)
parser.add_argument(
    "--transcript_type",
    choices=["txt"],
    default="txt",
    help="The file extension of text transcript files",
)
parser.add_argument(
    "--media",
    action=ReadableDir,
    default=".",
    help="Path to the directory containing media files",
)
parser.add_argument(
    "--transcript",
    action=ReadableDir,
    default=".",
    help="Path to files containing text transcripts",
)
parser.add_argument(
    "--output",
    action=ReadableDir,
    default=".",
    help="Path to directory to use as an output folder",
)
args = parser.parse_args()

# Setup logging
if args.quiet:
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(module)s | %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        level=logging.NOTSET,
    )
elif args.verbose:
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(module)s | %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        level=logging.DEBUG,
    )
else:
    logging.basicConfig(
        format="%(levelname)s | %(asctime)s | %(module)s | %(message)s",
        datefmt="%d/%m/%Y %I:%M:%S %p",
        level=logging.WARN,
    )

# Get train / test / val split
train = args.train
test = args.test
val = args.val
total = train + test + val

if round(total) != 1:
    raise RuntimeError("Train + Test + Validation split must equal 1")

log = logging.getLogger(__name__)
log.debug("Media directory: %s", args.media)
log.debug("Media file type: %s", args.media_type)
log.debug("Transcript directory: %s", args.transcript)
log.debug("Transcript file type: %s", args.transcript_type)
log.debug("Output directory: %s", args.output)
log.debug("Selected parser: %s", args.parser)

# Setup ghetto switch statement
backends = {"deepspeech": DeepSpeech}

# Lets us do cool things like this
backends[args.parser](
    media_dir=args.media,
    transcript_dir=args.transcript,
    output_dir=args.output,
    media_type=args.media_type,
    transcript_type=args.transcript_type,
    train=train,
    test=test,
    val=val,
    dont_shuffle=args.dont_shuffle,
).run()
