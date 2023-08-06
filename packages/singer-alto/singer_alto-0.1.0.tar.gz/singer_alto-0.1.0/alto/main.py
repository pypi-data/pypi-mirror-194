#! /usr/bin/env python3
"""Main entry point for the CLI."""
import os
import sys
import threading
import typing as t
from contextlib import contextmanager
from pathlib import Path

import tomlkit
from doit.cmd_base import Command, ModuleTaskLoader
from doit.cmd_run import Run
from doit.doit_cmd import DoitMain

import alto.engine
from alto.cmd import AltoCmd
from alto.constants import DEFAULT_ENVIRONMENT

T_LOCALS = threading.local()
"""Thread-local storage for the CLI."""

class AltoInit(Command):
    doc_purpose = "Initialize a new project"
    doc_usage = "alto init"
    doc_description = (
        "Scan the current directory for a file named alto.{toml,yml,yaml,json} and "
        "create one if it doesn't exist."
    )

    def execute(self, opt_values, pos_args):
        """Initialize a new project."""
        config_fname = "alto.toml"
        secret_fname = "alto.secrets.toml"
        config_path = t.cast(Path, T_LOCALS.root).joinpath(config_fname)
        secret_path = t.cast(Path, T_LOCALS.root).joinpath(secret_fname)
        try:
            if AltoMain.conf_name:
                print("An Alto file already exists in {}".format(t.cast(Path, T_LOCALS.root)))
                return 1

            while True:
                confirm = input(
                    f"Files to generate:\n{t.cast(Path, T_LOCALS.root).joinpath(config_fname)}\n"
                    f"{t.cast(Path, T_LOCALS.root).joinpath(secret_fname)}\n"
                    "Proceed? [y/N]: ",
                )
                if confirm in ("y", "Y", "yes", "Yes", "YES"):
                    break
                else:
                    print("Aborting...")
                    return 0

            print("Initializing a new project in {}".format(t.cast(Path, T_LOCALS.root)))
            config_path.write_text(
                tomlkit.dumps(
                    {
                        "default": {
                            "project_name": os.urandom(4).hex(),
                            "extensions": [],
                            "namespace": "raw",
                            "taps": {
                                "tap-carbon-intensity": {
                                    "pip_url": (
                                        "git+https://gitlab.com/meltano/tap-carbon-intensity.git"
                                        "#egg=tap_carbon_intensity"
                                    ),
                                    "namespace": "carbon_intensity",
                                    "config": {},
                                    "capabilities": ["state", "catalog"],
                                    "select": ["*.*"],
                                }
                            },
                            "targets": {
                                "target-jsonl": {
                                    "pip_url": "target-jsonl==0.1.4",
                                    "config": {"destination_path": "output"},
                                }
                            },
                        }
                    }
                )
            )
            secret_path.write_text(tomlkit.dumps({"default": {"taps": {}, "targets": {}}}))
        except Exception as e:
            print("Failed to initialize project: {}".format(e))
            return 1
        else:
            return 0


class AltoRun(Run):
    """Run the project."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class AltoRepl(Command):
    doc_purpose = "Drop into an interactive prompt with the project loaded"
    doc_usage = "alto repl"
    doc_description = "Uses cmd.Cmd to drop into an interactive prompt with the project loaded."

    def execute(self, opt_values, pos_args):
        """Drop into a REPL."""
        _ = pos_args
        engine = alto.engine.AltoTaskEngine(root_dir=T_LOCALS.root)
        engine.setup(opt_values)
        AltoCmd(engine=engine).cmdloop()


class AltoMain(DoitMain):
    """Main entry point for the CLI."""

    root = Path.cwd()
    conf_name = None

    def get_cmds(self):
        """Get the commands to register.
        
        This shows how we can add commands as well as override existing ones.
        """
        commands = super().get_cmds()
        commands["init"] = AltoInit
        commands["run"] = AltoRun
        commands["repl"] = AltoRepl
        return commands


def main():
    """Main entry point for the CLI."""
    _ = ModuleTaskLoader
    args = list(sys.argv[1:])
    T_LOCALS.root = root = _get_root_scrub_args(args)

    conf_name = None
    for ext in ("toml", "yml", "yaml", "json"):
        if (root / f"alto.{ext}").exists():
            conf_name = f"alto.{ext}"
            break

    if not conf_name and "init" not in args:
        print(
            f"No Alto file found in {root.resolve()}\n"
            "Run `alto init` to create one or invoke "
            "alto with -r/--root to specify a directory..."
        )
        return 1
    else:
        f"Config {conf_name} found in {root}"
        AltoMain.conf_name = conf_name

    if "ALTO_ENV" not in os.environ:
        os.environ["ALTO_ENV"] = DEFAULT_ENVIRONMENT

    @contextmanager
    def _ctx(path):
        odir = Path.cwd()
        os.chdir(path)
        try:
            yield
        finally:
            os.chdir(odir)

    with _ctx(root):
        return AltoMain(
            alto.engine.AltoTaskEngine(Path.cwd()),
            extra_config={},
        ).run(args)


def _get_root_scrub_args(args: t.List[str]) -> Path:
    """Get the root directory and scrub the sys args.
    
    This is a helper function for the main entry point. It's used to get the root
    directory and scrub the sys args so that the doit CLI doesn't complain about
    unrecognized arguments.
    """
    for ix, arg in enumerate(list(args)):
        if arg in ("--root", "-r"):
            root = Path(args[ix + 1])
            assert root.is_dir()
            args.pop(ix)
            args.pop(ix)
            break
        elif arg.startswith("--root="):
            root = Path(arg.split("=", 1)[1])
            assert root.is_dir()
            args.pop(ix)
            break
    else:
        root = Path.cwd()
    return root


if __name__ == "__main__":
    sys.exit(main())
