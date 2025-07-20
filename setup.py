#!/usr/bin/env python3
"""
Setup script for CrowdStrike Correlation Rules Backup Tool
"""
from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crowdstrike-correlation-rules-backup",
    version="1.0.0",
    author="CrowdStrike Correlation Rules Backup Tool",
    author_email="1B05H1N@pm.me",
    description="A Python tool for backing up CrowdStrike correlation rules using the Falcon API",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="",
    packages=find_packages(),
    py_modules=["cli", "config"],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: System Administrators",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: System :: Systems Administration",
        "Topic :: Security",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "crowdstrike-backup=cli:cli",
        ],
    },
    zip_safe=False,
    keywords="crowdstrike, falcon, api, backup, correlation, rules, security",
    project_urls={
        "Bug Reports": "",
        "Source": "",
        "Documentation": "https://www.falconpy.io/",
    },
) 