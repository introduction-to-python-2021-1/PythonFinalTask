"""Remove all files in the `build` and `dist` directories."""

from pathlib import Path
from shutil import rmtree


def main() -> None:
    """Remove files created by ``setup.py``."""
    root = Path(__file__).parents[1].resolve()

    for dir_name in {"build", "dist"}:
        rmtree(root / dir_name, ignore_errors=True)


if __name__ == "__main__":
    main()
