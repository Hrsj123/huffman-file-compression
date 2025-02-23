from .huffman_file_serializer import HuffmanFileSerializer
from .utils import file_reader, cli_argument_parser
import os

def main():
    file_name, deserialize = cli_argument_parser()
    if deserialize:
        # Decode
        decoded_text = HuffmanFileSerializer.decode_from_file(file_name)
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        with open(f"{base_name}-uncompressed.txt", "w") as file:
            file.write(decoded_text)
    else:
        # Encode
        base_name = os.path.splitext(os.path.basename(file_name))[0]
        dest_file = os.path.join(os.getcwd(), f"{base_name}-compressed.txt")
        obj = HuffmanFileSerializer(dest_file)
        text = "".join([i for i in file_reader(file_name)])
        obj.encode_and_write(text)
