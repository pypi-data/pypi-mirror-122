from setuptools import setup

setup(
    name='pertsev_krogh_interpolator',
    version='0.1.0',
    description='My realisation of Krogh interpolator',
    url='https://github.com/pertsevpv',
    author='Pertsev Pavel',
    author_email='pertsevpv@gmail.com',
    license='BSD 2-clause',
    packages=['pertsev_krogh_interpolator'],
    install_requires=[
                      'numpy',
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
