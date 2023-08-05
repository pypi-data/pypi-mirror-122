import continuous_distributions as st
import mle 

class norm_ci(st.Norm_rv):

    def __init__(self, mean=0, variance=1, data=[], alpha=0.05, estimate='variance'):
        
        """
        Initialize a normal random variable hypothesis test class

        Parameters
        ----------
        
        mean : float / int, mean of normal distribution 
        
        variance : float / int, var of normal distribution 
        
        data : array-like, a list of data to draw from. 
        
        estimate : str, mean or variance, default = mean
        
        Returns
        ---------
        None
        
        Notes
        ---------
        subclass of continuous_distributions.Norm_rv
        
        """

        #look at example p 1/27 CI notes
        
        #this is maybe a bad way to get around the limitations of the base 
        #normal_rv class but it works for now 
        if estimate == 'variance': 
            super().__init__(mean,variance)
            
            #is this a "given" value? should this just be supplied by user? 
            #is this just the mean..? since it's the MLE for mean? 
            self.x_bar = mle.normal(data)[0]
            self.variance = None 
        elif estimate == 'mean': 
            super().__init__(mean,variance)
            self.var_hat = mle.normal(data)[1]
            self.mean = None
        else:
            raise ValueError('enter either mean or variance for estimate arg')

        if 0 <= alpha <= 1: 
            self._alpha = alpha
        else: 
            raise ValueError('alpha must be between 0 and 1')
        
        #lower lim = L = L(x1,...xn)
        #upper lim = U = U(x1,...,xn) 
        #such that P(L <= theta <= U) = 1 - alpha 
        #where theta is the param being estimated 
