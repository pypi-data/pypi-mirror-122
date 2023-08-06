from setuptools import setup
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()


setup(name='Binsearch',
      version='1.1',
      description='Binsearchpy library is created with binary seach algorithm to make the search faster from list data structure',
      author='Dheeraj Kumar',
      long_description_content_type="text/markdown",
      long_description=long_description,
      author_email='engineerdheeraj97@gmail.com',
      license='MIT',
      packages=['Binsearch'],
      keywords=['python', 'Binarysearch', 'algorithm', 'list', 'Binary', 'BinaryList'],
      classifiers=[
              "Development Status :: 1 - Planning",
              "Intended Audience :: Developers",
              "Programming Language :: Python :: 3",
              "Operating System :: Unix",
              "Operating System :: Microsoft :: Windows",
          ],
      zip_safe=False)