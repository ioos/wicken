try:
    from setuptools import setup, find_packages
    packages = find_packages()
except ImportError:
    from distutils import setup

setup(
    name='Wicken',
    version='0.1.2',
    description='Maps metadata concepts to concrete specifations and file formats',
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
    license='GPLv3',
    keywords='Metadata ISO OGC NetCDF lxml xml ncml',
    packages= ['wicken'],
    install_requires = [
            'nose>=1.2.0',
            'lxml>=3.2.1',
            'petulant-bear>=0.1.2'
            ],
)
