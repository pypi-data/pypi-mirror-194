from setuptools import setup, find_packages

setup(
    name='talktokitty',
    version='0.1.1',
    license='MIT',
    author='Alec Becker',
    author_email='alecbecker1@gmail.com',
    url='https://github.com/awbecker25/talktokitty',
    description='A python package fot talking to Peaches and Molasses',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    entry_points={
        'console_scripts': ['talktokitty=talktokitty.main:main']
    }
)
