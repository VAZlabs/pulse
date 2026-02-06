#!/usr/bin/env python3
"""
Setup script for pulse - network diagnostics tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pulse-network-diagnostics",
    version="1.0.0",
    author="VAZlabs",
    author_email="vazorcode@gmail.com",
    description="Network diagnostics in 3 seconds - Check DNS → TCP → TLS → HTTP chain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/VAZlabs/pulse",
    py_modules=["pulse"],
    include_package_data=False,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Internet",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "pulse=pulse:main",
        ],
    },
)
