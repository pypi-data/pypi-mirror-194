import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="stopywatch",
    version="1.0.0",
    author="Jesus Alejandro Sanchez Davila",
    author_email="jsanchez.consultant@gmail.com",
    description="Simple Python 3 Stopwatch",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/jsanchezd/stopywatch",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[]
)
