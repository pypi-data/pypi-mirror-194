from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="governance",
    version="1.2.0",
    author="Ramsay Brown",
    author_email="ramsay@airesponsibilitylab.com",
    description="Automate AI Governance requirements by connecting your python notebooks directly to the Mission Control MLOps platform.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/airesponsibilitylab/governance_pip",
    packages=["governance"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
