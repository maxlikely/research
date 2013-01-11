import math

def binomial_log_likelihood(p, k, n):
    '''
    Returns binomial log-likelihood with
        probability p
        k successes
        n trials
    '''
    return k * math.log(p, 2) + (n - k) * math.log(1 - p, 2) # log base-2

def binomial_log_lambda(k1, k2, n1, n2):
    '''
    Returns the log_lambda statistic for two hypothesis.
    '''
    l = binomial_log_likelihood

    p = (k1 + k2) / float(n1 + n2)
    p1 = k1 / float(n1)
    p2 = k2 / float(n2)

    return l(p, k1, n1) + l(p, k2, n2) - l(p1, k1, n1) - l(p2, k2, n2)

#from scipy import stats
#EPS = 10e-16
#def binomial_pdf(k, n, p):
#    '''
#    pdf of the binomial with
#        k successes
#        n trials
#        p probability
#    '''
#    return stats.binom.pmf(k,n,p) + EPS
#
#def LLR(h1, h2):
#    '''
#    Returns log-likelihood ratio of two hypothesis, H1 and H2
#    '''
#    return math.log(h1 / h2, 2) # log base-2


