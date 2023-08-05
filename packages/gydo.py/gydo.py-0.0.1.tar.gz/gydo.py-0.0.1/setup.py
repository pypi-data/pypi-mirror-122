from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = 'A Package for interacting with Discord\'s API'

# Setting up
setup(
    name="gydo.py",
    version=VERSION,
    author="loldonut (John Heinrich)",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['requests', 'schedule', 'websockets', 'aiohttp'],
    keywords=['python', 'discord', 'gydo.py', 'discord api']
)