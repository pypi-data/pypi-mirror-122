import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dotdata",
    version="0.0.1",
    author="dotData, Inc.",
    author_email="info@dotdata.com",
    description="dotData package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://dotdata.com/",
    project_urls={},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.6",
)
