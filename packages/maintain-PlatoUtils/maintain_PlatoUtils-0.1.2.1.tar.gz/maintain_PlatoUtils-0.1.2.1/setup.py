import setuptools
from setuptools import setup

NAME="maintain_PlatoUtils"
VERSION="0.1.2.1"
PY_MODULES=["src.maintain_PlatoUtils.maintain_PlatoUtils"]

with open("README.md", "r",encoding="utf8") as fh:
    long_description = fh.read()

setup(
    name=NAME,
    version=VERSION,
    url='https://github.com/Timaos123/maintian_PlatoUtils.git',
    license='MIT',
    author='Timaos',
    author_email='201436009@uibe.edu.cn',
    description='运营PlatoDB的工具',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=['numpy',"nebula-python","pandas"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.0',
)