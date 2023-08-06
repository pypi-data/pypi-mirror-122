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
  version='1.0.4',
  description='Easy to use Neural AI Tool',
  author='DanishDeveloper',
  license='MIT', 
  classifiers=classifiers,
  keywords='nait', 
  packages=['nait'],
  install_requires=['numpy'] 
)