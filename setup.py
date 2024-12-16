# based on https://github.com/pypa/sampleproject
# MIT License

# Always prefer setuptools over distutils
from setuptools import setup, find_namespace_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='asreview-top2vec',
    description='Top2Vec tool for the ASReview project',
    version='0.1',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/george-gca/asreview-top2vec',
    author='George Araújo',
    author_email='george.gcac@gmail.com',
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 3 - Alpha',

        # Pick your license as you wish
        'License :: OSI Approved :: Apache Software License',

        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    keywords='asreview extension top2vec clusters visualization',
    packages=find_namespace_packages(include=['asreviewcontrib.*']),
    install_requires=[
        "asreview",
        "scikit-learn",
        "tensorboard",
        "top2vec",
    ],

    extras_require={
    },

    entry_points={
        "asreview.entry_points": [
            "top2vec = asreviewcontrib.top2vec.main:Top2VecEntryPoint",  # noqa: E501
        ]
    },

    project_urls={
        'Bug Reports':
            "https://github.com/george-gca/asreview-top2vec/issues",
        'Source':
            "https://github.com/george-gca/asreview-top2vec",
    },
)
