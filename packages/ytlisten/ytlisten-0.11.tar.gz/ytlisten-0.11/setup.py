from setuptools import setup, find_packages

setup(
    name='ytlisten',
    version='0.11',
    description='A command-line tool to search and listen to YouTube audio',
    author='Chris Ismael',
    author_email='chris.ismael@gmail.com',
    url='https://github.com/ismaelc/ytlisten',
    packages=find_packages(),
    install_requires=[
        'google-api-python-client',
        'python-vlc',
        'pytube'
    ],
    entry_points={
        'console_scripts': [
            'ytlisten = ytlisten.ytlisten:main'
        ]
    }
)