from setuptools import setup, find_packages
classifiers =[
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Education',
    'Operating System :: Microsoft :: Windows :: Windows 10',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    
    
    
]
setup(
name ='shal_example_pkg',
version = '0.0.1',
description = 'a simple calculaion',
#long_description =open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
long_description_content_type='text/markdown',
url='',
author = 'shalini_v',
author_email = 'shalinivenkatesh450@gmail.com',
license='MIT',
classifiers=classifiers,
keywords='calculator',
packages=find_packages(),
install_reuires=['']
)