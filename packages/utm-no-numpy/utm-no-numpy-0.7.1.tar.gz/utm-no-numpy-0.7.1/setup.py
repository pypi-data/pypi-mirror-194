from distutils.core import setup

from utm_no_numpy._version import __version__


setup(
    name='utm-no-numpy',
    version=__version__,
    author='Tobias Bieniek',
    author_email='none@example.com',
    url='https://github.com//JamesParrott/utm-no-numpy',
    description='Bidirectional UTM-WGS84 converter for python',
    keywords=['utm', 'wgs84', 'coordinate', 'converter'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    packages=['utm_no_numpy'],
    scripts=['scripts/utm-converter'],
)