import argparse
from pathlib import Path
from .FolderGenie import FolderGenie

def foldergenie():
    parser = argparse.ArgumentParser()
    parser.add_argument("source_file_path")
    args = parser.parse_args()

    source_file = Path(args.source_file_path)

    if not source_file.exists():
        print('The source file does not exist')
        raise SystemExit(1)

    # Generate the folders using the input file
    genie = FolderGenie(source_file)
    genie.generate_folders()