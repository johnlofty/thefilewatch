from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='thefilewatch',
    version='0.0.8',
    author='johnlofty',
    author_email='johnlofty@163.com',
    url='https://github.com/johnlofty/thefilewatch',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='multi-files watcher',
    packages=['thefilewatch'],
    install_requires=[
        'pyinotify',
    ],
    entry_points={}
)
