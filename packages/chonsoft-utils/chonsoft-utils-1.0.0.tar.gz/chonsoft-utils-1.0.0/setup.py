from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent
README = (HERE / 'README.md').read_text()

# This call to setup() does all the work
setup(
    name="chonsoft-utils",
    version="1.0.0",
    description="chonsoft utils package",
    long_description=README,
    long_description_content_type="text/markdown",
    url="",
    author="chonsoft",
    author_email="chonsoft@hotmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["pkg"],
    include_package_data=True,
    install_requires=[],
    entry_points={
        "console_scripts": [
            "chonsoft=pkg.__main__:main",
        ]
    },
)
