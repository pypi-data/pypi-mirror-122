from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: OS Independent',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='absotone-melz',
    version='0.0.4',
    description='A machine learning library for everyone!',
    long_description=open('README.md').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='https://github.com/absotone/melz',
    author='Vijay Jaisankar',
    author_email='vijayjaisankar.vj@gmail.com',
    license='MIT',
    classifiers=classifiers,
    keywords='ML',
    packages=find_packages(),
    install_requires = ['numpy','pandas','matplotlib','seaborn']
)