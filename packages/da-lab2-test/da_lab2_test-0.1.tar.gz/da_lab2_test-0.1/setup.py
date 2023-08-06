from setuptools import find_packages, setup


setup(name='da_lab2_test',

      version='0.1',

      author='Dmitriy Kolchin',

      author_email='284594@niuitmo.ru',

      description='Test numpy implementation for DA LAB2',

      packages=find_packages(),

      zip_safe=False,

      setup_requires=['numpy<=1.21.0'])