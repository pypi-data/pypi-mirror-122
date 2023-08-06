from .Generaldistribution import Distribution
import math
import matplotlib.pyplot as plt

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
    
    #

    # TODO: define the init function
        
        # TODO: store the probability of the distribution in an instance variable p
        # TODO: store the size of the distribution in an instance variable n
        
        # TODO: Now that you know p and n, you can calculate the mean and standard deviation
        #       You can use the calculate_mean() and calculate_stdev() methods defined below along with the __init__ function from the Distribution class
            
    # TODO: write a method calculate_mean() according to the specifications below

    def __init__(self, prob, size, mu = 0, sigma =1 ):
        Distribution.__init__(self, mu, sigma)
        self.p = prob
        self.n = size


    def calculate_mean(self):

        """Function to calculate the mean from p and n

        Args:
        mu:
        sigma:
        data_list:
        p:
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

        variance = self.n * self.p * (1- self.p)

        return math.sqrt(variance)


    # TODO: write a replace_stats_with_data() method according to the specifications below. The read_data_file() from the Generaldistribution class can read in a data
    # file. Because the Binomaildistribution class inherits from the Generaldistribution class,
    # you don't need to re-write this method. However,  the method
    # doesn't update the mean or standard deviation of
    # a distribution. Hence you are going to write a method that calculates n, p, mean and
    # standard deviation from a data set and then updates the n, p, mean and stdev attributes.
    # Assume that the data is a list of zeros and ones like [0 1 0 1 1 0 1]. 
    #
    #       Write code that: 
    #           updates the n attribute of the binomial distribution
    #           updates the p value of the binomial distribution by calculating the
    #               number of positive trials divided by the total trials
    #           updates the mean attribute
    #           updates the standard deviation attribute
    #
    #       Hint: You can use the calculate_mean() and calculate_stdev() methods
    #           defined previously.

    def replace_stats_with_data(self):

        """Function to calculate p and n from the data set. The function updates the p and n variables of the object.
        
        Args: 
            None
        
        Returns: 
            float: the p value
            float: the n value
    
        """
        positive_trials = [i for i in self.data if i > 0]

        self.n = len(self.data)

        self.p = len(positive_trials) / self.n

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

        plt.hist(self.data)

        plt.title("Histogram from Data")

        plt.xlabel("Data")

        plt.ylabel("Frequency")



    def pdf(self,k):
        """Probability density function calculator for the binomial distribution.
        
        Args:
            k (float): point for calculating the probability density function
            
        
        Returns:
            float: probability density function output
        """

        l_fac = (math.factorial(self.n) / (math.factorial(k) * math.factorial(self.n - k)))

        r_fac = self.p**k * (1 - self.p)**(self.n - k)

        prob = l_fac * r_fac

        return prob


    # write a method to plot the probability density function of the binomial distribution

    def plt_bar_pdf(self):
        """Function to plot the pdf of the binomial distribution
        
        Args:
            None
        
        Returns:
            list: x values for the pdf plot
            list: y values for the pdf plot
            
        """
    
        # TODO: Use a bar chart to plot the probability density function from
        # k = 0 to k = n
        
        #   Hint: You'll need to use the pdf() method defined above to calculate the
        #   density function for every value of k.


        #   Be sure to label the bar chart with a title, x label and y label

        x = []
        y = []
        for i in enumerate(range(0, self.n+1)):
            x.append(i[0])
            y.append(self.pdf(i[1]))


        plt.hist(x,y)

        plt.title("Histogram for pdf of Data")

        plt.xlabel("Data")

        plt.ylabel("PDF")


        return x,y



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
        
        # TODO: Define addition for two binomial distributions. Assume that the
        # p values of the two distributions are the same. The formula for 
        # summing two binomial distributions with different p values is more complicated,
        # so you are only expected to implement the case for two distributions with equal p.
        
        # the try, except statement above will raise an exception if the p values are not equal
        
        # Hint: When adding two binomial distributions, the p value remains the same
        #   The new n value is the sum of the n values of the two distributions.

        result = Binomial(self.p, self.n)

        result.n = self.n + other.n

        result.mean = self.p / result.n

        result.stdev = math.sqrt(result.n * self.p * (1 - self.p))

        return result




    def __repr__(self):
        """Function to output the characteristics of the Binomial instance
        
        Args:
            None
        
        Returns:
            string: characteristics of the Binomial object
        
        """

        return f'mean {self.mean}, standard deviation {self.stdev}, p {self.p}, n {self.n} '