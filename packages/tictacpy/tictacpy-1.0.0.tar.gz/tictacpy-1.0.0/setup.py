from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

readme = ''
with open('README.md') as f:
    readme = f.read()
 
setup(
  name='tictacpy',
  version='1.0.0',
  description='Play tic tac toe with friends',
  long_description=readme,
  url='https://github.com/ImpassiveMoon03/tictacpy',  
  author='Robert Offord',
  author_email='impassivedeveloper@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Tictactoe', 
  packages=find_packages(),
  install_requires=[''] 
)