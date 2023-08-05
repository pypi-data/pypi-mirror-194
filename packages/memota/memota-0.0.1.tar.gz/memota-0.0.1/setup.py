from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'CLI for ram monitoring'

# Setting up
setup(
    name="memota",
    version=VERSION,
    author="Bovdur",
    author_email="<mail@neuralnine.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
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