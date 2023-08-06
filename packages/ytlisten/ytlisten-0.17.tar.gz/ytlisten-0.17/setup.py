from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='ytlisten',
    version='0.17',
    description='A command-line tool to search and listen to YouTube audio',
    author='Chris Ismael',
    author_email='chris.ismael@gmail.com',
    url='https://github.com/ismaelc/ytlisten',
    license ='MIT',
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'ytlisten=ytlisten_proj.ytlisten:main'
        ]
    },
    zip_safe = False
)