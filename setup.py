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
import cloudcafe
import platform
import shutil

# These imports are only possible on Linux/OSX
if platform.system().lower() != 'windows':
    import pwd
    import grp

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload')
    sys.exit()

requires = open('pip-requires').readlines()

setup(
    name='cloudcafe',
    version=cloudcafe.__version__,
    description='CloudCAFE is an implementation of the Open CAFE Framework specifically designed to test deployed versions of OpenStack',
    long_description='{0}\n\n{1}'.format(
        open('README.md').read(),
        open('HISTORY.rst').read()),
    author='Rackspace Cloud QE',
    author_email='cloud-cafe@lists.rackspace.com',
    url='http://rackspace.com',
    packages=find_packages(exclude=[]),
    package_data={'': ['LICENSE', 'NOTICE']},
    package_dir={'cloudcafe': 'cloudcafe'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    #https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=(
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: Other/Proprietary License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',
        #'Programming Language :: Python :: 3.1',
        #'Programming Language :: Python :: 3.2',
        #'Programming Language :: Python :: 3.3',
    )
)

''' @todo: need to clean this up or do it with puppet/chef '''
# Default Config Options
root_dir = "{0}/.cloudcafe".format(os.path.expanduser("~"))
config_dir = "{0}/configs".format(root_dir)

# Build Default directories
if(os.path.exists("{0}/engine.config".format(config_dir)) == False):
    raise Exception("Core CAFE Engine configuration not found")
else:
    # Copy over the default configurations
    if(os.path.exists("~install")):
        os.remove("~install")
        # Report
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
    else:
        # State file
        temp = open("~install", "w")
        temp.close()

        # Modify file permissions if on not running on Windows or as root
        modify_permissions = (platform.system().lower() != 'windows'
                              and os.getenv("SUDO_USER"))

        # Get uid and gid of the current user to set permissions (Linux/OSX only)
        if modify_permissions:
            sudo_user = os.getenv("SUDO_USER")
            uid = pwd.getpwnam(sudo_user).pw_uid
            gid = pwd.getpwnam(sudo_user).pw_gid
    
        config_dirs = os.listdir("configs")
        for dir in config_dirs:
            if not os.path.exists("{0}/{1}".format(config_dir, dir)):
                print("Installing configurations for: {0}".format("{0}/{1}".format(config_dir, dir)))
                os.makedirs("{0}/{1}".format(config_dir, dir))
                # Fix the directory permissions
                if modify_permissions:
                    os.chown("{0}/{1}".format(config_dir, dir), uid, gid)
            for file in os.listdir("configs/{0}".format(dir)):
                print("Installing {0}/{1}/{2}".format(config_dir, dir, file))
                shutil.copy2("configs/{0}/{1}".format(dir, file), "{0}/{1}/{2}".format(config_dir, dir, file))
                # Fix the directory permissions
                if modify_permissions:
                    os.chown("{0}/{1}/{2}".format(config_dir, dir, file), uid, gid)
