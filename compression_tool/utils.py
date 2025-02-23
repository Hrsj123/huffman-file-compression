import argparse
from typing import Iterator

FILEPATH = "."
DESCRIPTION = "A command-line utility for generating a compressed file from an input file using Huffman Compression."
EPILOG = f'{"-" *(len(DESCRIPTION) // 2 - 2)} END {"-" *(len(DESCRIPTION) // 2 - 2)}'

def file_reader(file_name: str) -> Iterator[str]:
    with open(file_name, "rb") as file:
        while byte_char := file.read(1):
            try:
                char = byte_char.decode("utf-8")
            except UnicodeDecodeError as e:
                continue
            else:
                yield char

def cli_argument_parser() -> str:
    parser = argparse.ArgumentParser(
        prog="huffman-compress",
        description=DESCRIPTION,
        epilog=EPILOG,
    )

    parser.add_argument(FILEPATH, help="The path where the file exists")
    parser.add_argument("-u", "--uncompress", action="store_true", help="Deserialize encoded file.")
    args = parser.parse_args()

    file_path = vars(args)[FILEPATH]
    
    return (file_path, args.uncompress)
