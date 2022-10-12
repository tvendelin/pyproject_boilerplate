"""
Generate MD files for man pages
"""
import argparse
import re
import subprocess
from importlib.metadata import distribution

import yaml

DIST = "mypackage"
section_name = re.compile(r"^\w[\w ]*\w\:$")
usage = re.compile(r"^usage: ")
option = re.compile(r"^  ((?:\-{,2}[\w\-]*\w(?: \w+)?(?:, )?)+)(?:\s+(.*))?")
# .TH "$title/nowrap$" "$section/nowrap$" "$date/nowrap$" "$footer/nowrap$" "$header/nowrap$"


def main():
    """
    Markdown files for man pages of CLI scripts of a Python package.

    Creates markdown files in `man_md` directory for each CLI endpoint
    in a Python package. The man pages can be generated with

    ```
    pandoc -s -t man -o <SCRIPT> man_md/<SCRIPT>.1.md
    ```

    The package should be already installed, preferrably
    in a virtual environment.
    """

    parser = argparse.ArgumentParser(
        description=main.__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-d", "--dist", required=True, help="Name of a Python package")
    ns = parser.parse_args()
    create_md_for_man_all(ns.dist)


def create_md_for_man_all(dist_name):
    """
    Create .md files for all script endpoints in the distribution.

    Args:
        dist_name: The name of the distribution
    """
    dist = distribution(dist_name)
    for entry_point in dist.entry_points:
        name = entry_point.name

        help_msg = _get_help_msg(name)
        frontmatter = _get_script_metadata(name)

        md = get_markdown(name=name, help_msg=help_msg, frontmatter=frontmatter)

        with open(f"man_md/{name}.{frontmatter['section']}.md", "w", encoding="UTF-8") as fh:
            fh.write(md)


def _get_script_metadata(name):
    fm = {}

    fm["title"] = name.upper()
    fm["section"] = 1
    fm["date"] = "2022-10-13"
    fm["footer"] = name.upper()  # aka source
    fm["header"] = "General Commands Manual"  # aka manual

    return fm


def _get_help_msg(name):
    return (
        subprocess.run([name, "-h"], stdout=subprocess.PIPE, check=True)
        .stdout.decode("utf-8")
        .split("\n")
    )


def get_markdown(name, help_msg, frontmatter):
    """
    Generate Markdown from a help message suitable for man page generation with pandoc

    Args:
        name: the name of the distribution
        help_msg: help message emitted by argparse
        frontmatter: a dict with template params, must include title, section, date, footer, header
    """

    out = [yaml.dump(frontmatter, explicit_start=True, explicit_end=True), "# NAME\n"]

    synopsis = _get_synopsis(help_msg)
    description = _get_description(help_msg)
    subj = re.match(r"^([^\.]*)", description[0]).group(1)

    out.append(f"{name} - {subj}\n")
    out.append("# SYNOPSIS\n")
    out.append(synopsis)
    out.append("")
    out.append("# DESCRIPTION\n")
    out.append("\n".join(description))
    out.append("")

    isHelpText = False

    while help_msg:
        line = help_msg.pop(0)
        isOption = option.match(line)
        if isOption:
            option_spec = isOption.group(1)
            option_help = isOption.group(2)

            if isHelpText:
                out.append("")
            isHelpText = True

            out.append(f"## `{option_spec}`")
            out.append("")
            if option_help:
                out.append(f"{option_help}")
                out.append("")
            continue

        if section_name.match(line):
            if isHelpText:
                out.append("")

            line = f"# {line[:-1].upper()}\n"
            isHelpText = False
            out.append(line)
            #            out.append("")
            continue

        if line:
            out.append(f"{line.strip()}")
            continue

    return "\n".join(out)


def _get_synopsis(help_msg):
    line = help_msg.pop(0)
    line = usage.sub("", line)

    synopsis = [line.strip()]
    while True:
        line = help_msg.pop(0)
        if not line:
            break
        synopsis.append(line.strip())
    return " ".join(synopsis)


def _get_description(help_msg):
    line = None
    while not line:
        line = help_msg.pop(0)

    description = [line.strip()]

    while not section_name.match(help_msg[0]):
        line = help_msg.pop(0)
        description.append(line.strip())

    return description


if __name__ == "__main__":
    main()
