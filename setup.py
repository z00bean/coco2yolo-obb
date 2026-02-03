#!/usr/bin/env python3
"""Setup script for coco2yolo-obb package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Read requirements
requirements = (this_directory / "requirements.txt").read_text().strip().split('\n')

setup(
    name="coco2yolo-obb",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Convert COCO segmentation annotations to YOLO Oriented Bounding Box format",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/z00bean/coco2yolo-obb",
    py_modules=["coco2yolo_obb"],
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "coco2yolo-obb=coco2yolo_obb:main",
        ],
    },
    keywords="coco yolo obb oriented bounding box computer vision annotation conversion",
    project_urls={
        "Bug Reports": "https://github.com/z00bean/coco2yolo-obb/issues",
        "Source": "https://github.com/z00bean/coco2yolo-obb",
        "Documentation": "https://github.com/z00bean/coco2yolo-obb#readme",
    },
)