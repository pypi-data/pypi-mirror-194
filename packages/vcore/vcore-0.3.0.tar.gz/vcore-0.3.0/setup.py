from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vcore",
    packages=find_packages(),
    version="0.3.0",
    description="Venus internal data crawling",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        "web3",
        "numpy",
        "pandas",
        "tqdm",
        "web3_multicall",
        "retrying",
        "requests",
    ],
    author="Aditya Rout",
    license="",
)
