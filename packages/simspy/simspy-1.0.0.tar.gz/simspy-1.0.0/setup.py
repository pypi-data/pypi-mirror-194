import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simspy",
    version="1.0.0",
    author="Milla and Kewalin",
    author_email="millah211@gmail.com, kewalin-16@hotmail.com",
    description="SIMSPY is an 8-function package that can only solve single machine scheduling problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires= ['random','tkinter','ttkbootstrap'],
    python_requires='>=3.7',
)
