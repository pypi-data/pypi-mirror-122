from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]

setup(
    name='kalicrypt',
    version='1.0.1',
    description='Simple encryption of string values',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    url='',
    author='CoderKali',
    author_email='thecoders4780@outlook.com',
    license='MIT',
    classifiers=classifiers,
    keywords='encryption',
    packages=find_packages(),
    install_requires = ['']    
)
