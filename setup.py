from setuptools import find_packages, setup

setup(
    name="ansys-sherlock",
    version="0.1.dev0",
    description="A Python wrapper for Ansys Sherlock gRPC APIs",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    url="https://github.com/pyansys/pySherlock/",
    license="MIT",
    author="ANSYS, Inc.",  # this is required
    maintainer="PyAnsys developers",  # you can change this
    # this email group works
    maintainer_email="pyansys.support@ansys.com",
    # Include all install requirements here.  If you have a longer
    # list, feel free just to create the list outside of ``setup`` and
    # add it here.
    install_requires=[],
    # Plan on supporting only the currently supported versions of Python
    python_requires=">=3.7",
    # Less than critical but helpful
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
