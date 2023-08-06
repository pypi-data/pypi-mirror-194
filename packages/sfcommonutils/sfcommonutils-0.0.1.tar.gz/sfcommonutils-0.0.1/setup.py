import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

requires = [
    "requests>=2.23.0",
    "PyYAML>5.3",
    "mergedict>=1.0.0"
]

setuptools.setup(
    name="sfcommonutils",
    version="0.0.1",
    author="johnson",
    author_email="",
    description="A set of lightweight utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requires,
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
