import os
from setuptools import setup, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

MACROS = [
    ("_FILE_OFFSET_BITS", "64"),
    ("_CRT_SECURE_NO_WARNINGS", ""),
]
if os.name == "nt":
    MACROS.append(("_WIN", ""))

SOURCES = ["pyumdreplace.c", "UMD-replace.c"]

def main():
    setup(name="pyumdreplace",
          version="0.1.0",
          author="Illidan",
          description="Python interface for UMD-replace.",
          long_description=long_description,
          long_description_content_type="text/markdown",
          url="https://github.com/Illidanz/pyumdreplace",
          classifiers=[
              "Programming Language :: Python :: 3",
              "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
          ],
          ext_modules=[Extension("pyumdreplace", SOURCES, define_macros=MACROS)]
        )

if __name__ == "__main__":
    main()
