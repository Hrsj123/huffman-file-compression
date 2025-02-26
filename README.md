# Huffman File Compression

A CLI tool and Python package to compress and decompress files using Huffman Compression.

## Installation

To install the package, clone the repository:

```sh
$ git clone https://github.com/Hrsj123/huffman-file-compression.git
$ cd huffman-file-compression
$ pip install huffman-compression
```

### Install in Development Mode

To install the package in development mode, run:

```sh
$ pip install -e .
```

## Usage

The tool provides two main ways to use Huffman compression: as a **CLI tool** and as a **Python package**.

### CLI Usage

#### Compress a File

To compress a file using Huffman encoding:

```sh
huffman-compress <file_path>
```

This creates a new compressed file in the same directory.

#### Decompress a File

To decompress a previously compressed file:

```sh
huffman-compress -u <file_path>
```

This restores the original file from the compressed version.

#### Specify Destination File (Optional Parameter)

To specify a destination file for compression:

```sh
huffman-compress -d <dest_file> <src_file>
```

To specify a destination file for decompression:

```sh
huffman-compress -ud <dest_file> <src_file>
```

### Using as a Python Package

You can also use Huffman compression programmatically in Python.

```python
from compression_tool import HuffmanFileSerializer

# Initialize with source file
obj = HuffmanFileSerializer("./test/test.txt")

# Compress file
obj.compress_file("./test/test-compressed.txt")

# Decompress file
data = HuffmanFileSerializer.decode_compress_file("./test/test-compressed.txt")
```

## How It Works

- The tool constructs a **Huffman Tree** based on character frequencies in the input file.
- It encodes the file using **Huffman coding**, storing the encoding dictionary.
- The decompression reverses the process to restore the original content.

## Requirements

- **Python Version**: 3.11.9
- No external dependencies

