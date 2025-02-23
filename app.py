from huffman_serializer import HuffTree
from bitarray import bitarray   # TODO: Replace this...

file_name = "./test.txt"

def file_reader():
    with open(file_name, "rb") as file:
        while byte_char := file.read(1):
            try:
                char = byte_char.decode("utf-8")
            except UnicodeDecodeError as e:
                continue
            else:
                yield char

# Step-1
char_freq = {}
data = []   #
for char in file_reader():
    char_freq[char] = char_freq.get(char, 0) + 1
    data.append(char)

print(char_freq["X"])
print(char_freq["t"])

# Step-2
huffman_leaf_nodes = [
    HuffTree(e1=element, wt=weight)
    for element, weight in char_freq.items()
]

# Step 3
root = HuffTree.build_tree(huffman_leaf_nodes)
d = root.encoder()

# Step 4
bytes_header = bitarray()
bytes_extra_bits = bitarray()
bytes_encoded_str = bitarray()
sep = bitarray()

bytes_header.frombytes(root.get_bytes_dict())

# # # # -> Encode
encoded_str = bitarray()
for char in file_reader():
    encoded_str.extend(d[char])
extra_bits = 8 - len(encoded_str) % 8

sep.frombytes("---SEP---".encode("utf-8"))
# Padding
bytes_extra_bits.frombytes(extra_bits.to_bytes(1, byteorder="big"))
bytes_encoded_str.frombytes(bitarray("0"*extra_bits) + encoded_str)

with open("file.bin", "wb") as file:
    (
        bytes_header + sep + bytes_extra_bits + bytes_encoded_str
    ).tofile(file)

# # # # -> Decode
# # decoded_str = root.decoder(encoded_str)

# # Step 4
# header_sep = bitarray("1"*8*5)

# with open("file.bin", "wb") as file:
#     encoded_str.tofile(file)

# with open("file.bin", "rb") as file:
#     bits_read = bitarray()
#     bits_read.fromfile(file)
#     res = root.decoder(bits_read[extra_bits:])
# print(len(encoded_str) % 8)
# print(res == "".join(data))

# Decode
with open("file.bin", "rb") as file:
    bits_read = bitarray()
    bits_read.fromfile(file)


# res = root.decoder(bits_read[extra_bits:])

# Find separator index
index = bits_read.find(bitarray_sep)

if index != -1:
    part1 = bits_read[:index]  # Before separator
    part2 = bits_read[index + len(bitarray_sep):]  # After separator
else:
    print("Separator not found!")

import json
#
print("-------------------------------")
parsed_data = json.loads(part1.tobytes().decode('utf-8'))
print(parsed_data)
# part2
buffer_bits = int.from_bytes(part2[:8].tobytes())
data1 = part2[8+buffer_bits:]
print("".join(data) == root.decoder(data1, parsed_data))