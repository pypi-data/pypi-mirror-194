from setuptools import setup, find_packages

setup(
    name='wtday',
    version='0.1.0',
    description='A CLI app that shows you what is celebrated today',
    packages=find_packages(),
    install_requires=[
        'urllib3',
        'beautifulsoup4',
        'keyboard',
        'colorama',
        'pywin32'
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)