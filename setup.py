#!/usr/bin/python3
from setuptools import setup, find_packages, Extension
from pathlib import Path
from Cython.Build import cythonize

_SRC = Path(__file__).parent.absolute() / "nlp"


def get_extensions():
    exts = _SRC.glob("**/*.pyx")
    return list(map(str, exts))


compiler_directives = dict(
    language_level=3,
)

extensions = cythonize(
    get_extensions(),
    compiler_directives=compiler_directives,
)

setup(
    name="nlp",
    version="0.0.1",
    ext_modules=extensions,
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "nlp": [
            "**/*.toml", "**/*.yml",
            "**/.*yaml", "**/*.txt",
            "**/*.json", "**/*.pxd",
            "**/*.pyx",
        ],
    },
    zip_safe=False,
)
