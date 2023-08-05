from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='TBGDL',
    long_description_content_type='text/markdown',
    long_description=long_description,
    keywords="pygame, textadventure, text, game",
    version='1.0.2',
    packages=['tbgdl'],
    install_requires=[
        "colorama",
        "simpleaudio",
        "numpy",
        "musicalbeeps"
    ],
    url='https://github.com/Marko2155/TBGDL',
    license='MIT',
    author='Marko Camandioti',
    author_email='camandiotimarko@gmail.com',
    description="A Python library for creating text-based games.",
    project_urls={
        'Documentation': 'https://github.com/Marko2155/TBGDL#readme',
        'Source': 'https://github.com/Marko2155/TBGDL',
        'Tracker': 'https://github.com/Marko2155/TBGDL/issues',
    }
)
