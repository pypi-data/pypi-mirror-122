from setuptools import setup

setup(name='apwz',
    version='0.1',
    description='A python',
    url='http://github.com/takipsizad/apwz',
    author='takipsizad',
    author_email='addeniz25@gmail.com',
    license='GPLV3',
    entry_points={
        'console_scripts': ['apwz=apwz.command_line:main'],
    },
    zip_safe=False
)
