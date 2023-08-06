import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="nextrade",
    version="0.1.4",
    author="fs",
    author_email="master@finterstellar.com",
    description="Trade volume analysis tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/finterstellar/library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'numpy',
        'pandas',
        'requests',
        'plotly',
    ],
    python_requires='>=3.7',
)