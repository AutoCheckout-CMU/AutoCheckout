import BookKeeper as BK
from math_utils import *

BODY_THRESH = 0.8 

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
        if total_score == 0:
            ce_distance = float('inf')
        else:
            ce_distance /= total_score
            
        # print("Distance for target: ", id, "is: ", str(ce_distance))
        if (ce_distance <= min_dist):
            result_id = id
            result_target = target
            min_dist = ce_distance
    # print("Result ID: ", result_id)
    return result_id, result_target

"""
Helper functions to associate targets to a product with the possible closest body part
Input:
    product_loc: Coordinates of product location (global coordinate)
    targets: Dictionary of target IDs and Target object
Returns:
    id (String): result target id
    target (Target object): result Target object
"""
def associate_product_closest(product_loc, targets):
    result_id = None
    result_target = None
    min_dist = float('inf')
    for id, target in targets.items():
        closest_dist = float('inf')
        if target.head is not None:
            head, score = target.head['position'], target.head['score']
            # print("head dist", calculate_distance3D(head, product_loc), "score", score)
            if (score > BODY_THRESH):
                closest_dist = min(calculate_distance3D(head, product_loc), closest_dist)
        if target.left_hand is not None:
            left_hand, score = target.left_hand['position'], target.left_hand['score']
            # print("left_hand dist", calculate_distance3D(left_hand, product_loc), "score", score)
            if (score > BODY_THRESH):
                closest_dist = min(calculate_distance3D(left_hand, product_loc), closest_dist)
        if target.right_hand is not None:
            right_hand, score = target.right_hand['position'], target.right_hand['score']
            # print("right_hand dist", calculate_distance3D(right_hand, product_loc), "score", score)
            if (score > BODY_THRESH):
                closest_dist = min(calculate_distance3D(right_hand, product_loc), closest_dist)
            
        # print("Closest distance for target: ", id, "is: ", str(closest_dist))
        if (closest_dist <= min_dist):
            result_id = id
            result_target = target
            min_dist = closest_dist
    # print("Result ID: ", result_id)
    if (not result_id or not result_target):
        result_id, result_target = targets.items[0]
    return result_id, result_target
