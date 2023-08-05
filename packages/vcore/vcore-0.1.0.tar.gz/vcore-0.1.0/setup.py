from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name="vcore",
    packages=find_packages(),
    version="0.1.0",
    description="Venus internal data crawling",
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
