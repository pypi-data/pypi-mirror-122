import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

requirements = []

setuptools.setup(
        name="testpag",
        version="0.0.1",
        author="Pavel P.",
        author_email="pasha228@gmail.com",
        description="Some description",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/friedwok",
        packages=setuptools.find_packages(),
        install_requires=requirements,
        classifiers=[
            "Programming Language :: Python :: 3.8",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires='>=3.6',
    )
