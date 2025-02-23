import json
from bitarray import bitarray
from huffman_serializer import HuffTree

class EncodedFile:
    SEPARATOR = "---SEP---".encode("utf-8")  # Unique separator

    def __init__(self, filename):
        self.filename = filename

    def encode_and_write(self, text):
        """Encodes text using Huffman encoding and writes it to a binary file."""
        # Step 1: Build character frequency
        char_freq = {char: text.count(char) for char in set(text)}

        # Step 2: Create Huffman Tree and get encoding dictionary
        huffman_nodes = [HuffTree(e1=char, wt=wt) for char, wt in char_freq.items()]
        root = HuffTree.build_tree(huffman_nodes)
        encoding_dict = root.encoder()

        # Step 3: Convert header (dictionary) to bytes
        bytes_header = bitarray()
        header_json = root.get_bytes_dict()
        bytes_header.frombytes(header_json)

        # Step 4: Convert separator to bytes
        bytes_sep = bitarray()
        bytes_sep.frombytes(self.SEPARATOR)

        # Step 5: Encode the text into bits
        encoded_bits = bitarray()
        for char in text:
            encoded_bits.extend(encoding_dict[char])

        # Step 6: Calculate extra padding bits for byte alignment
        extra_bits = (8 - len(encoded_bits) % 8) % 8
        bytes_extra_bits = bitarray()
        bytes_extra_bits.frombytes(extra_bits.to_bytes(1, byteorder="big"))

        # Step 7: Add padding bits and convert to bytes
        bytes_padding = bitarray("0" * extra_bits)
        bytes_encoded_str = bitarray()
        bytes_encoded_str.frombytes(bytes_padding + encoded_bits)

        # Step 8: Write everything to a binary file
        with open(self.filename, "wb") as file:
            file_data = bytes_header + bytes_sep + bytes_extra_bits + bytes_encoded_str
            file_data.tofile(file)

        print(f"Encoded data written to {self.filename}")

    def decode_from_file(self):
        """Reads the binary file, extracts encoded data, and decodes it back to a string."""
        with open(self.filename, "rb") as file:
            bits_read = bitarray()
            bits_read.fromfile(file)

        # Step 1: Locate separator and split
        bytes_sep = bitarray()
        bytes_sep.frombytes(self.SEPARATOR)

        sep_index = bits_read.find(bytes_sep)
        if sep_index == -1:
            raise ValueError("Separator not found in the file!")

        # Split header and encoded data
        header_bits = bits_read[:sep_index]
        remaining_bits = bits_read[sep_index + len(bytes_sep):]

        # Step 2: Extract extra bits count
        extra_bits = int.from_bytes(remaining_bits[:8].tobytes(), "big")
        decoded_bits = remaining_bits[8 + extra_bits:]  # Remove padding bits

        # Step 3: Decode header
        parsed_data = json.loads(header_bits.tobytes().decode("utf-8"))

        # Step 4: Decode Huffman-encoded content
        decoded_text = HuffTree.decoder(decoded_bits, d=parsed_data)

        return decoded_text
