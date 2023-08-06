from setuptools import setup, find_packages
setup(
name='my-ctl',
version='1.0.1',
description='Python Project Template',
author_email='1406046087@qq.com',
author='yuanmingzhuo',
license='LABELNET',
keywords=['my-ctl'],
packages=find_packages(),
include_package_data=True,
install_requires=['click==8.0.3', 'twine==3.5.0', 'nuitka==0.6.17.5', 'requests==2.25.1', 'pytest==6.2.5'],
python_requires='>=3.8',
entry_points="""
[console_scripts]
myctl=my_ctl:cli
"""
)