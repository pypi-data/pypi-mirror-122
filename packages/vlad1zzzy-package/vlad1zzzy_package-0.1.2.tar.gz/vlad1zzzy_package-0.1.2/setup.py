from setuptools import setup

#matplotlib require numpy>=1.16
#pandas require numpy>=1.17
setup(
    name='vlad1zzzy_package',
    version='0.1.2',
    description='A example Python package',
    url='https://github.com/vlad1zzzy/vlad1zzzy_package',
    author='Vlad Kryukov',
    author_email='vladikkrukov0204@gmail.com',
    packages=['vlad1zzzy_package'],
    install_requires=['matplotlib',
                      'pandas',
                      'scipy',
                      'numpy==1.16',
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