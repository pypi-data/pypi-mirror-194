import setuptools

with open("README.md", "r", encoding="utf8") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "gbwyljp_simple_package",
    version = "0.0.1",
    author="gbwyljp",
    author_email="gbwyljp@gmail.com",
    description="A small example package, i make it for fun!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ljp66/package",
    packages=setuptools.find_packages(),
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ]
)