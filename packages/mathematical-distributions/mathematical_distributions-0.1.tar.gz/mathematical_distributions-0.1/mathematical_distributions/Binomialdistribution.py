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
        n (int) the total number of trials

    """
    
    def __init__(self, prob=.5, size=20):
        self.p = prob
        self.n = size
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())
    
    def calculate_mean(self):
    
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set
    
        """

        return self.p * self.n

    def calculate_stdev(self):

        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set
    
        """

        return math.sqrt(self.n * self.p * (1 - self.p))
        
        
        
    def replace_stats_with_data(self):
    
        """Function to calculate p and n from the data set
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """        

        self.n = len(self.data)
        positives = 0
        for result in self.data:
            if result == 1:
                positives += 1
        self.p = positives / self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n
        
    def plot_bar(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None
        """

        no_positives = no_negatives = 0
        for result in self.data:
            if result == 1:
                no_positives += 1
            else:
                no_negatives += 1
        x_values = [0, 1]
        y_values = [no_negatives, no_positives]
        plt.figure(x_values, y_values, color='blue', width=0.4)
        plt.xlabel("Coin values")
        plt.ylabel("Number of times")
        plt.title("Coin flip results")
        
    def pdf(self, k):
        """Probability density function calculator for the gaussian distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        return (math.factorial(self.n)/(math.factorial(k) * math.factorial(self.n - k))) * (self.p ** k) * ((1 - self.p) ** (self.n - k))

    def plot_bar_pdf(self):

        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """

        x_values = y_values = list()
        for k in range(0, self.n + 1):
            x_values.append(k)
            y_values.append(self.pdf(k))
        plt.figure(x_values, y_values, color='blue', width=0.4)
        plt.xlabel("Num of successes")
        plt.ylabel("Probability")
        plt.title("Probability density function based on number of successes")
        return x_values, y_values
                
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

        result = Binomial()
        result.p = self.p
        result.n = self.n + other.n
        return result

    def __repr__(self):
    
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Gaussian
        
        """

        return f"mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n}"
