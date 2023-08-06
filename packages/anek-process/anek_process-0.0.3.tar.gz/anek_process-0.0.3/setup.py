

from setuptools import setup, find_packages
import codecs
import os

# here = os.path.abspath(os.path.dirname(__file__))

# with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
#     long_description = "\n" + fh.read()

VERSION = '0.0.3'
DESCRIPTION = 'Parallel processing of tasks for vertical scaling'
LONG_DESCRIPTION = 'A package to provide ability to execute a small program in parallel with the ability to stop the execution in the middle without thinking too much about memory leaks.'

# Setting up
setup(
    name="anek_process",
    version=VERSION,
    author="Bhramaand (Lalit Atrish)",
    author_email="<atrish.lalit03@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(include=['dist'], exclude=['build','multiproc']),
    install_requires=[],
    keywords=['python', 'parallel', 'processing', 'thread', 'threading', 'veritcal','scaling'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)