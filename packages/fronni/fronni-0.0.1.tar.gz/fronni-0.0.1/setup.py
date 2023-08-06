import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as fh:
    license = fh.read()

with open("requirements.txt", "r") as fh:
    require = fh.read()

setuptools.setup(
    name="fronni",                     # This is the name of the package
    version="0.0.1",                        # The initial release version
    author="Kaushik Mitra",                     # Full name of the author
    description="Machine Learning model performance metrics & charts with confidence intervals, optimized with numba to be fast",
    long_description=long_description,      # Long description read from the the readme file
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),    # List of all python modules to be installed
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],                                      # Information to filter the project on PyPi website
    python_requires='>=3.6',                # Minimum version requirement of the package
    py_modules=["fronni"],             # Name of the python package
    package_dir={'':'fronni/src'},     # Directory of the source code of the package
    install_requires=[require]                     # Install other dependencies if any
)