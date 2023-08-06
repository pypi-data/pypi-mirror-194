from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='chemdatabase',
  version='0.0.8',
  description='Save your chemicals with their properties by ust drawing them in google sheet and retrive them with their smailr',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Ahmed Alhilal',
  author_email='aalhilal@kfu.edu',
  license='MIT', 
  classifiers=classifiers,
  keywords='chemiformatics, chemical_database',
  packages=find_packages(),
  install_requires=['requests',"rdkit", "pubchempy", "ipywidgets","IPython","panel-chemistry", ])

