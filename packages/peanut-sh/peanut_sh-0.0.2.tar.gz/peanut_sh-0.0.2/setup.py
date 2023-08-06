from setuptools import setup, find_packages

from peanut_sh import __version__

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3 :: Only',
    'Programming Language :: Python :: Implementation :: CPython',
    'Programming Language :: Python :: Implementation :: PyPy',
]

setup(
    name='peanut_sh',
    version=__version__,
    description='Daemon process on Unix-like systems',
    author='shfubet',
    author_email='shfubet@gmail.com',
    license='MIT',
    packages=find_packages(include=["peanut_sh"]),
    python_requires='>=3.8',
    classifiers=CLASSIFIERS,
    include_package_data=True,
)
