"""
Generate MD files for man pages
"""
import argparse
import re
import subprocess
from importlib.metadata import distribution
import importlib

DIST = "mypackage"
section_name = re.compile(r"^\w[\w ]*\w\:$")
usage = re.compile(r"^usage: ")
option = re.compile(r"^  ((?:\-{,2}[\w\-]*\w(?: \w+)?(?:, )?)+)(?:\s+(.*))?")
description_first_line = re.compile("^([^.]+)")
# .TH "$title/nowrap$" "$section/nowrap$" "$date/nowrap$" "$footer/nowrap$" "$header/nowrap$"


def main():
    """
    Man pages of CLI scripts of a Python package.
    """

    parser = argparse.ArgumentParser(
        description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--dist", required=True, help="Name of a Python package")
    ns = parser.parse_args()
    create_man_for_all(ns.dist)


def create_man_for_all(dist_name):
    """
    Create man pages for all script endpoints in the distribution.

    Args:
        dist_name: The name of the distribution
    """
    dist = distribution(dist_name)
    print(dist.version)
    for entry_point in dist.entry_points:
        name = entry_point.name
        print(name)
        module = importlib.import_module(entry_point.module, dist_name)
        ap = module.get_argument_parser()
        ap.formatter_class = ManHelpFormatter
        ap.prog = name

        print(ap.format_help())


def _get_script_metadata(name):
    fm = {}

    fm["title"] = name.upper()
    fm["section"] = 1
    fm["date"] = "2022-10-13"
    fm["footer"] = name.upper()  # aka source
    fm["header"] = "General Commands Manual"  # aka manual

    return fm


class ManHelpFormatter:
    def __init__(self, prog):
        self.prog = prog
        self._chunks = [".SH NAME", "short description"]
        self._description_seen = False

    def add_usage(self, usage, actions, mutually_exclusive_groups):
        section_header = ".SH SYNOPSYS\n"
        if usage:
            buf.append(usage)
            self._chunks.append(section_header + usage)
            return
        opt = []
        pos = []
        for action in actions:
            thing = self._Action(action)
            if thing.is_positional:
                pos.append(thing.get_usage())
                continue
            opt.append(thing.get_usage())

        options = " ".join((section_header, *opt, *pos))
        self._chunks.append(options)

    def add_text(self, txt):
        if not txt:
            return

        if not self._description_seen:
            mch = description_first_line.match(txt)
            self._chunks[1] = mch.group(1).strip()
            self._chunks.append(".SH DESCRIPTION")
        self._chunks.append(txt)

        #print(f"Adding text >{txt}<")

    def start_section(self, title):
        if not title:
            return
        self._chunks.append(f".SH {title.upper()}")
        pass
        #print(f"Start section {title}")

    def add_arguments(self, group_actions):
        for action in group_actions:
            self._chunks.append(self._Action(action).get_option_line())
        pass
        #print(f"Adding args {group_actions}")

    def end_section(self):
        pass
        #print(f"Section end")

    def format_help(self):
        return "\n".join(self._chunks)

    class _Action:
        def __init__(self, action):
            self.name = action.metavar or action.dest
            self.full_name = self.name
            self.required = action.required
            self.metavar = None
            self.is_positional = False
            self.help = action.help

            if not action.option_strings:
                self.is_positional = True
                return

            self.name = action.option_strings[0]
            self.full_name = ", ".join(action.option_strings)
            if action.__class__.__name__ not in (
                "_StoreTrueAction",
                "_StoreFalseAction",
                "_HelpAction",
            ):
                self.metavar = action.metavar or action.dest.upper()

        def get_usage(self):
            out = [self.name]
            if self.metavar:
                out.append(self.metavar)
            if not self.required:
                return f"[{' '.join(out)}]"
            return " ".join(out)
        
        def get_option_line(self):
            return f"{self.full_name}\t{self.help}"


if __name__ == "__main__":
    main()
