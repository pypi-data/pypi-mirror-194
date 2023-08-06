from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'API and CLI to manage a remote filesystem'

setup(
    name='simplecloud',
    version='0.0.0.2',
    author='Garrett Charles',
    author_email='realcomputerscientist@gmail.com',
    description='Local Network Cloud',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'cloud = cloud.cloud_cli:main',
            'cloud-server = cloud.cloud_api:main'
        ]
    },
    keywords='',
    install_requires=requirements,
    zip_safe=False
)