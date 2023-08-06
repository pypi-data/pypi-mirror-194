from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

setup(
    name='ytlisten',
    version='0.19',
    description='A command-line tool to search and listen to YouTube audio',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
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
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    zip_safe = False
)