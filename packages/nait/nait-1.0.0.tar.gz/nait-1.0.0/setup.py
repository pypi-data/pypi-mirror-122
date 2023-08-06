from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='nait',
  version='1.0.0',
  description='Easy to use Neural AI Tool',
  #long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  #url='',  
  author='DanishDeveloper',
  #author_email='',
  license='MIT', 
  classifiers=classifiers,
  keywords='nait', 
  packages=find_packages(),
  install_requires=['numpy'] 
)