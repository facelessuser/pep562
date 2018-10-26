#!/usr/bin/env python
"""Setup Pep562."""

from setuptools import setup, find_packages
import os
import imp
import traceback


def get_version():
    """Get version and version_info without importing the entire module."""

    devstatus = {
        'alpha': '3 - Alpha',
        'beta': '4 - Beta',
        'candidate': '4 - Beta',
        'final': '5 - Production/Stable'
    }
    path = os.path.join(os.path.dirname(__file__), 'pep562')
    fp, pathname, desc = imp.find_module('__meta__', [path])
    try:
        v = imp.load_module('__meta__', fp, pathname, desc)
        if v.__version_info__[3].startswith('.dev-'):
            return v.__version__, '2 - Pre-Alpha'
        else:
            return v.__version__, devstatus[v.__version_info__[3]]
    except Exception:
        print(traceback.format_exc())
    finally:
        fp.close()


def get_requirements(req):
    """Load list of dependencies."""

    install_requires = []
    with open(req) as f:
        for line in f:
            if not line.startswith("#"):
                install_requires.append(line.strip())
    return install_requires


def get_description():
    """Get long description."""

    with open("README.md", 'r') as f:
        desc = f.read()
    return desc


VER, DEVSTATUS = get_version()


setup(
    name='pep562',
    version=VER,
    keywords='pep 562 backport',
    description='Backport of PEP 562.',
    long_description=get_description(),
    long_description_content_type='text/markdown',
    author='Isaac Muse',
    author_email='Isaac.Muse@gmail.com',
    url='https://github.com/facelessuser/pep562',
    packages=find_packages(exclude=['tests']),
    license='MIT License',
    classifiers=[
        'Development Status :: %s' % DEVSTATUS,
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
    ]
)
