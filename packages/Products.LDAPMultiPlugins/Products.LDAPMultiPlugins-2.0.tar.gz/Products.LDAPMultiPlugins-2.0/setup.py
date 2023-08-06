##############################################################################
#
# Copyright (c) 2010-2021 Jens Vagelpohl and Contributors. All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

import os

from setuptools import find_packages
from setuptools import setup


NAME = 'LDAPMultiPlugins'
here = os.path.abspath(os.path.dirname(__file__))

def _read(name):
    f = open(os.path.join(here, name))
    return f.read()

_boundary = '\n' + ('-' * 60) + '\n\n'

setup(name='Products.%s' % NAME,
      version='2.0',
      description='LDAP-backed plugins for the Zope2 PluggableAuthService',
      long_description=( _read('README.rst') 
                       + _boundary
                       + _read('CHANGES.rst')
                       ),
      classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Framework :: Zope2",
        "Framework :: Zope :: 2",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Zope Public License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2 :: Only",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development",
        "Topic :: System :: Systems Administration ::"
        " Authentication/Directory :: LDAP",
        ],
      keywords='web application server zope zope2 ldap',
      author="Jens Vagelpohl and contributors",
      author_email="jens@dataflake.org",
      url="http://pypi.python.org/pypi/Products.%s" % NAME,
      project_urls={
        'Issue Tracker': ('https://github.com/dataflake/'
                          'Products.LDAPMultiPlugins/issues'),
        'Sources': 'https://github.com/dataflake/Products.LDAPMultiPlugins',
      },
      license="ZPL 2.1",
      packages=find_packages(),
      include_package_data=True,
      namespace_packages=['Products'],
      zip_safe=False,
      python_requires='>=2.7,<3',
      install_requires=[
        'setuptools',
        'Zope2 <4',
        'python-ldap <3',
        'Products.LDAPUserFolder <3',
        'Products.PluggableAuthService <2',
        ],
      extras_require={
        'exportimport': ['Products.GenericSetup <1.9'],
        'docs': [
          'Sphinx',
          'sphinx_rtd_theme',
          'repoze.sphinx.autointerface',
          'pkginfo'
        ],
      },
      entry_points="""
      [zope2.initialize]
      Products.%s = Products.%s:initialize
      """ % (NAME, NAME),
      )

