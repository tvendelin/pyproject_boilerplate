"""
Placeholder to test a project setup
"""
from jinja2 import Environment, PackageLoader, select_autoescape


def return_a_string():
    """
    Returns "Ohoo!"
    """

    # Jinja2 is used only for the sake of having a dependency
    tenv = Environment(loader=PackageLoader("mymodule"), autoescape=select_autoescape())

    template = tenv.get_template("ohoo.j2")
    return template.render(text="Ohoo!")


def main():
    """
    Main function
    """
    print(return_a_string())


if __name__ == "__main__":
    main()
