import setuptools

with open("README.md", "r") as fh:

    long_description = fh.read()

setuptools.setup(

    name="formula_commit",

    version="1.0.0",

    author="BigForLy",

    author_email="authorname@templatepackage.com",

    description="Template Setup.py package",

    long_description=long_description,

    long_description_content_type="text/markdown",

    url="https://github.com/BigForLy/formula_commit",

    packages=setuptools.find_packages(),

    classifiers=[

        "Programming Language :: Python :: 3",

        "License :: OSI Approved :: MIT License",

        "Operating System :: OS Independent",

    ],

    python_requires='>=3.9',

)