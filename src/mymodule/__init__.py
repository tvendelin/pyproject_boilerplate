"""
Placeholder to test a project setup
"""
import argparse

from jinja2 import Environment, PackageLoader, select_autoescape


def return_a_string():
    """
    Returns "Ohoo!"
    """

    # Jinja2 is used only for the sake of having a dependency
    tenv = Environment(loader=PackageLoader("mymodule"), autoescape=select_autoescape())

    template = tenv.get_template("ohoo.j2")
    return template.render(text="Ohoo!")


def get_argument_parser():
    """
    Returns an instance of argparse.ArgumentParser.
    Useful for generation of man pages.
    """
    parser = argparse.ArgumentParser(
        prog="ohoo", description=main.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("bar", help="bar has no effect")
    parser.add_argument(
        "abracadabraabracadabrabracadabrabracadabrabracadabrabracadabrabracadabrabracadabrabracad",
        help="this long param has no effect",
    )
    parser.add_argument("--foo", "-f", help="has no effect", metavar="Foo_value")
    parser.add_argument(
        "--baz-ladida",
        "-b",
        help=(
            "has no effect whatever whatsoever has no effect whatever whatsoeverhas no effect"
            " whatever whatsoever"
        ),
        required=True,
    )
    return parser


def main():
    """
    Prints "Ohoo!" and exits.

    This program doesn't do anything useful by itself,
    but helps to develop packaging utilities by the virtue
    of its very existence.
    """

    parser = get_argument_parser()
    parser.parse_args()
    print(return_a_string())


if __name__ == "__main__":
    main()
