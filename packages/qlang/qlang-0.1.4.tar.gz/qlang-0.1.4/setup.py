from setuptools import setup
from pathlib import Path

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='qlang',
    version='0.1.4',
    author='nirvanasupermind',
    author_email='nirvana.supermind@gmail.com',
    url='https://github.com/nirvanasupermind/qlang',
    license='LICENSE',
    packages=['.'],
    description='A concise, procedural programming language',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=[]
)