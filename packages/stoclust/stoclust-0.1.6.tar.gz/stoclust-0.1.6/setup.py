from setuptools import setup
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='stoclust',
    version='0.1.6',
    author='Samuel Loomis',
    author_email='sloomis@ucdavis.edu',
    packages=['stoclust'],
    description='Modular methods for stochastic clustering',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[
        'numpy >= 1.15.0',
        'scipy >= 1.1.0',
        'plotly >= 4.12.0',
        'tqdm >= 4.41.1',
        'pandas >= 0.25.0'
    ],
)