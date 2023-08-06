from setuptools import setup

setup(
    name='stoclust',
    version='0.1.5',
    author='Samuel Loomis',
    author_email='sloomis@ucdavis.edu',
    packages=['stoclust'],
    description='Modular methods for stochastic clustering',
    install_requires=[
        'numpy >= 1.15.0',
        'scipy >= 1.1.0',
        'plotly >= 4.12.0',
        'tqdm >= 4.41.1',
        'pandas >= 0.25.0'
    ],
)