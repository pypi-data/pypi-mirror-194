import typer
from cookiecutter.main import cookiecutter


def create(
    template: str = ...,
    checkout: str = typer.Option(None, "-c", "--checkout", help="Branch, tag or commit to checkout after git clone", metavar="<branch>"),
    output_dir: str = typer.Option(".", "-o", "--output-dir", help="Where to output the generated project dir into", metavar="<path>"),
    no_input: bool = typer.Option(False, "--no-input/", help="Do not prompt for parameters")
):
    """
    Create a project from TEMPLATE.

    You can view the list of available templates at https://gitlab.com/lunni/templates.
    You can also specify a custom template by just pasting a Git URI.
    """

    # TODO: better check
    if "/" not in template:
        template = f"https://gitlab.com/lunni/templates/{template}.git"

    print(template)

    cookiecutter(
        template=template,
        checkout=checkout,
        output_dir=output_dir,
        no_input=no_input,
    )
