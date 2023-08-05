import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cracklib-pkg",
    version="0.0.1",
    author="glitch_prog",
    author_email="glitch_prog@mail.com",
    description="A hash cracker package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/tsy7/cracklib.git",
    project_urls={
        "Bug Tracker": "https://github.com/tsy7/cracklib.git/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
