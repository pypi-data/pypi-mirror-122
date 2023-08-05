"""
Setup
"""
import setuptools

with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="time_series_transformer",
    version="1.0.2",
    author="Daniel Kaminski de Souza",
    author_email="daniel@kryptonunite.com",
    description="Time Series Transformer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DanielAtKrypton/time_series_transformer",
    packages=['time_series_transformer'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        # use the following for torch 1.9.1 and cuda 11.1:
        # "torch==1.9.1+cu111",
        # yse the following for torch only
        "torch",
    ],
    extras_require={
        'dev': [
            'pylint',
            'autopep8',
            'bumpversion',
            'twine',
        ],
        'test': [
            'pytest>=4.6',
            'pytest-cov',
            'flights-time-series-dataset',
            'time-series-predictor',
        ],
        'docs': [
        ]
    }
)
