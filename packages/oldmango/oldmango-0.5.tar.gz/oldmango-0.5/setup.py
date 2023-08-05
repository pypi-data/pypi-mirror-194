from setuptools import setup, find_packages

setup(
    name='oldmango',
    version='0.5',
    description='Linux commands AI',
    packages=find_packages(),
    install_requires=[
        'openai==0.25.0',
        'click==7.1.2',
        'requests==2.26.0',
        'aiohttp'
    ],
    entry_points={
        'console_scripts': [
            'oldmango=oldmango.oldmango:main'
        ]
    }
)

