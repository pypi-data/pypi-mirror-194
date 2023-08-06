import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


classifiers = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Developers",
    "Topic :: Software Development :: Libraries",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
]

install_requires = [
    "ipywidgets>=8.0.4,<9.0"
]

setup(
    name="nbinspector",
    version="0.1",
    author="Michael Wharton",
    author_email="mwharton3@protonmail.com",
    description=("Tool to help inspect arbitrary objects in Jupyter notebooks"),
    url="https://github.com/mwharton3/nbinspector",
    packages=find_packages(),
    include_package_data=True,
    download_url="https://github.com/mwharton3/nbinspector/archive/0.1.tar.gz",
    install_requires=install_requires,
    classifiers=classifiers,
    zip_safe=False,
)
