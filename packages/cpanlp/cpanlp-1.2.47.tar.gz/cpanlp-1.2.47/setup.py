from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.2.47'
DESCRIPTION = 'Narrating Accounting Using Python like a 🤖️.'

# Setting up
setup(
    name="cpanlp",
    version=VERSION,
    author="Draco Deng",
    author_email="dracodeng6@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://cpanlp.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[],
    keywords=['machine language', 'python', 'accounting', 'cpa', 'audit','intelligent accounting', 'linguistic turn', 'linguistic',"intelligent audit","natural language processing","machine learning","finance","certified public accountant",'big four'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        'Natural Language :: English',
        'Natural Language :: Chinese (Simplified)',
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Investment",
    ]
)