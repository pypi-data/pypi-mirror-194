"""This provides a custom UI for doit.

It is based on the ConsoleReporter, but uses rich to provide a more
interesting UI. It is entirely optional, and must be explicitly
enabled via the presence of the `ALTO_RICH_UI` environment variable.
"""

import time
from typing import Dict, List

import doit.task
from doit.reporter import ConsoleReporter
from doit.task import Task
from rich.console import Console
from rich.progress import (
    Progress,
    SpinnerColumn,
    TaskID,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)


class InjectedIO:
    def __init__(self, ui: "AltoUI", method="write"):
        self.ui = ui
        self.method = method

    def write(self, text):
        getattr(self.ui, self.method)(text)

    def flush(self):
        pass

    def isatty(self):
        return False

    def __reduce__(self):
        return self.__class__, (self.ui, self.method)

    def __getstate__(self):
        return self.ui, self.method

    def __setstate__(self, state):
        self.ui, self.method = state


def monkeypatch_stream(ui: "AltoUI"):
    doit.task.Stream._get_out_err = lambda _, verbosity: (
        InjectedIO(ui=ui, method="write_stdout"),
        InjectedIO(ui=ui, method="write_stderr"),
    )


class AltoUI(ConsoleReporter):
    desc = "Alto UI"
    task_ids: Dict[str, TaskID] = {}

    def __init__(self, outstream, options):
        _ = outstream
        self.console = Console()
        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[dim]{task.fields[name]}"),
            TextColumn("[progress.description]{task.description}"),
            TaskProgressColumn(),
            TimeElapsedColumn(),
            TextColumn("{task.fields[status]}"),
            console=self.console,
            redirect_stderr=False,
            redirect_stdout=False,
            expand=True,
        )
        super().__init__(self.outstream, options)

        monkeypatch_stream(self)
        self.progress.start()

    @property
    def outstream(self):
        return self.progress.console.file

    @outstream.setter
    def outstream(self, value):
        self.progress.console.file = value

    def write(self, text):
        self.progress.console.print(text, end="")

    write_stdout = write

    def write_stderr(self, text):
        self.progress.console.print(text, end="")

    def flush(self):
        pass

    def initialize(self, tasks: List[Task], selected_tasks: List[str]) -> None:
        self.write("Running [bold]Alto[/bold] version: [green]0.1.0[/green]")
        self.time = time.time()

    def get_status(self, task: Task) -> None:
        if task.name[0] != "_":
            self.task_ids[task.name] = self.progress.add_task(
                description=task.doc or f"Running {task.name}",
                total=1,
                start=False,
                name=task.title(),
                status="[yellow]checking dependencies",
            )

    def execute_task(self, task: Task) -> None:
        if task.name[0] != "_":
            try:
                self.progress.update(self.task_ids[task.name], status="[yellow]started")
                self.progress.start_task(self.task_ids[task.name])
            except KeyError:
                pass

    def skip_uptodate(self, task: Task) -> None:
        if task.name[0] != "_":
            try:
                self.progress.start_task(self.task_ids[task.name])
                self.progress.update(
                    self.task_ids[task.name], completed=1, status="[green dim]up-to-date"
                )
                self.progress.stop_task(self.task_ids[task.name])
            except KeyError:
                pass

    def skip_ignore(self, task: Task) -> None:
        if task.name[0] != "_":
            try:
                self.progress.update(
                    self.task_ids[task.name], completed=1, status="[yellow dim]ignored"
                )
                self.progress.stop_task(self.task_ids[task.name])
            except KeyError:
                pass

    def add_success(self, task: Task) -> None:
        if task.name[0] != "_":
            try:
                self.progress.update(self.task_ids[task.name], completed=1, status="[green]success")
                self.progress.stop_task(self.task_ids[task.name])
            except KeyError:
                pass

    def add_failure(self, task, fail):
        try:
            self.progress.update(self.task_ids[task.name], completed=1, status="[red bold]failed")
        except KeyError:
            pass
        super().add_failure(task, fail)

    def _write_failure(self, result, write_exception: bool = True) -> None:
        if write_exception:
            self.write_stderr(result["exception"].get_msg())
            self.console.bell()

    def complete_run(self) -> None:
        for result in self.failures:
            task: Task = result["task"]
            if not task.executed:
                continue
            show_err = task.verbosity < 1 or self.failure_verbosity > 0
            show_out = task.verbosity < 2 or self.failure_verbosity == 2
            if show_err or show_out:
                self.write("#" * 40 + "\n")
            if show_err:
                self._write_failure(result, write_exception=self.failure_verbosity)
                err = "".join([a.err for a in task.actions if a.err])
                self.write_stderr("{} <stderr>:\n{}\n".format(task.name, err))
            if show_out:
                out = "".join([a.out for a in task.actions if a.out])
                self.write_stdout("{} <stdout>:\n{}\n".format(task.name, out))
        if self.runtime_errors:
            self.write_stderr("#" * 40 + "\n")
            self.write_stderr("Execution aborted.\n")
            self.write_stderr("\n".join(self.runtime_errors))
            self.write_stderr("\n")
        self.write(f"Total runtime: [green]{time.time() - self.time:.2f}[/green] seconds")
        self.progress.stop()
