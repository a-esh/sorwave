from setuptools import setup, find_packages 
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="sorwave",
    version="0.0.2",
    author="a-esh",
    author_email="abrahamescalona@live.com",
    description="Music Sorter based on Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/a-esh/sorwave",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6", 
    install_requires=[
        "requests>=2.25.1",
        "mutagen>=1.45.1"
    ],
    entry_points={  
        "console_scripts": [
            "sorwave=sorwave.main:main",
        ],
    },
    include_package_data=True,
)
