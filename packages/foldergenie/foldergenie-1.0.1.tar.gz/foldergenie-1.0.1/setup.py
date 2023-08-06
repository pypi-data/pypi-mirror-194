from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Directory structure creation'
LONG_DESCRIPTION = 'A package that allows to create complex folder structures'

# Setting up
setup(
    name="foldergenie",
    version=VERSION,
    author="Skadoosh (Hariprasad)",
    author_email="<hariprasad19036@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'folder', 'file', 'directory', 'organize'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)