from setuptools import setup

setup(
    name='ezdownloader',
    version='0.1.1',
    description = 'A simple file downloading tool ',
    author = 'codemilo',
    author_email = 'milomurthy@gmail.com',
    url = 'https://github.com/codemilo-ui/ezdownloader',
    packages=['ezdownloader'],
    keywords = ['downloader', 'wget'],
    install_requires=[
        'urllib3',
        'tqdm'
    ],
    entry_points={
        'console_scripts': [
            'ezdownloader = ezdownloader.ezdownloader:main'
        ]
    }
)
