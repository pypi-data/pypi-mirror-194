"""
Donut
Copyright (c) 2022-present NAVER Corp.
MIT License
"""
import os
from glob import glob
from setuptools import find_packages, setup

ROOT = os.path.abspath(os.path.dirname(__file__))


def read_version():
    data = {}
    path = os.path.join(ROOT, "synthdog", "_version.py")
    with open(path, "r", encoding="utf-8") as f:
        exec(f.read(), data)
    return data["__version__"]


def read_long_description():
    path = os.path.join(ROOT, "README.md")
    with open(path, "r", encoding="utf-8") as f:
        text = f.read()
    return text


setup(
    name="synthdog",
    version="0.0.4",#read_version(),
    description="Customized synthdog package from donut-python project",
    long_description=read_long_description(),
    long_description_content_type="text/markdown",
    author="ML Team",
    author_email="",
    url="https://github.com/bilykigor/synthdog.git",
    license="MIT",
    packages=find_packages(
        exclude=[
            "config",
            "dataset",
            "misc",
            "result",
            "donut",
            "app.py",
            "lightning_module.py",
            "README.md",
            "train.py",
            "test.py",
            "deploy.sh"
        ]
    ),
    py_modules=[os.path.splitext(os.path.basename(path))[0] for path in glob("synthdog/*.py")],
    include_package_data=True,
    python_requires=">=3.7",
    install_requires=[
    ],
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
