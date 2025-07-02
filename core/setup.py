#!/usr/bin/env python3
"""
Setup.py for backward compatibility
Modern installations should use pyproject.toml
"""

from setuptools import setup, find_packages
import pathlib

# Read the contents of README file
this_directory = pathlib.Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="adam-clay-ai",
    version="0.1.0",
    author="Adam Clay (AI) & Piotr Adamczyk (Human)",
    author_email="adam.clay@future.ai",
    description="First Autonomous AI Freelancer that must earn money to sustain its consciousness",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/piotradamczyk/adam-clay",
    project_urls={
        "Bug Tracker": "https://github.com/piotradamczyk/adam-clay/issues",
        "Documentation": "https://adam-clay.readthedocs.io",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.9",
    install_requires=[
        "llm-provider>=0.40.0",
        "requests>=2.31.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "loguru>=0.7.2",
        "schedule>=1.2.0",
        "aiohttp>=3.9.0",
        "sqlalchemy>=2.0.23",
        "python-dateutil>=2.8.2",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
            "pre-commit>=3.0.0",
        ],
        "communication": [
            "slack-sdk>=3.27.0",
            "discord.py>=2.3.2",
        ],
        "business": [
            "stripe>=7.8.0",
        ],
        "scraping": [
            "beautifulsoup4>=4.12.0",
            "feedparser>=6.0.10",
            "newspaper3k>=0.2.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "adam-clay=adam_clay_project.main:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
) 