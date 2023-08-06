import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent

# README = (HERE / "README.md").read_text()

setup(
    name="caspius",
    version="1.0.0",
    description="Easy logging system",
    long_description="Logging system which can show timestamp, "
                     "paint logs by your colors and handle every log by your functions",
    long_description_content_type="text/markdown",
    url="https://github.com/dangost/caspius",
    keywords=["python", "logger", "logging", "caspius"],
    author="dangost",
    author_email="dangost16@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    packages=[],
    include_package_data=True,
    install_requires=[],
)