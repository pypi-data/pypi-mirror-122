from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='aadhar_pan_extractor',
  version='0.0.1',
  description='extracts Aadhaar and extracts Pan information',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Deepak Singh Chauhan',
  author_email='deepaksingh0034602@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='aadhar extracts information', 
  packages=find_packages(),
  install_requires=[''] 
)