from file_bytes_io import EncodedFile

obj = EncodedFile("file.txt")

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

text = "".join([i for i in file_reader()])
obj.encode_and_write(text)
decoded_text = obj.decode_from_file()
print(text == decoded_text)
