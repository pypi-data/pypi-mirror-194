import json
import os
from pathlib import Path

from setuptools import find_packages
from setuptools import setup

mod_name = 'on-the-fly-stats'
package_name = mod_name.replace('-', '_')
this_directory = Path(__file__).parent

# Note: must not use Constants here; causes the install/setup to fail
version = None
path = os.path.join(os.path.abspath(os.path.dirname(__file__)), package_name, 'lib', 'version.json')
with open(path, 'r', encoding='utf-8') as fp:
    j = json.load(fp)
    version = j['version']
print(f'setup for version: {version}')

long_desc = (this_directory / 'README.md').read_text()
long_version = version.replace('.', '_')

setup(
    name=mod_name,
    include_package_data=True,
    packages=find_packages(include=f'{package_name}*', ),
    version=version,
    license='MIT',
    description='On the fly statistics including standard deviation, average, min/max and counters',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    author='JA',
    author_email='cppgent0@gmail.com',
    url=f'https://bitbucket.org/arrizza-public/{mod_name}/src/master',
    download_url=f'https://bitbucket.org/arrizza-public/{mod_name}/get/master.zip',
    keywords=['statistics', 'utility'],
    install_requires=[
        'pytest-ver',
    ],
    classifiers=[
        # Choose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable"
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.9',
    ],
)

print('OK   GenBuildInfo completed successfully')
