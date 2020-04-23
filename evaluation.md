# competition score + dry run
================== Evaluation Summary ==================
Databases:  ['BASELINE-1', 'BASELINE-2', 'BASELINE-3', 'BASELINE-4', 'BASELINE-5', 'BASELINE-6', 'BASELINE-7', 'BASELINE-8', 'BASELINE-10', 'BASELINE-11', 'BASELINE-12', 'BASELINE-13', 'BASELINE-14', 'BASELINE-20', 'BASELINE-22', 'BASELINE-23', 'BASELINE-25']
Ground truth version:  ground_truth/v14.json
Overall precision is: 82.2%
Overall recall is: 90.9%
Overall F1 is: 86.3%

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


# BASELINE-1: 1.0. 1 person. Pick 1 item at gondola 3, pick 1 item at gondola 1, pick 1 item at gondola 2.
# BASELINE-2: 1.0. 1 person. Pick 1 item at gondola 3, pick 1 item at gondola 2, pick 1 item at gondola 1.
# BASELINE-3: 1.0. 1 person. Pick 1 item at gondola 3, puback; pick 1 item at gondola 2, pick 1 item at gondola 1, pick 1 item at gondola 3.
# BASELINE-4: 1.0. 1 person. Pick 1 item at gondola 3, pick 3 items at gondola 2 sequentially, putback 1 item to the correct place.
# BASELINE-5 0.67. [Vision]: 1 person. Pick 1 green water at gondola 3, puback to wrong place, where there're red water with same weights; from this place, pickup 1 red water, and the misplaced green water. Pickup 1 item from gondola 1.
# BASELINE-6 1.0. : 1 person. Pick 1 big water at gondola 1, put back to wrong place where there're many small water. Pick 2 small water. Pickup 1 item at gondola 3, put back to wrong place at gondola 2, then repick this misplaced item.
# BASELINE-7 1.0.: 2 people. Each pick some items. May have crossing hands issue.
# BASELINE-8 0.83. [Todo]: 2 people. Each pick some items. Stay very close, may have crossing hands issue.
# BASELINE-9 0.5. [Difficult, Vision]: 2 people. Each pick some items. Stay very close, exchange items between them.
# BASELINE-10 0.67 [Difficult].: 2 people. Simultaneously pickup 1 same item each from the same place. Simultaneously pickup 1 different item each from the same shelf. 
# BASELINE-11 1.0.: 3 people. Very complicated.
# BASELINE-12 0.28. [Todo]: 3 people. Very complicated.
# BASELINE-13: 1.0. 1 person. Pick up two very close but different product.
# BASELINE-14: 1.0. 1 perosn. Very simple case, not sure why wrong.
# BASELINE-15: 1.0. 1 person. Simple.
# BASELINE-16: 0.8. [Todo] 1 person. Misplaced items and close weight.
# BASELINE-17: 0.33 [Urgent]. 1 person. Hold an item for very long time and pick it up.
# BASELINE-18: 0.5. 1 person. At the same pick up one water A at plate 3, 2 waters B at plate 6. Same shelf. Then put back B at A's place, they are same weight, so difficult.
# BASELINE-19: 0.8  [Urgent]. 1 person. Pickup 3 chips A, two chips B, one chip C. Put back one 1 chip A to its "original place".
# BASELINE-20: 1.0. 1 person. Pick up three very close but different product, then putback one.
# BASELINE-21: 0.85. 1 person. Very quickly pick up N close items one by one, then putback one.
# BASELINE-22: 0.28 [Urgent]. 1 person. Slowly pickup 1 item.
# BASELINE-23: 1.0. 1 person. Putback item and retake, should be simple.
# BASELINE-24: 1.0. 1 person. Pick up two very close but different product.
# BASELINE-25: 1.0. 1 person. Pick 4 items, one by one, simple.
# BASELINE-26: 1.0. 1 person. Pickup 2 same products adjacent plates.
# BASELINE-27: 1.0. 1 person. Pickup and put back.
# BASELINE-28: 0.12 [Urgent] 1 person. Hold 2 items on shelf for a long time, then only pick up 1.
# BASELINE-29: 1.0. 1 person. Pick up adjacent items quickly.
# BASELINE-30: 0.80. 1 person. Pick 3 items, leave 1 at floor.

# TEAM-3-DAY-1-TEST-1 0.75： suggest not included.
# TEAM-3-DAY-1-TEST-2 1.0:
# TEAM-3-DAY-1-TEST-3 1.0:
# TEAM-3-DAY-1-TEST-4 1.0:
# TEAM-3-DAY-1-TEST-5 1.0:

# TEAM-3-DAY-2-TEST-1. 1.0: empty receipt
# TEAM-3-DAY-2-TEST-2: 1.0.
# TEAM-3-DAY-2-TEST-3: 1.0.

# BENCHMARK-1: 1.0.
# BENCHMARK-2: 1.0.

# TEAM-99-DAY-2-TEST-1: 0.62 [Todo]