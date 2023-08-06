"""
Example usage:

from Binomialdistribution import Binomial
ex = Binomial(.15, 60)
ex.read_data_file('numbers_binomial.txt')
ex.replace_stats_with_data()
"""


import math
import matplotlib.pyplot as plt
from .Generaldistribution import Distribution


class Binomial(Distribution):
    """ Binomial distribution class for calculating and
    visualizing a Binomial distribution.

    Attributes:
        mean (float) representing the mean value of the distribution
        stdev (float) representing the standard deviation of the distribution
        data_list (list of floats) a list of floats to be extracted from the data file
        p (float) representing the probability of an event occurring
        n (int) representing the number of trials

    """
    #       A binomial distribution is defined by two variables:
    #           the probability of getting a positive outcome
    #           the number of trials

    #       If you know these two values, you can calculate the mean and the standard deviation
    #
    #       For example, if you flip a fair coin 25 times, p = 0.5 and n = 25
    #       You can then calculate the mean and standard deviation with the following formula:
    #           mean = p * n
    #           standard deviation = sqrt(n * p * (1 - p))

    def __init__(self, p, n):
        """
        Args:
            p (float) stores the probability of the distribution
            n (int) stores the size of the distribution (num of trials)
        """
        self.p = p
        self.n = n
        mean = self.calculate_mean()
        stdev = self.calculate_stdev()
        Distribution.__init__(self, mean, stdev)  # only extra thing is self.data = []

    def calculate_mean(self):
        """Function to calculate the mean from p and n

        Args:
            None

        Returns:
            float: mean of the data set
        """
        self.mean = self.n * self.p
        return self.mean

    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.

        Args:
            None

        Returns:
            float: standard deviation of the data set

        """
        self.stdev = math.sqrt(self.n*self.p*(1-self.p))
        return self.stdev

    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set

        Args:
            None

        Returns:
            float: the p value
            float: the n value
        """
        # update the p and n attributes of the binomial distribution
        self.n = len(self.data)
        self.p = sum(self.data)/self.n  # num of positive trials divided by the total trials
        # update the mean and standard deviation attributes
        self.calculate_mean()
        self.calculate_stdev()
        return self.p, self.n

    def plot_bar(self):
        """Function to output a histogram of the instance variable data using
        matplotlib pyplot library.

        Args:
            None

        Returns:
            None
        """
        fig, ax = plt.subplots()
        ax.bar(x = ['0', '1'], height = [(1 - self.p) * self.n, self.p * self.n])
        ax.set_title('Bar Chart of Data')
        plt.show()

        return None

    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.

        Args:
            k (float): point for calculating the probability density function


        Returns:
            float: probability density function output
        """
        p = self.p
        n = self.n
        fact = math.factorial  # shorthand for convenience
        return (fact(n)/(fact(k) * fact(n-k))) * (p**k) * (1-p)**(n-k)


    def plot_pdf(self):
        """Function to plot the pdf of the binomial distribution

        Args:
            None

        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot

        """
        x = range(self.n+1)
        y = [self.pdf(k) for k in x]
        fig, ax = plt.subplots()
        ax.bar(x, y)
        ax.set_xlabel('k')
        ax.set_ylabel('density')
        ax.set_title('Pdf of the binomial distribution')
        plt.show()

        return x, y

    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p

        Args:
            other (Binomial): Binomial instance

        Returns:
            Binomial: Binomial distribution

        """

        try:
            assert self.p == other.p, 'p values are not equal'
        except AssertionError as error:
            raise

        result = Binomial(self.p, self.n + other.n)  # mean, stdev computed at the init
        return result

    def __repr__(self):
        """Function to output the characteristics of the Binomial instance

        Args:
            None

        Returns:
            string: characteristics of the Binomial object

        """
        return f'mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}'
