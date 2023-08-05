  
from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='klayop',
  version='1.0.1',
  description='Owo, what is this?',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Tejas Patil',
  author_email='tejas1950@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='never gonna give you up', 
  packages=find_packages(),
  install_requires=[''] 
)