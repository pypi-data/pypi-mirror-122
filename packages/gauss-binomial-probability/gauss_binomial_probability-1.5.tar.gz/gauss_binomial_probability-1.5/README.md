# Gaussian-Binomial-distributions package

This package contains the code for calculating the probability density function of gaussian and binomial distribution by providing the data file. From the data file, the package contains two classes called gaussian and binomial which can calculate the further details such as mean and standard deviation from the data file provided (data file should be .txt).
Moreover, the classes can be further use to calculate probability density and plot the respective graphs.And one can use it further for adding two or more Gaussian function or Binomial functions.

# Files

Below is the brief information about the files used:
1. __init__.py is the file for importing the Binomial and Gaussian class from the respective modules

2. General Distribution (`Generaldistribution.py`) - This module of python package contains the code of `class Distribution` for calculating and visualizing a probability distribution. Additionally, there is a method called `read_data_file`, which is the function to read in data from a txt file. The txt file should have one number (float) per line. The numbers are stored in the data attribute.

3. Gaussian Distribution (`Gaussindistribution.py`) - This module contains the class for calculating and visulizing a Gaussian distribution which inherits the properties of Distribution from `Generaldistribution.py`.

4. Binomial Distribution (`Binomialdistribution.py`) - Binomial distribution class for calculating and visualizing a Binomial distribution.

# Installation guide for the package

You can install the gauss-binomial-probability from PyPI:
`pip install gauss_binomial_probability`