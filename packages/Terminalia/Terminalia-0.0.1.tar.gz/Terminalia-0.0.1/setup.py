from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A Python Library for Command Line Interface (CLI) Development'

# Setting up
setup(
    name="Terminalia",
    version=VERSION,
    author="ai",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=['requests', 'textblob', 'langdetect'],
    keywords=['python', 'terminal', 'console', 'color', 'style', 'design'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)