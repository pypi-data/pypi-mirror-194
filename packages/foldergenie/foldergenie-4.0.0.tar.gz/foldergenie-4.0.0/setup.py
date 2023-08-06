from setuptools import setup, find_packages

VERSION = '4.0.0'
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
    entry_points={
        'console_scripts': ['foldergenie=foldergenie:foldergenie'],
    },
    install_requires=[],
    keywords=['python', 'folder', 'file', 'directory', 'organize'],
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: Microsoft :: Windows",
    ]
)