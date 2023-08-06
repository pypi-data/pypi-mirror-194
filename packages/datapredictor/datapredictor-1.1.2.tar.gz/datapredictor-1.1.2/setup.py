from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='datapredictor',
  version='1.1.2',
  description='This packet is predict data!',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Umidyor',
  author_email='umidyor007@hmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='data predict', 
  packages=find_packages(),
  install_requires=['scikit-learn==1.2.1','numpy==1.24.2',"pandas==1.5.3"] 
)
