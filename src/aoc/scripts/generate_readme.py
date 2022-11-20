#!/usr/bin/env python

import re

import rich_click as click
from aoc.utils.console import console
from aocd.models import default_user

from aoc import ROOT_DIR


@click.command()
def main():
    total_stars = get_stars()
    console.log("Updating images")
    _update_stars_in_image(total_stars)
    console.log("Updating readme")

    readme_file = ROOT_DIR.parent.parent / "README.md"

    with open(readme_file) as f:
        current_readme = f.read()

    readme = _update_stars(current_readme, total_stars)

    with open(readme_file, "w") as f:
        f.write(readme)


def get_stars():
    """Retrieve number of stars."""
    u = default_user()
    stats = u.get_stats()
    total_stars = 0
    for entry, results in stats.items():
        stars = len(results)
        total_stars += stars
    return total_stars


def _update_stars(readme: str, star_count: int) -> str:
    return re.sub(
        pattern=r"&message=\d+",
        repl=f"&message={star_count}",
        string=readme,
        flags=re.DOTALL,
    )


def _replace_between_tags(string: str, content: str, start: str, end: str) -> str:
    """Replace a string between tags."""
    content = "\n".join([start, content, end])

    return re.sub(
        pattern=rf"{start}.*?{end}",
        repl=content,
        string=string,
        flags=re.DOTALL,
    )


def _update_stars_in_image(star_count: int) -> None:
    """Update star counts in svg image."""
    images = ("image_dark.svg", "image_light.svg")
    image_path = ROOT_DIR.parent.parent
    content = f'				<span class="star-count">{star_count}</span>'

    for image in images:
        image_file = image_path / image
        with open(image_file) as f:
            svg_content = f.read()

        svg_content = _replace_between_tags(
            svg_content, content, "<!-- start star count -->", "<!-- end star count -->"
        )

        with open(image_file, "w") as f:
            f.write(svg_content)


if __name__ == "__main__":
    main()
