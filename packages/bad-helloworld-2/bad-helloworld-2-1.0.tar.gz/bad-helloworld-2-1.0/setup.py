from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name = "bad-helloworld-2", # by this name people can download that project
    version = "1.0",
    description = "hello world to break dependencies...",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    py_modules = ["helloworld"], # modules of package
    package_dir = {'': 'src'}, # our code under src directory
    classifiers = [
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires = [
         "numpy==1.20.0", # :))
    ],
    # extras_require = {
    #     "dev": [
    #         "pytest>=3.7",
    #     ]
    # }
    python_requires=">=3.9", # :))
)
