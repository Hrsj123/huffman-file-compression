import json

from .huffman_tree import HuffTree
from .utils import file_reader

class HuffmanFileSerializer:
    SEPARATOR = "---SEP---".encode("utf-8")  # Unique separator

    def __init__(self, filename: str, sep: str=None):
        self.filename = filename
        if sep is not None:
            if len(sep) <= 1:
                raise ValueError("Length of sep has to be greater than 1.")
            self.SEPARATOR = sep.encode("utf-8")
    
    def from_file(self, src_filename=None):
        text = "".join([i for i in file_reader(file_name=src_filename)])
        self.encode_and_write(text)

    def encode_and_write(self, text):
        """Encodes text using Huffman encoding and writes it to a binary file."""
        # Build character frequency
        char_freq = {char: text.count(char) for char in set(text)}

        # Create Huffman Tree and get encoding dictionary
        huffman_nodes = [HuffTree(e1=char, wt=wt) for char, wt in char_freq.items()]
        root = HuffTree.build_tree(huffman_nodes)
        encoding_dict = root.encoder()

        # Convert header (dictionary) to bytes
        bytes_header = root.get_bytes_dict()

        # Convert separator to bytes
        bytes_sep = self.SEPARATOR

        # Encode the text into bits
        encoded_bits = []
        for char in text:
            encoded_bits.extend(list(encoding_dict[char]))

        # Calculate extra padding bits for byte alignment
        extra_bits = (8 - len(encoded_bits) % 8) % 8
        bytes_extra_bits = extra_bits.to_bytes(1, byteorder="big")

        # Add padding bits and convert to bytes
        bytes_padding = list("0" * extra_bits)
        padded_encoded_list = [*bytes_padding, *encoded_bits]
        padded_bytes_encoded_str = bytes(int("".join(padded_encoded_list[i:i+8]), 2) for i in range(0, len(padded_encoded_list), 8))

        # Write everything to a binary file
        with open(self.filename, "wb") as file:
            file_data = bytes_header + bytes_sep + bytes_extra_bits + padded_bytes_encoded_str
            file.write(file_data)

        print(f"Encoded data written to {self.filename}")

    @classmethod
    def decode_from_file(cls, filename: str=None) -> str:
        """Reads the binary file, extracts encoded data, and decodes it back to a string."""
        file_bytes = None
        with open(filename, "rb") as file:
            file_bytes = file.read()

        # Locate separator and split
        bytes_sep = cls.SEPARATOR

        sep_index = file_bytes.find(bytes_sep)
        if sep_index == -1:
            raise ValueError("Separator not found in the file!")

        # Split header and encoded data
        header_bits = file_bytes[:sep_index]
        remaining_bits = file_bytes[sep_index + len(bytes_sep):]

        # Extract extra bits count & remove padded bits
        decoded_bits_list = []
        for byte in remaining_bits[1:]:
            decoded_bits_list.extend(list(format(byte, '08b')))
        extra_bits = int.from_bytes(remaining_bits[:1])
        decoded_bits_list = decoded_bits_list[extra_bits:]

        # Decode header
        parsed_data = json.loads(header_bits.decode("utf-8"))

        # Decode Huffman-encoded content
        decoded_text = HuffTree.decoder(decoded_bits_list, d=parsed_data)

        return decoded_text
