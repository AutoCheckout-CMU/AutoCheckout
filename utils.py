import BookKeeper as BK
from math_utils import *

"""
Helper functions to associate targets to a product with head ONLY
Input:
    product_loc: Coordinates of product location (global coordinate)
    targets: Dictionary of target IDs and Target object
Returns:
    id (String): result target id
    target (Target object): result Target object
"""
def associate_product_naive(product_loc, targets):
    result_id = None
    result_target = None
    min_dist = float('inf')
    for id, target in targets.items():
        distance = calculate_distance3D(target.head, product_loc)
        if (distance < min_dist):
            result_id = id
            result_target = target
    return result_id, result_target
