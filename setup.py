from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="claudius",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A terminal UI for managing .claudeignore files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/claudius",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "textual>=3.0.1",
    ],
    entry_points={
        "console_scripts": [
            "claudius=claudius.main:main",
        ],
    },
)
