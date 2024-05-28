from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="SongManager",
    version="0.0.1",
    author="a-esh",
    author_email="abrahamescalona@gmail.com",
    description="Music Sorter based on Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-esh/SongManager",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", 
    install_requires=[
        "requests>=2.25.1",
        "pandas>=1.2.3",
        "mutagen>=1.45.1"
    ],
    entry_points={  
        "console_scripts": [
            "SongManager=src.main:main",
        ],
    },
    include_package_data=True,
)
