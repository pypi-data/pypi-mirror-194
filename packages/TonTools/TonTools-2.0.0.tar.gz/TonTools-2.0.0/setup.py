from setuptools import setup

requirements = ["tonsdk>=1.0.6", "ton>=0.26", "aiohttp>=3.8.1", "setuptools>=65.3.0", "requests>=2.28.1"]

setup(
    name='TonTools',
    version='2.0.0',
    packages=['TonTools'],
    url='',
    license='MIT License',
    author='yungwine',
    author_email='cyrbatoff@gmail.com',
    description='Explore TON Blockchain with python',
    install_requires=requirements,
)
