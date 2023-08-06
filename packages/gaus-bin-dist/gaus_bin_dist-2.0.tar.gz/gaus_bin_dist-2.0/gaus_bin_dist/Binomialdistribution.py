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
    
    def __init__(self, p=0, n=0):
        self.p = p
        self.n = n
        Distribution.__init__(self, self.calculate_mean(), self.calculate_stdev())


    def calculate_mean(self):
        """Function to calculate the mean from p and n
        
        Args: 
            None
        
        Returns: 
            float: mean of the data set

        """
        mean = self.p * self.n
        self.mean = mean
        return mean


    def calculate_stdev(self):
        """Function to calculate the standard deviation from p and n.
        
        Args: 
            None
        
        Returns: 
            float: standard deviation of the data set

        """
        stdev = math.sqrt(self.n * self.p * (1 - self.p))
        self.stdev = stdev
        return stdev


    def replace_stats_with_data(self):
        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: p value
            float: n value

        """
        self.n = len(self.data)
        self.p = sum(self.data) / self.n
        self.mean = self.calculate_mean()
        self.stdev = self.calculate_stdev()
        return self.p, self.n


    def plot_histogram(self):
        """Function to output a histogram of the instance variable data using 
        matplotlib pyplot library.
        
        Args:
            None
            
        Returns:
            None

        """
        plt.hist(self.data)
        plt.title('Histogram of Data')
        plt.xlabel('Value')
        plt.ylabel('Count')
        plt.show()


    def pdf(self, k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
            
        """
        a = math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k))
        b = (self.p ** k) * ((1 - self.p) ** (self.n - k))
        return a * b


    def plot_pdf(self):
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            None
            
        """
        x, y = [], []
        for k in range(self.n + 1):
            x.append(k)
            y.append(self.pdf(k))

        plt.bar(x, y)
        plt.title('Distribution of Outcomes')
        plt.xlabel('Outcomes')
        plt.ylabel('Probability')
        plt.show()


    def __add__(self, other):
        """Function to add together two Binomial distributions with equal p
        
        Args:
            other (Binomial): Binomial instance
            
        Returns:
            Binomial: Binomial distribution
            
        """
        assert self.p == other.p, 'p values are not equal'
        
        p = self.p
        n = self.n + other.n
        binomial = Binomial(p, n)
        return binomial


    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """
        return 'mean {}, standard deviation {}, p {}, n {}'.format(self.mean, 
            self.stdev, self.p, self.n)
