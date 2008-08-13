from setuptools import setup, find_packages

setup(name='drosophila_eye_map',
      description='eye map of Drosophila melanogaster',
      author='Andrew Straw',
      author_email='strawman@astraw.com',
      version='0.2', # keep in sync with upload_stuff.sh
      packages = find_packages(),
      )
