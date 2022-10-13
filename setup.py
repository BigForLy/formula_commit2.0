from setuptools import find_packages, setup

with open("README.md") as f:
    long_description = f.read()


setup(
    name="formula_commit",
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    version="1.1.11",
    license="MIT",
    license_files="LICENSE",
    author="BigForLy",
    author_email="not_my_email@net_domena.ay",
    description="Formula commit",
    url="https://github.com/BigForLy/formula_commit2.0",
    python_requires=">=3.9",
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=["memory-profiler==0.60.0"],
)
