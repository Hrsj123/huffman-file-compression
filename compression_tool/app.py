from .huffman_file_serializer import HuffmanFileSerializer
from .utils import file_reader, cli_argument_parser
import os
import sys

def main():
    src_file_name, deserialize, dest_folder = cli_argument_parser()

    if not os.path.isfile(src_file_name):
        print("Error: Invalid source file provided.")
        sys.exit(1)
    if dest_folder is not None:
        if not os.path.isdir(dest_folder):
            print("Error: Invalid destination folder provided.")
    else:
        dest_folder = "./"
    
    # fix path:
    src_file_name = os.path.normpath(src_file_name)
    dest_folder = os.path.normpath(dest_folder)
    
    base_name = os.path.splitext(os.path.basename(src_file_name))[0]
    if deserialize:
        # Decode
        try:
            decoded_text = HuffmanFileSerializer.decode_compress_file(src_file_name)
        except ValueError as e:
            print(f"Error: {str(e)}")
        with open(os.path.join(dest_folder, f"{base_name}-uncompressed.txt"), "w") as file:
            file.write(decoded_text)
    else:
        # Encode
        dest_file = os.path.join(os.getcwd(), os.path.join(dest_folder, f"{base_name}-compressed.txt"))
        obj = HuffmanFileSerializer(src_file_name)
        obj.compress_file(dest_file)
