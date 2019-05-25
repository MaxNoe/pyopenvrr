from setuptools import setup, find_packages


setup(
    name='openvrr',
    author='Maximilian Nöthe',
    author_email='maximilian.noethe@tu-dortmund.de',
    version='0.1.0',
    packages=find_packages(),
    install_requires=['requests'],
)
