from .huffman_file_serializer import HuffmanFileSerializer
from .utils import file_reader, cli_argument_parser
import os

def main():
    file_name, deserialize = cli_argument_parser()
    dest_file = os.path.join(os.getcwd(), f"{file_name.split('.')[0]}-compressed.txt")
    obj = HuffmanFileSerializer(dest_file)
    if deserialize:
        # Decode
        decoded_text = obj.decode_from_file(file_name)
        with open(f"{file_name.split('.')[0]}-uncompressed.txt", "w") as file:
            file.write(decoded_text)
    else:
        # Encode
        text = "".join([i for i in file_reader(file_name)])
        obj.encode_and_write(text)
