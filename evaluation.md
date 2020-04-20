April 19th 2020
New evaluation: Precision, Recall, F1 for competition purpose
DEBUG = 0 (exact competition mode)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12', 'cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall precision is: 90.0%
Overall recall is: 90.0%
Overall F1 is: 90.0%

DEBUG = 1 (with putback events)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12', 'cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall precision is: 89.0%
Overall recall is: 86.9%
Overall F1 is: 88.0%

*****************************************************************************************************************************************************************************************

DEBUG = 1 (include putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12', 'cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall products detection rate is: 97.6%
Overall association accuracy is: 97.3%
Overall precision is: 89.0%
Overall recall is: 86.9%


DEBUG = 0 (countereract putback event)

================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12', 'cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall products detection rate is: 100.0%
Overall association accuracy is: 97.8%
Overall precision is: 90.0%
Overall recall is: 90.0%

DEBUG = 1 (include putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall products detection rate is: 100.0%
Overall association accuracy is: 93.8%
Overall precision is: 72.7%
Overall recall is: 72.7%

DEBUG = 0 (countereract putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-19', 'ALL-SIMPLE-CHIP-1', 'TEAM-PEI-1', 'TEAM-PEI-JD-1', 'TEAM-8-1']
Ground truth version:  ground_truth/v12.json
Overall products detection rate is: 120.0%
Overall association accuracy is: 100.0%
Overall precision is: 66.7%
Overall recall is: 80.0%


# TODO Mengmeng: fusion total score
event 560g delta
weight socre productA 530g 70%
weight socre productB 610g 30%
location productA 100%

# DRY RUN
# TODO: ALL-SIMPLE-CHIP-1, 1 person, take one item and put it at another place, not purchasing anything else.
# TODO: TEAM-5-1, 2 people, each take one product at the same time, at the same place, with same same barcode. The db data only lasts for 4 seconds ( 2020-04-18T00:29:37 to 2020-04-18T00:29:41), while the video lasts for 1 min 30 seconds
# TODO: TEAM-8-1, 2 people, person A take 1 bottle water and put it back to a wrong place, then person B bought that mis-placed water.
# TODO: TEAM-PEI-1, 1 person, person A buy 1 item, then another, simple.
# TODO: TEAM-PEI-JD-1, 2 people, take different products at the same time, simple. Planogram is wrong for gondola 3!!!! Need to rely on weight.

# TODO: cps-test-13, 3 people, taken many items. person A pickup product, then give to person B, whose receipt? assume person A
# TODO: cps-test-14, 2 people. Touched many items. Person A pickup product, then put back, at this time personB's head is closer to the put back position.
# TODO: cps-test-15, 2 people, they tend to touch things and put back quickly; they also take items at same time for the same position
# TODO: cps-test-16, 4 people, taken many items
# TODO: cps-test-17, 4 people, taken many items, more complex than test-16. Very close to each other, even the head is very close. Crossing hands. Putback items to wrong places. Touch items at wrong places.
# TODO: cps-test-18, 4 people, taken many items, more complex than test-16. Only use head may be a problem.
# DONE: cps-test-19, 1 person, for item at wrong place caused by test-17, pick it up, then put back to another wrong place?
# TODO: cps-test-20, 1 person, pickup N items at the same time
# TODO: cps-test-21, 1 person, simple.
# TODO: cps-test-22, 1 person, simple.
# TODO: cps-test-23, put back to wrong place N times. Complicated.
# TODO: cps-test-24, 1 person, hold the plate first for a while, then pickup the product.

# TODO: moving window size wrong
# assert (timestamps_count == weight_shelf_mean[i].shape[1])
# assert (timestamps_count == weight_shelf_std[i].shape[1])
# assert (timestamps_count == weight_plate_mean[i].shape[2])
# assert (timestamps_count == weight_plate_std[i].shape[2])

# TODO BASELINE-1: 1 person. Pick 1 item at gondola 3, pick 1 item at gondola 1, pick 1 item at gondola 2.
# TODO BASELINE-2: 1 person. Pick 1 item at gondola 3, pick 1 item at gondola 2, pick 1 item at gondola 1.
# TODO BASELINE-3: 1 person. Pick 1 item at gondola 3, puback; pick 1 item at gondola 2, pick 1 item at gondola 1, pick 1 item at gondola 3.
# TODO BASELINE-4: 1 person. Pick 1 item at gondola 3, pick 3 items at gondola 2 sequentially, putback 1 item to the correct place.
# TODO BASELINE-5 [Difficult]: 1 person. Pick 1 green water at gondola 3, puback to wrong place, where there're red water with same weights; from this place, pickup 1 red water, and the misplaced green water. Pickup 1 item from gondola 1.
# TODO BASELINE-6 [Difficult]: 1 person. Pick 1 big water at gondola 1, put back to wrong place where there're many small water. Pick 2 small water. Pickup 1 item at gondola 3, put back to wrong place at gondola 2, then repick this misplaced item.
# TODO BASELINE-7: 2 people. Each pick some items. May have crossing hands issue.
# TODO BASELINE-8: 2 people. Each pick some items. Stay very close, may have crossing hands issue.
# TODO BASELINE-9: 2 people. Each pick some items. Stay very close, exchange items between them.
# TODO BASELINE-10: 2 people. Simultaneously pickup 1 same item each from the same place. Simultaneously pickup 1 different item each from the same shelf. 
# TODO BASELINE-11: 3 people. Very complicated.
# TODO BASELINE-12: 3 people. Very complicated.