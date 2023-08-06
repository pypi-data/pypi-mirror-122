from setuptools import setup

import sys
import platform

plat_bit = platform.architecture()[0]

major = sys.version_info.major
minor = sys.version_info.minor
micro = sys.version_info.micro

package_dir = {}

if major == 3 and minor == 5:
    if micro > 2:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py35_64/iobjectspy'}
    else:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py352_64/iobjectspy'}
elif major == 3 and minor == 6:
    if micro < 6:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py36_64/iobjectspy'}
    else:
        package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py366_64/iobjectspy'}
elif major == 3 and minor == 7:
    package_dir = {'iobjectspy': 'iobjectspy/iobjectspy-py37_64/iobjectspy'}
else:
    raise RuntimeError('Unsupported python version : %d.%d ' % (major, minor))

try:
    with open("README.md", "r", encoding='utf-8') as fh:
        long_description = fh.read()
except Exception:
    long_description = ''

_ignore_names = set(('_csuperpy', '__pycache__', '.gitignore'))


def _list_files(path, package_data):
    import os
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if file not in _ignore_names:
            if os.path.isfile(file_path):
                package_data.append(file_path)
            elif os.path.isdir(file_path):
                _list_files(file_path, package_data)


def _get_package_data():
    import os
    package_data = []
    current_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), package_dir['iobjectspy'])
    _list_files(current_path, package_data)
    result_package_data = []
    format_current_path = current_path.replace('\\', '/') + '/'
    for f in package_data:
        file_path = str(f).replace('\\', '/')
        result_package_data.append(file_path.replace(format_current_path, ''))
    return result_package_data


setup(
    name='iobjectspy',
    version='10.2.0',
    packages=['iobjectspy'],
    url='http://iobjectspy.supermap.io',
    license='SuperMap',
    description='SuperMap iObjects Python',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'py4j==0.10.7'
    ],
    package_data={'iobjectspy': _get_package_data()},
    package_dir=package_dir,
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries',
    ],
    entry_points={
        "console_scripts": [
            "iobjectspy=iobjectspy:main",
        ],
    },
)
