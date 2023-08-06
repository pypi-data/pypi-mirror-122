# [PDS toolbox] setup package:
# python setup.py sdist bdist_wheel
# twine upload dist/*

import setuptools

with open("README.md","r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "pdstoolbox",
    version = "0.0.5",
    author = "TQ",
    author_email="tqin0411@outlook.com",
    description = "code-testing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/QinYu211/pds",
    packages=setuptools.find_packages(),
    install_requires=['pandas','matplotlib','numpy'],
    # add any additional packages that needs to be installed along with pdstoolbox package.

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)

