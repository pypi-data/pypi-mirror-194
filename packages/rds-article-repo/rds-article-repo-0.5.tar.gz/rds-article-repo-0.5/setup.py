from setuptools import setup

setup(name='rds-article-repo',
        version='0.05',
        description='util functions for  applications.',
        author='Johnson Simon',
        packages=['rds-article-repo'],
        install_requires=['wheel','boto3','requests',
        'dnspython'])
