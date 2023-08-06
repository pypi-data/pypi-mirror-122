import setuptools

with open("README.md", "r", encoding='UTF-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcalive", # Replace with your own username
    version="0.0.3",
    author="SZI",
    description="Arcalive Loader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)