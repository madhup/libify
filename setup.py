from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='libify',
      version='0.78',
      author='Madhup Sukoon',
      author_email='29144316+vagrantism@users.noreply.github.com',
      description='Import Databricks notebooks as libraries/modules',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/vagrantism/libify',
      license='MIT',
      packages=['libify'],
      classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.5',
    zip_safe=False)
