#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Setup script for Advanced Calculator
Creates an executable for Windows
"""

from setuptools import setup, find_packages
import sys
import os

# Read README for long description
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="AdvancedCalculator",
    version="1.0.0",
    author="Fady Shehata",
    author_email="fady-shehata0@example.com",
    description="A bilingual calculator with NVDA screen reader support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fady-shehata0/CalcForBlind",
    license="MIT",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Natural Language :: English",
        "Natural Language :: Arabic",
        "Topic :: Multimedia",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: People with Disabilities",
    ],
    python_requires=">=3.8",
    install_requires=[
        "wxPython>=4.1.0",
    ],
    entry_points={
        "gui_scripts": [
            "advanced-calculator=calculator:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
