from setuptools import find_packages, setup


setup(name='dalab2test',

      version='0.3',

      author='Dmitriy Kolchin',

      author_email='284594@niuitmo.ru',

      description='Test numpy implementation for DA LAB2',

      packages=find_packages(),

      zip_safe=False,

      setup_requires=['numpy<1.17.3'])