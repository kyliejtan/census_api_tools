import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="census_api_tools",
    version="0.0.1",
    author="Kylie Jun-Di Tan",
    author_email="kyliejtan@gmail.com",
    description="A package containing tools to make gathering data from US Census Bureau API's easier.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kyliejtan/census_api_tools",
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
