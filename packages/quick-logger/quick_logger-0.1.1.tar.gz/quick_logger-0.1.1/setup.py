import setuptools


with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quick_logger",
    version="0.1.1",
    author="Michael Everingham",
    author_email="lamerlink@live.com",
    description="A simple interface for the standard Python logging library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaeleveringham/quick_logger",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
        "Typing :: Typed",
    ],
    python_requires='>=3.7',
)
