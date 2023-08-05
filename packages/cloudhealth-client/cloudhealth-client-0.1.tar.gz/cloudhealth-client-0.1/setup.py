from setuptools import setup

setup(
    name='cloudhealth-client',
    version='0.1',
    author='Alberto Narro',
    author_email='alberto.narro@hotmail.com',
    url = 'https://github.com/albertonarro/cloudhealth-client',
    keywords = ['CLOUDHEALTH', 'CLIENT', 'CLI'],
    packages=['cloudhealth'],
    license='LICENSE',
    description='A REST Client for Cloudhealth',
    install_requires=[
        'requests==2.28.2',
    ]
)
