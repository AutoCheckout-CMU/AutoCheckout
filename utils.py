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
        distance = calculate_distance3D(target.head['position'], product_loc)
        # print("Distance for target: ", id, "is: ", str(distance))
        if (distance < min_dist):
            result_id = id
            result_target = target
            min_dist = distance
    # print("Result ID: ", result_id)
    return result_id, result_target

"""
Helper functions to associate targets to a product with head and hands
Input:
    product_loc: Coordinates of product location (global coordinate)
    targets: Dictionary of target IDs and Target object
Returns:
    id (String): result target id
    target (Target object): result Target object
"""
def associate_product_ce(product_loc, targets):
    result_id = None
    result_target = None
    min_dist = float('inf')
    for id, target in targets.items():
        ce_distance = 0
        total_score = 0
        if target.head is not None:
            head, hscore = target.head['position'], target.head['score']
            ce_distance += calculate_distance3D(head, product_loc)*hscore
            total_score += hscore
        if target.left_hand is not None:
            left_hand, lscore = target.left_hand['position'], target.left_hand['score']
            ce_distance += calculate_distance3D(left_hand, product_loc)*lscore
            total_score += lscore
        if target.right_hand is not None:
            right_hand, rscore = target.right_hand['position'], target.right_hand['score']
            ce_distance += calculate_distance3D(right_hand, product_loc)*rscore
            total_score += rscore
        ce_distance /= total_score
        
        # print("Distance for target: ", id, "is: ", str(distance))
        if (ce_distance < min_dist):
            result_id = id
            result_target = target
            min_dist = ce_distance
    # print("Result ID: ", result_id)
    return result_id, result_target

