from setuptools import setup

setup(
    name='Wicken',
    version='0.2.0',
    description='Maps metadata concepts to concrete specifications and file formats',
    author='David Stuebe',
    author_email='DStuebe@ASAScience.com',
    url='https://github.com/ioos/wicken',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Topic :: Scientific/Engineering',
    ],
    license='Apache 2.0',
    keywords='Metadata ISO OGC NetCDF lxml xml ncml',
    packages=['wicken'],
    tests_require=['nose>=1.2.0'],
    install_requires=[
            'netCDF4>=1.0.0',
            'lxml>=3.2.1',
            'petulant-bear>=0.1.2'
            ],
)
