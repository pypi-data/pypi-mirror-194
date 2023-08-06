import argparse
import os

from pymermaid2dir import __version__
from pymermaid2dir.vis import to_markdown


def main():
    parser = argparse.ArgumentParser(
        prog=os.path.basename(os.path.dirname(__file__)),
        description="pymermaid",
    )
    parser.add_argument("--folder", "-f", required=True, help="Input Root Folder")
    parser.add_argument("--output", "-o", required=True, help="Output Mode")
    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    input_root_folder = args.folder
    output_mode = args.output

    prety_str = to_markdown(input_root_folder, output=output_mode)

    return prety_str


if __name__ == "__main__":
    main()
