import os
import setuptools

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name = "unitscvt",
    version = "0.0.22",
    author = "Lucas Borges",
    author_email = "lucas.borges@fysik.su.se",
    description = ("SI constants and convertion rates to Atomic units"),
    license = "MIT",
    keywords = "units",
    url = "https://gitlab.fysik.su.se/lucas.borges/unitsconversion",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Topic :: Utilities",
    ],
    python_requires='>=3.6',
)
