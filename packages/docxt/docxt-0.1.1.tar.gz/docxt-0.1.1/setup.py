#!/usr/bin/env python
# coding: utf-8
from setuptools import setup
setup(
    name='docxt',
    version='0.1.1',
    author='barwe',
    author_email='barwechin@163.com',
    # url='http://barwe.top',
    description='A simple way to generate a report from a template.',
    packages=[
        'docxt',
        'docxt.utils'
    ],
    install_requires=['docxtpl', 'beautifulsoup4'],
    # include_package_data=True,
    # package_data={
    #     "docxt": ['svg2emf.jar']
    # }
    # data_files=[
    #     ('docxt', ['docxt/svg2emf.jar'])
    # ]
)