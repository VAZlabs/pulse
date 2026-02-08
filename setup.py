#!/usr/bin/env python3
"""
Setup script for pulse - Advanced Network Diagnostics Tool
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="pulse-network-diagnostics",
    version="2.0.0",
    author="pulse-team",
    author_email="pulse@example.com",
    description="Advanced async network diagnostics tool - Check DNS → TCP → TLS → HTTP chain",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vazor-code/pulse",
    packages=find_packages(),
    include_package_data=True,
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
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet",
        "Topic :: System :: Networking",
        "Topic :: System :: Systems Administration",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "black>=23.7.0",
            "flake8>=6.0.0",
            "mypy>=1.5.0",
            "isort>=5.12.0",
        ],
        "yaml": ["PyYAML>=6.0"],
        "dns": ["dnspython>=2.3.0"],
    },
    entry_points={
        "console_scripts": [
            "pulse=pulse:main",
        ],
    },
)
