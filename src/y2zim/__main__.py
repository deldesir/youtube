import pathlib
import sys


def main():
    # allows running it from source
    sys.path = [str(pathlib.Path(__file__).parent.parent.resolve())] + sys.path

    from y2zim.entrypoint import main as entry

    return entry()


if __name__ == "__main__":
    sys.exit(main())