from setuptools import setup

__project__ = 'kamrakamri_OOP'
__version__ = '62.51'
__description__ = 'A text-based adventure game using OOP'
__packages__ = ['slay']
__author__ = 'Raz Raza'
__author_email__ = "abcrazzak20@gmail.com"
__classifiers__ = [
    'Development Status :: 1 - Planning',
    'Intended Audience :: Education',
    'Programming Language :: Python :: 3',
    "Operating System :: OS Independent"
]
__requires__ = []

# Setting up
setup(  name = __project__,
        version = __version__,
        description = __description__,
        packages = __packages__,
        author = __author__,
        author_email = __author_email__,
        keywords = [],
        classifiers = __classifiers__,
        requires = __requires__
      )



