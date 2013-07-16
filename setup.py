try:
    from setuptools import setup, find_packages
    packages = find_packages()
except ImportError:
    from distutils import setup

setup(
    name='Wicken',
    version='0.1',
    description='Maps metadata concepts to concrete spefications and file formats',
    author='David Stuebe',
    author_email='DStuebe@ASAScience.com',
    url='https://github.com/asascience-open/wicken',
    classifiers=[
        'License :: GNU GPL',
        'Topic :: OGC :: Metadata',
        'Topic :: NetCDF :: CF',
        'Topic :: ISO :: Metadata'
        ],
    license='GNU GPL',
    keywords='Metadata ISO OGC NetCDF lxml xml ncml',
    packages= ['wicken'],
    install_requires = [
            'nose>=1.2.0',
            'lxml>=3.2.1',
            'petulantbear>=0.1'
            ],
)
