import math as m
import random as r

import continuous_distributions as st

#following examples on p. 11 / 31 of hyp testing notes 
class norm_hyp(st.Norm_rv):

    def __init__(self, mean, variance, H0, HA, test_type='simple'):
        
        """
        Initialize a normal random variable hypothesis test class

        Parameters
        ----------
        data : array-like, a list of data to draw from. 

        H0 : str, the null hypothesis to test. This does not have to be
        anything in particular as of right now.
        
        HA : str, the alternative hypotethis to test
        
        test_type : str, simple or complex, defaults=simple
        
        Returns
        ---------
        None
        
        Notes
        ---------
        
        """

        # might not want a mean if that's what we're testing,
        # we wouldn't know the mean in advance
        super().__init__(mean, variance)

        #new values of subclass
        self.std_dev = m.sqrt(variance)
        self.H0 = H0
        self.HA = HA
        self.type = test_type # simple or compound test

    def z_score(self, x):

        """Calculate a z score
        
        Parameters
        ----------
        data : array-like, a list of data to draw from. 

        H0 : str, the null hypothesis to test. This does not have to be
        anything in particular as of right now.
        
        HA : str, the alternative hypotethis to test
        
        test_type : str, simple or complex, defaults=simple
        
        Returns
        ---------
        None
        
        Notes
        ---------  
        
        
        """

        self.z = (x - self.mean) / (self.variance)
        return self.z

#unfinished, come back to this at some point

# based on example on p. 2 of hyp testing notes
class gen_test:

        def __init__(self, data, H0):

            """
            Initialize a general hypothesis test class

            Parameters
            ----------
            data : array-like, a list of data to draw from. 

            H0 : string, the null hypothesis to test. This does not have to be
            anything in particular as of right now.
            
            Returns
            ---------
            None
            
            Notes
            ---------
            I based this on something simple like the classic probability 
            problem of drawing marbles from a bag and seeing how many were of 
            a certain color.
            
            """

            self.data = list(data)
            self.H0 = H0

        def run_test(self, n, counter, accept_left, accept_right):

            """
            Run a general hypothesis test.

            Parameters
            ----------
            n : int, the number of samples to draw

            counter : str, the 'object' you want to count. For example, with a
            data set like ['R', 'B', 'R'] for red and blue marbles, to count
            red marbles, counter='R'

            accept_left : int, the left bound of the acceptance region

            accept_right : int, the right bound of the acceptance region

            Returns:
            ----------
            decision : str, the decision made based on the sample drawn
            
            Notes
            ----------
            """

            sample = r.sample(self.data, n)
            acceptance_region = {accept_left, accept_right}
            rejection_region = (set(i for i in range(1, len(self.data)))
                                .symmetric_difference(acceptance_region))
            sample_count = sample.count(counter)

            if sample_count in acceptance_region:
                decision = (
                    f'Do not reject the null hypothesis of : {self.H0}. Count'
                    f' is {sample_count}'
                    )
            if sample_count in rejection_region:
                decision = (
                    f'Reject the null hypothesis of {self.H0}.'
                    f' Count is {sample_count}'
                    )
            return decision
