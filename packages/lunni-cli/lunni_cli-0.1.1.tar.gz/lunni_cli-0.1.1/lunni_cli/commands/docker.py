import typer
from os import execlp

def dev(
    build: bool = typer.Option(False, "--build /", help="Build images before starting containers."),
    detach: bool = typer.Option(False, "-d /", "--detach /", help="Run containers in the background."),
):
    """
    Create and start containers. Wraps `docker-compose up`.
    """

    args = []
    if build: args.append("--build")
    if detach: args.append("--detach")

    execlp("docker-compose", "docker-compose", "up", *args)


def run(
    build: bool = typer.Option(False, "--build /", help="Build images before starting container."),
    detach: bool = typer.Option(False, "-d /", "--detach /", help="Run container in the background and print container ID."),
    service: str = typer.Argument(...),
    args: list[str] = typer.Argument(None),
):
    """
    Run a one-off command on a service. Wraps `docker-compose run`.
    """

    docker_args = []
    if build: docker_args.append("--build")
    if detach: docker_args.append("--detach")
    docker_args.append(service)
    docker_args.extend(args)

    execlp("docker-compose", "docker-compose", "up", *docker_args)
