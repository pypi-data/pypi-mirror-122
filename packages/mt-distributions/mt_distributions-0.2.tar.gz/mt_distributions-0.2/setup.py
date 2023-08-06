from setuptools import setup

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "mt_distributions" / "README.md").read_text()

setup(name='mt_distributions',
      version='0.2',
      description='Gaussian and Binomial distributions, made for the Udacity Machine Learning Foundations course',
      packages=['mt_distributions'],
      long_description=long_description,
      long_description_content_type='text/markdown',
      zip_safe=False)