from distutils.core import setup

setup(
    name='ytlisten',
    version='0.13',
    description='A command-line tool to search and listen to YouTube audio',
    author='Chris Ismael',
    author_email='chris.ismael@gmail.com',
    url='https://github.com/ismaelc/ytlisten',
    packages=['ytlisten'],
    install_requires=[
        'google-api-python-client',
        'python-vlc',
        'pytube'
    ]
)