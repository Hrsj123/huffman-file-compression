from setuptools import find_packages, setup

setup(
    name="huffman-compression",
    version="0.0.1",
    packages=find_packages(),
    # install_requires=[],
    entry_points={
        "console_scripts": [
            "huffman-compress=compression_tool.app:main",
        ]
    },
)
