from .huffman_file_serializer import HuffmanFileSerializer
from .utils import file_reader, cli_argument_parser
import os

def main():     # TODO: Instead of throwing error -> Use msg and exit code...
    src_file_name, deserialize, dest_folder = cli_argument_parser()

    if not os.path.isfile(src_file_name):
        raise ValueError("Invalida source file provided")
    if dest_folder is not None:
        if not os.path.isdir(dest_folder):
            raise ValueError("Invalid destination folder provided")
    else:
        dest_folder = "./"
    
    # fix path:
    src_file_name = os.path.normpath(src_file_name)
    dest_folder = os.path.normpath(dest_folder)
    
    base_name = os.path.splitext(os.path.basename(src_file_name))[0]
    if deserialize:
        # Decode
        decoded_text = HuffmanFileSerializer.decode_compress_file(src_file_name)
        with open(os.path.join(dest_folder, f"{base_name}-uncompressed.txt"), "w") as file:
            file.write(decoded_text)
    else:
        # Encode
        dest_file = os.path.join(os.getcwd(), os.path.join(dest_folder, f"{base_name}-compressed.txt"))
        obj = HuffmanFileSerializer(src_file_name)
        obj.compress_file(dest_file)
