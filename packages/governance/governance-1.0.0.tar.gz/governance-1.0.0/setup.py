from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="governance",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package for submitting data to an API endpoint",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/governance",
    packages=["governance"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
