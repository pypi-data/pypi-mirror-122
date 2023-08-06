#!/usr/bin/env python

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

setup(name="scalefree-target-s3-json",
      version="0.1",
      description="Singer.io target for writing JSON files and upload to S3",
      long_description=long_description,
      long_description_content_type='text/markdown',
      author="Scalefree GmbH",
      url='https://github.com/ScalefreeCOM/scalefree-target-s3-json',
      download_url = 'https://github.com/ScalefreeCOM/scalefree-target-s3-json/archive/refs/tags/v_01.tar.gz',
      classifiers=[
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3 :: Only'
      ],
      py_modules=["target_s3_json"],
      install_requires=[
          'pipelinewise-singer-python==1.*',
          'inflection==0.5.1',
          'boto3==1.17.39',
      ],
      extras_require={
          "test": [
              'pylint==2.10.*',
              'pytest==6.2.*',
              'pytest-cov==2.12.*',
              'nose==1.3.7'
          ]
      },
      entry_points="""
          [console_scripts]
          target-s3-json=target_s3_json:main
       """,
      packages=["target_s3_json"],
      package_data = {},
      include_package_data=True,
)
