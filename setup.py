import setuptools

setuptools.setup(
    name="parvus",
    version="0.0.1",
    author="Jonas",
    author_email="jonas@valfridsson.net",
    description="Tiny python webserver",
    url="",
    packages=setuptools.find_packages(exclude=["tests"]),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
