import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-ds",
    version="1.0.0",
    author="parth parikh",
    author_email="subzero23@sudomail.com",
    description="No non-sense solutions to common Data Structure and Algorithm interview questions in Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prabhupant/python-ds",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)