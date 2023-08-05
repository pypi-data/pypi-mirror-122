from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="kgcl",  # this is what we pip install (the name under pypi)
    version="0.0.1",
    description="Knowledge Graph Change Language",
    packages=[
        "apply",
        "diff",
        "grammar",
        "model",
    ],
    py_modules=[
        "kgcl",
        "kgcl_diff",
        "pretty_print_kgcl",
    ],  # list of python code modules - this is the code I want to distribute (this is what people import - not what they pip-install)
    package_dir={"": "kgcl"},
    classifiers=[
        "Programming Language :: Python :: 3.8",
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "linkml ~= 1.0.3",
        "rdflib >= 5.0.0",
        "lark >= 0.11.3",
        "click >= 7.1.2",
    ],
    extras_require={"dev": ["pytest>=3.7"]},
    url="https://github.com/ckindermann/knowledge-graph-change-language",
    author="Christian Kindermann",
    author_email="chris.kind.man@gmail.com",
),
