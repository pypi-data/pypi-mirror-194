import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup_info = {
    "name": "aspose_compressor",
    "version": "0.0.3",
    "author": "CantCode023",
    "author_email": "cantcode023@gmail.com",
    "description": "Compress video with 100% compress size and no quality loss with only 3 lines of code.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "url": "https://github.com/CantCode023/aspose_compressor",
    "packages": setuptools.find_packages(),
    "install_requires": ["requests", "urllib3"],
    "classifiers": [
        "Programming Language :: Python :: 3",
    ],
    "python_requires": '>=3.7'
}


setuptools.setup(**setup_info)