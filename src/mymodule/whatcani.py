"Display available command-line tools"
import argparse
import re
from importlib.metadata import distribution

DIST = "mypackage"


def get_argument_parser():
    """
    Returns an instance of argparse.ArgumentParser.
    Useful for generation of man pages.
    """
    parser = argparse.ArgumentParser(description="Display available CLI utilities", add_help=True)

    parser.add_argument(
        "-q",
        "--quiet",
        help="Display full paths to commands without descriptions",
        action="store_true",
    )
    return parser


def list_tasks():
    "Display available command-line tools"

    parser = get_argument_parser()

    parser.add_argument(
        "-q",
        "--quiet",
        help="Display full paths to commands without descriptions",
        action="store_true",
    )
    args = parser.parse_args()

    if args.quiet:
        lines = []
    else:
        lines = ["", "Available Commands", "", "For help on specific command, run it with -h", ""]

    dist = distribution(DIST)

    for ep in dist.entry_points:
        doc = ep.load().__doc__
        doc = re.sub(r"\n +", "\n", doc, flags=re.DOTALL)
        doc = re.sub(r"^\n+", "", doc, flags=re.DOTALL)
        doc = re.sub("^", "\t", doc, flags=re.MULTILINE)
        lines.append(ep.name)
        lines.append("")
        lines.append(doc)
        lines.append("")

    print("\n".join(lines))
