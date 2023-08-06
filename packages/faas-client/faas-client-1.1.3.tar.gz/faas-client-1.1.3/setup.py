import os

import setuptools

install_requires = [
    "sh"
]

test_requires = [
    "pytest",
    "pytest-xdist"
]

client_version = os.environ.get("CLIENT_VERSION", "0.0.0")

setuptools.setup(
    name="faas-client",
    version=client_version,
    author="Laurent Michel",
    author_email="softozor@gmail.com",
    description=f"A client library for faas-cli",
    url="https://gitlab.hidora.com/softozor/faas-client",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    extras_require={
        "test": test_requires,
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
