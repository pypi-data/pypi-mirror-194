import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="librarypy",
    version="0.0.1",
    author="IO Teknikk",
    author_email="mr.edwin74@gmail.com",
    description="LibraryPy is a Python library built for Python 3.11.0.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IO-Teknikk/LibraryPy",
    project_urls={
        "Bug Tracker": "https://github.com/IO-Teknikk/LibraryPy/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.11"
)
