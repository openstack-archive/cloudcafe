"""
Copyright 2013 Rackspace

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import os
import sys


try:
    from setuptools import setup, find_packages
    from setuptools.command.install import install as _install
except ImportError:
    from distutils.core import setup, find_packages
    from distutils.command.install import install as _install

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()


def print_cafe_mug():
    print('\n'.join(["\t\t   _ _ _",
                     "\t\t  ( `   )_ ",
                     "\t\t (    )   `)  _",
                     "\t\t(____(__.___`)__)",
                     "\t\t",
                     "\t\t    ( (",
                     "\t\t       ) )",
                     "\t\t    .........    ",
                     "\t\t    |       |___ ",
                     "\t\t    |       |_  |",
                     "\t\t    |  :-)  |_| |",
                     "\t\t    |       |___|",
                     "\t\t    |_______|",
                     "\t\t=== CloudCAFE ==="]))
    print("========================================================")
    print("CloudCAFE Framework installed")
    print("========================================================")


#Post-install engine configuration
def _post_install(dir):
    from cafe.configurator.managers import EngineConfigManager
    EngineConfigManager.install_optional_configs('configs')
    print_cafe_mug()


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(
            _post_install, (self.install_lib,),
            msg="Running post install tasks...")


requires = open('pip-requires').readlines()
setup(
    name='cloudcafe',
    version='0.0.1',
    description=(
        'CloudCAFE is an implementation of the Open CAFE Framework '
        'specifically designed to test deployed versions of OpenStack'),
    long_description='{0}\n\n{1}'.format(
        open('README.md').read(),
        open('HISTORY.rst').read()),
    author='Rackspace Cloud QE',
    author_email='cloud-cafe@lists.rackspace.com',
    url='http://rackspace.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',),
    cmdclass={'install': install})
