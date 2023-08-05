import os
import subprocess
from typing import Optional

import pkg_resources
import typer
from questionary.form import form

from fastapi_cli_tool.constants import (
    Database,
    License,
    PackageManager,
    PythonVersion,
    DatabaseORM,
)
from fastapi_cli_tool.context import AppContext, ProjectContext
from fastapi_cli_tool.generator import generate_app, generate_project
from fastapi_cli_tool.helpers import binary_question, question, question_input

app = typer.Typer(
    add_completion=False,
    help="Managing FastAPI projects made easy!",
    name="Manage FastAPI",
)


@app.command(help="Creates a FastAPI project.")
def startproject(name: str):
    try:
        results = form(
            packaging=question(PackageManager),
            python=question(PythonVersion),
            license=question(License),
            database=question(Database),
            database_orm=question(DatabaseORM),
            use_code_formatter=binary_question("use code formatter:"),
        ).ask()
        context = ProjectContext(name=name, **results)
        generate_project(context)
    except Exception as e:
        SystemExit(1)


@app.command(help="Creates a FastAPI component.")
def startapp():
    if os.path.exists(os.path.join(os.getcwd(), "manage.py")):
        result = form(name=question_input("Choose a name")).ask()
        context = AppContext(**result)
        generate_app(context)
    else:
        typer.echo(f"No FastApi Project Found! ❌")


@app.command(help="Run a FastAPI application.")
def run(prod: bool = typer.Option(False)):
    args = []
    if not prod:
        args.append("--reload")
    app_file = os.getenv("FASTAPI_APP", "core.app")
    subprocess.call(["uvicorn", f"{app_file}:app", *args])


def version_callback(value: bool):
    if value:
        version = pkg_resources.get_distribution("fastapi-cli").version
        typer.echo(f"fastapi-cli, version {version}")
        raise typer.Exit()


@app.callback()
def main(
    version: bool = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the Manage FastAPI version information.",
    )
):
    ...


if __name__ == "__main__":
    app()
