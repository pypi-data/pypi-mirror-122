from setuptools import setup
import pathlib

HERE = pathlib.Path(__file__).parent

README = (HERE / "README.md").read_text()

setup(name='gauss_binomial_probability',
      version='1.5',
      description='Gaussian and Binomial distributions',
      long_description=README,
      long_description_content_type="text/markdown",
      packages=['gauss_binomial_probability'],
      author= 'Jainish Shah',
      author_email= 'jainishnikul2525@gmail.com',
      zip_safe=False)