from setuptools import setup, find_packages

VERSION = '0.0.31'
DESCRIPTION = 'Saeligram Basic Package'
LONG_DESCRIPTION = 'A basic package as of now but will build in future \n You can import by typing import saeli'

# Setting up
setup(
    name="saeligram",
    version=VERSION,
    author="Saeligram",
    author_email="<saeligram@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)