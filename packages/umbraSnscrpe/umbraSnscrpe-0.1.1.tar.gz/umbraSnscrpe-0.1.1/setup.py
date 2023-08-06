from setuptools import setup, find_packages
import codecs
import os


VERSION = '0.1.1'
DESCRIPTION = ''
LONG_DESCRIPTION = ''

# Setting up
setup(
    name="umbraSnscrpe",
    version=VERSION,
    author="umbra",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[	'requests[socks]',
	'lxml',
	'beautifulsoup4',
	'pytz; python_version < "3.9.0"',
	'filelock'],
    keywords=['lxml', 'requests[socks]', 'beautifulsoup4', 'pytz; python_version < "3.9.0"', 'filelock'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ]
)