from __future__ import absolute_import
from __future__ import unicode_literals
import os

from setuptools import setup, find_packages

try:
    with open("README.rst") as f:
        readme = f.read()
except IOError:
    readme = ''

def __requires_from_file(filename):
    return open(filename).read().splitlines()

here = os.path.dirname(os.path.abspath(__file__))
version = next((line.split('=')[1].strip().replace("'", '')
                for line in open(os.path.join(here, 'cluster', '__init__.py'))
                if line.startswith('__version__ =')), '0.0.dev0')

setup(
        name="cluster-lee",
        version=version,
        url='https://github.com/alien2327/cluster-lee',
        author='YohanLee',
        author_email='alien2327@gmail.com',
        maintainer='YohanLee',
        maintainer_email='alien2327@gmail.com',
        description='Package Dependency: Validates package requirements',
        long_description=readme,
        packages=find_packages(),
        install_requires=['numpy', 'tqdm'],
        license='MIT',
        classifiers=['Programming Language :: Python :: 3'],
        entry_points="""
        # -*- Entry points: -*-
        [console_scripts]
        pkgdep = pypipkg.scripts.command:main
        """
)
