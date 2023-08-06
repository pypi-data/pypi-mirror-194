from setuptools import find_packages, setup

REPO_URL = "https://github.com/jaichel/excursor"

with open("README.md") as file:
    long_description = file.read()

setup(
    name="excursor",
    version="0.1.0",
    author="Joshua Lusk",
    author_email="luskjh@gmail.com",
    description="Trading bot.",
    long_description=long_description,
    packages=find_packages(include="excursor"),
    install_requires=[],
    python_requires=">=3.11",
    entry_points={"console_scripts": ["excursor=excursor.console:run"]},
    license="BSD",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3.11",
    ],
    url="https://github.com/jaichel/excursor",
    keywords="trading bot",
    project_urls={
        "Source": REPO_URL,
        "Tracker": f"{REPO_URL}/issues",
    },
)
