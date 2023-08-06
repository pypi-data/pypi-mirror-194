from setuptools import setup

setup(
    name='regmodel',
    version='0.1',
    packages=['push'],
    install_requires=[
        'awscli',
        'gto',
        'dvc[s3]'
    ],
    entry_points={
        'console_scripts': [
            'regmodel = push.main:main'
        ]
    }
)