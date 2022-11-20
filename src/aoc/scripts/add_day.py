#!/usr/bin/env python3

from datetime import datetime
import os
from textwrap import wrap

from aoc import ROOT_DIR
from aoc.utils.console import console
from aoc_to_markdown import get_markdown
import rich_click as click
from jinja2 import Template


@click.command()
@click.option("--year", default=lambda: datetime.now().year, type=int, help="AoC Year")
@click.option("--day", default=lambda: datetime.now().day, type=int, help="AoC Day")
def main(year, day):
    """Create files for an AoC day."""
    console.log(f"Creating files for {year} day {day}")
    year = str(year)
    day = str(day)
    create_dirs(year)

    create_solution_file(year, day)
    create_test_file(year, day)


def create_dirs(year: str) -> None:
    """Create directories for files."""
    if not os.path.exists(ROOT_DIR / year):
        os.makedirs(ROOT_DIR / year)

    if not os.path.exists(init_file := ROOT_DIR / year / "__init__.py"):
        with open(init_file, "w"):
            pass

    if not os.path.exists(ROOT_DIR / "tests" / year):
        os.makedirs(ROOT_DIR / "tests" / year)

    init_file = ROOT_DIR / "tests" / year / "__init__.py"
    if not os.path.exists(init_file):
        with open(init_file, "w"):
            pass


def create_solution_file(year: str, day: str) -> None:
    """Create solution file if needed."""
    solution_file = ROOT_DIR / year / f"{day.zfill(2)}.py"
    template_file = ROOT_DIR / "templates" / "solution.py.j2"

    if os.path.exists(solution_file):
        return

    markdown = []
    lines = str.splitlines(get_markdown(year, day))
    for line in lines:
        markdown.extend(
            wrap(line, replace_whitespace=False, drop_whitespace=False)
        )
    problem_statement = "\n".join(markdown)

    with open(template_file) as template:
        template_renderer = Template(template.read())

    with open(solution_file, "w") as file:
        file.write(
            template_renderer.render(
                now=datetime.now(), problem=problem_statement, year=year, day=day
            )
        )


def create_test_file(year: int, day: int) -> None:
    """Create test file if needed."""
    test_file = ROOT_DIR / "tests" / year / f"{day.zfill(2)}.py"
    template_file = ROOT_DIR / "templates" / "test.py.j2"

    if os.path.exists(test_file):
        return

    with open(template_file) as template:
        template_renderer = Template(template.read())

    with open(test_file, "w") as file:
        file.write(template_renderer.render(now=datetime.now(), year=year, day=day))
    pass


if __name__ == "__main__":
    main()
