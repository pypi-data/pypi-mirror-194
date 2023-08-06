import os

from setuptools import find_packages, setup

__version__ = '0.0.dev1677500204'


def read(file_name):
    with open(os.path.join(os.path.dirname(__file__), file_name)) as f:
        return f.read()


setup(
    name='discord-repl',
    version=__version__,
    author='Ettore Leandro Tognoli',
    author_email='ettoreleandrotognoli@gmail.com',
    license='Apache License 2.0',
    data_files=[
        'LICENSE',
    ],
    description='Discord REPL',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    packages=find_packages(
        './src/main/python/',
    ),
    package_dir={'': 'src/main/python'},
    package_data={
        '': ['**/*.toml'],
    },
    include_package_data=True,
    classifiers=[
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
    ],
    python_requires='>=3.10',
    install_requires=[
        'discord.py==1.7.*',
        'emoji==0.6.*',
        'docker==6.*',
        "toml==0.10.*",
        "pyyaml==6.*",
    ],
    tests_require=[
        'coverage',
        'pylint',
    ],
    entry_points={
        'console_scripts': [
            'discord-repl=discord_repl.__main__:_main'
        ]
    },
)
