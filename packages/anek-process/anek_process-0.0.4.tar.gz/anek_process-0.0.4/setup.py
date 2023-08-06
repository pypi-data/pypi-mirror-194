from setuptools import setup, find_packages
from metadata import VERSION, DESCRIPTION, LONG_DESCRIPTION
# Setting up
setup(
    name="anek_process",
    version=VERSION,
    author="Bhramaand (Lalit Atrish)",
    author_email="<atrish.lalit03@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
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