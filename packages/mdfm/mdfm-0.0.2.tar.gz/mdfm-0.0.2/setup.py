from setuptools import setup
from os import path

DIR = path.dirname(path.abspath(__file__))
DESCRIPTION = "mdfm is a linux tools for My Dot Files Manager. (backup or restore)"
KEYWORDS = ['dfm', 'mdfm', 'dotfiles', 'backup',
            'backup-script', 'linux', 'python']
AUTHORS = 'lisuke'
URL = 'http://github.com/lisuke/mdfm'
EMAIL = '1657787678@qq.com'

with open(path.join(DIR, 'requirements.txt')) as f:
    INSTALL_PACKAGES = f.read().splitlines()

with open(path.join(DIR, 'README.md')) as f:
    README = f.read()

# get __version__ from _version.py
ver_file = path.join('mdfm', '_version.py')
with open(ver_file) as f:
    exec(f.read())

VERSION = __version__

setup(
    name='mdfm',
    packages=['mdfm'],
    description=DESCRIPTION,
    long_description=README,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_PACKAGES,
    version=VERSION,
    url=URL,
    author=AUTHORS,
    author_email=EMAIL,
    keywords=KEYWORDS,
    license="GPLv3",
    tests_require=[
        # 'pytest'
    ],
    include_package_data=True,
    platforms="any",
    python_requires='>=3',
    entry_points={
        'console_scripts': [
            'mdfm = mdfm.mdfm:main'
        ]
    }
)
