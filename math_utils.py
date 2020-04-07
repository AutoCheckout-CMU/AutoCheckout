import numpy as np
import math
import scipy.stats as ss

def areaUnderTwoGaussians(mu1, sigma1, mu2, sigma2):
    # Find the intersection of both pdf's -> We used:
    # syms x mu1 sigma1 mu2 sigma2
    # solve(exp(-(x-mu1)**2/(2*sigma1**2))/(sigma1*sqrt(2*pi)) == exp(-(x-mu2)**2/(2*sigma2**2))/(sigma2*sqrt(2*pi)), x)
    if sigma1 == sigma2: # Only one intersection point
        xSol = (mu1**2 - mu2**2)/(2*mu1 - 2*mu2)
        if np.isnan(xSol):
            xSol = mu1
        xEv = xSol - 1
        if normpdf(xEv, mu1, sigma1) < normpdf(xEv, mu2, sigma2):
            A = ss.norm.cdf(xSol, mu1, sigma1) + ss.norm.cdf(xSol, mu2, sigma2, 'upper')
        else:
            A = ss.norm.cdf(xSol, mu2, sigma2) + ss.norm.cdf(xSol, mu1, sigma1, 'upper')
    else:
        # xSol = np.zeros(1, 2)
        xSol = [[(mu2*sigma1**2 - mu1*sigma2**2 + sigma1*sigma2*(2*sigma2**2*math.log(sigma2/sigma1) - 2*sigma1**2*math.log(sigma2/sigma1) - 2*mu1*mu2 + mu1**2 + mu2**2)**(1/2))/(sigma1**2 - sigma2**2)],
                [-(mu1*sigma2**2 - mu2*sigma1**2 + sigma1*sigma2*(2*sigma2**2*math.log(sigma2/sigma1) - 2*sigma1**2*math.log(sigma2/sigma1) - 2*mu1*mu2 + mu1**2 + mu2**2)**(1/2))/(sigma1**2 - sigma2**2)]]
        if xSol[1] > xSol[2]:
            xSol.reverse()
        xEv = sum(xSol)/2
        if normpdf(xEv, mu1, sigma1) > normpdf(xEv, mu2, sigma2):
            muEnds = mu1
            sigmaEnds = sigma1
            muMiddle = mu2
            sigmaMiddle = sigma2
        else:
            muEnds = mu2
            sigmaEnds = sigma2
            muMiddle = mu1
            sigmaMiddle = sigma1
        A = ss.norm.cdf(xSol[1], muEnds, sigmaEnds) + np.diff(ss.norm.cdf(xSol, muMiddle, sigmaMiddle)) + ss.norm.cdf(xSol[2], muEnds, sigmaEnds, 'upper')
    
    if A > 1:
        A = 0
    return A

def normpdf(x, mu, sigma):
    return 1/(sigma*math.sqrt(2*math.pi))*math.exp(-1*(x-mu)**2/2*sigma**2)