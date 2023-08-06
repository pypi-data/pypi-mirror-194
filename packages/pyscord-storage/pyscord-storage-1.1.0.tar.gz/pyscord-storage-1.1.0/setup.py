from setuptools import find_packages, setup

setup(
    name="pyscord-storage",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    author="Arter Tendean",
    author_email="arter@animemoe.us",
    description="Free unlimited file hosting using Discord server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/animemoeus/pyscord-storage",
    license="MIT",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
    ],
)
