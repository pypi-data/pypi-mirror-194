# Lunni CLI

Lunni's command line interface lets you set up projects ready for continuous
deployment with Lunni, straight from the command line.

## Installation

To install Lunni CLI, make sure you have Python version 3.11 or later. You'll
also want to [have pipx](https://github.com/pypa/pipx#install-pipx), a package
manager for installing Python CLI tools.

```
pipx install lunni-cli
lunni --install-completion [bash|zsh|fish|powershell]
```

This installs Lunni CLI globally, so you can run `lunni` commands from any
directory. You can check the version and find out some basic information about
the tool with the following command:

```
lunni version
```


## CLI commands

To get a list of commands, run `lunni --help`. To get a list of command
arguments & flags run `lunni COMMAND --help`.


## lunni create

Set up projects ready for deployment on Lunni (or Docker Swarm).

We provide some templates you can use:

- [Modern Python setup]() with Poetry, FastAPI or Flask, CI/CD, code quality
  and testing

- more coming soon!


## lunni dev & run

Run an app locally. This just wraps `docker-compose up` and `docker-compose
run` respectively, but it allows you to save some keystrokes.
