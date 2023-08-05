from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='LIST_OF_LOCATIONS',
    version='0.0.1',
    description='A tool for the location of the techmanpy robot',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='Arjan van der Knaap',
    author_email='18103677@student.hhs.nl',
    license='MIT',
    classifiers=classifiers,
    keywords='Techmanpy',
    packages=find_packages(),
    install_requires=['Techmanpy']
)