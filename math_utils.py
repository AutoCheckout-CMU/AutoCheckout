import numpy as np
import math
from scipy.stats import norm
import BookKeeper as BK


def areaUnderTwoGaussians(m1, std1, m2, std2):
    if m1 > m2:
        (m1, std1, m2, std2) = (m2, std2, m1, std1) 
    a = 1/(2*std1**2) - 1/(2*std2**2)
    b = m2/(std2**2) - m1/(std1**2)
    c = m1**2 /(2*std1**2) - m2**2 / (2*std2**2) - np.log(std2/std1)
    pointOfIntersect = np.roots([a,b,c])[0]
    area = norm.cdf(pointOfIntersect,m2,std2) + (1.-norm.cdf(pointOfIntersect,m1,std1))
    
    return area




"""
Function to calculate distance of two 3D coordinates
"""
def calculate_distance3D(loc_a, loc_b):
    return math.sqrt((loc_a.x - loc_b.x)**2 + (loc_a.y - loc_b.y)**2 + (loc_a.z - loc_b.z)**2)
