from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='Discord bot package',
  version='0.0.1',
  description='This library helps you code a discord bo with few lines.',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Basha coder',
  author_email='adam.webtools@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='discord bot', 
  packages=find_packages(),
  install_requires=['discord'] 
)