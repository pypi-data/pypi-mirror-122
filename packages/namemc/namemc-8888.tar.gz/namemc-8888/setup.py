from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='namemc',
  version='8888',
  description="It's just a name snipe.",
  long_description=open('README.md').read(),
  long_description_content_type='text/markdown',
  author='kggn',
  license='MIT', 
  classifiers=classifiers,
  keywords=[],
  packages=find_packages(),
  install_requires=[]
)
