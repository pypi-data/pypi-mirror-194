from setuptools import setup, find_packages

setup(
    name='wtday',
    version='0.1.4',
    description='A CLI app that shows you what is celebrated today',
    author='Juan Castillo',
    author_email='cfuendev@gmail.com',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'wtday=wtday.main:main'
        ]
    },
    install_requires=[
        'urllib3',
        'beautifulsoup4',
        'keyboard',
        'colorama',
        'pywin32'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Utilities'
    ],
    python_requires='>=3.6',
)