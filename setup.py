from setuptools import setup
import flaskstrap
with open('requirements.txt') as r:
      requirements = r.read().splitlines()
setup(name='flaskstrap',
      version=flaskstrap.__version__,
      description='basic ansible bootstrap method',
      url='http://github.com/martyni/flaskstrap',
      author='martyni',
      author_email='martynjamespratt@gmail.com',
      license='MIT',
      packages=['flaskstrap'],
      install_requires=requirements,
      zip_safe=False,
      entry_points = {
         'console_scripts': ['flaskstrap=flaskstrap.app:main'],
      },
      include_package_data=True
      )

