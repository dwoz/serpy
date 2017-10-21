from setuptools import setup

test_requires = [
    'tox',
    'pytest',
]

setup(
    name = 'serpy',
    py_modules = ['libserpy'],
    version = '0.0.1',
    description = (
        'Serpy provides library and command line tool for querying search '
        'engines'
    ),
    author = 'dan@woz.io',
    author_email = 'dan@woz.io',
    url = 'https://github.com/dwoz/serpy',
    keywords = [
        'web', 'search',
    ],
    entry_points = {
        'console_scripts': [
            'serpy=libserpy:main',
        ],
    },
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Other Audience',
        'Programming Language :: Python',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Topic :: Utilities',
    ],
)

