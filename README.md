# Huffman File Compression

A CLI tool to compress and decompress files using Huffman Compression.

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

The CLI tool provides two main functionalities:

### Compress a File

To compress a file using Huffman encoding:

```sh
huffman-compress <file_path>
```

This creates a new compressed file in the same directory.

### Decompress a File

To decompress a previously compressed file:

```sh
huffman-compress -u <file_path>
```

This restores the original file from the compressed version.

## How It Works

- The tool constructs a **Huffman Tree** based on character frequencies in the input file.
- It encodes the file using **Huffman coding**, storing the encoding dictionary.
- The decompression reverses the process to restore the original content.

## Requirements

- **Python Version**: 3.11.9
- No external dependencies
