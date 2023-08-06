#!/usr/bin/env python3

import argparse
import sys
from typing import List

from .merger import get


def parse_args(command_line: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", help="The source file", required=True)
    parser.add_argument("--dest", help="The destination file", required=True)
    parser.add_argument(
        "--update", help="Update values?", default=False, action="store_true"
    )

    return parser.parse_args(command_line)


def main():
    args = parse_args(sys.argv[1:])

    with open(args.source, "rb") as source_file:
        source = source_file.read()

    with open(args.dest, "rb") as dest_file:
        dest = dest_file.read()

    merger = get(source, dest)
    output_data = merger(source, dest, args.update)

    with open(args.dest, "wb") as dest_file:
        dest_file.write(output_data)


if __name__ == "__main__":
    main()
