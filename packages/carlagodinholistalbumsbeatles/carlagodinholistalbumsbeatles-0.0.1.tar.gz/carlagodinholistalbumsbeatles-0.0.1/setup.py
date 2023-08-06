from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 11',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3.11'
]
 
setup(
  name='carlagodinholistalbumsbeatles',
  version='0.0.1',
  description='Shows the list of The Beatles Albums',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='Carla Sónia Godinho',
  author_email='carlasoniagodinho4@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='list albums', 
  packages=find_packages(),
  install_requires=[''] 
)