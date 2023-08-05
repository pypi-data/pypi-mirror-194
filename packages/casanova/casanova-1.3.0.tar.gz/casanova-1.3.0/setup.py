from setuptools import setup, find_packages

with open("./README.md", "r") as f:
    long_description = f.read()

setup(
    name="casanova",
    version="1.3.0",
    description="Specialized & performant CSV readers, writers and enrichers for python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://github.com/medialab/casanova",
    license="MIT",
    author="Guillaume Plique",
    author_email="kropotkinepiotr@gmail.com",
    keywords="csv",
    python_requires=">=3.7",
    packages=find_packages(exclude=["benchmark", "test"]),
    package_data={"docs": ["README.md"]},
    install_requires=["ebbe>=1.11.0,<2", "file-read-backwards>=2.0.0,<3"],
    extras_require={"http": ["urllib3", "certifi"]},
    zip_safe=True,
)
