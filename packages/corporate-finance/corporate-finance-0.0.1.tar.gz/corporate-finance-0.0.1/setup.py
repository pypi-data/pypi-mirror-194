import io
from os import path
from setuptools import setup, find_packages
 
# --- get version ---
with open("corporate-finance/version.py") as f:
    line = f.read().strip()
    version = line.replace("version = ", "").replace('"', '')

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with io.open(path.join(here, 'corporate-finance/README.txt'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name='corporate-finance',
  version=version,
  description='A comprehensive library for corporate finance in Python',
  long_description=long_description,
  author='Hemant Thapa',
  author_email='hemantthapa1998@gmail.com',
  url='https://github.com/harryworlds/corporate-finance',
  license='MIT', 
  classifiers = [ 'Development Status :: 5 - Production/Stable',
                  'Intended Audience :: Education',  
                  'Operating System :: Microsoft :: Windows :: Windows 10',  
                  'Operating System :: MacOS :: MacOS X',  
                  'License :: OSI Approved :: MIT License',  
                  'Programming Language :: Python :: 3.6',
                  'Programming Language :: Python :: 3.7',
                  'Programming Language :: Python :: 3.8',
                  'Programming Language :: Python :: 3.9',
                  'Programming Language :: Python :: 3.10',
                ],
  keywords='corporate finance, pandas, yahoo finance, numpy, pandas datareader, seaborn, matplotlib', 
  packages=find_packages(),
  install_requires=['pandas>=1.3.0', 'numpy>=1.16.5',
                      'requests>=2.26', 'seaborn>=0.11.0',
                      'yfinance>=0.2.0', 'matplotlib>=3.4.0']
)



"""
NOTE:
corporate finance is not affiliated, endorsed, or vetted by any sponser, Inc.
It is for eductional purpose and tools to leverage your financial knowledge.

"""