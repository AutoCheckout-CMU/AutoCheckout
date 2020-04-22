# competition score + dry run
================== Evaluation Summary ==================
Databases:  ['BASELINE-1', 'BASELINE-2', 'BASELINE-3', 'BASELINE-4', 'BASELINE-5', 'BASELINE-6', 'BASELINE-7', 'BASELINE-8', 'BASELINE-10', 'BASELINE-11', 'BASELINE-12', 'BASELINE-14']
Ground truth version:  ground_truth/v14.json
Overall precision is: 82.0%
Overall recall is: 83.7%
Overall F1 is: 82.8%

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

# TODO BASELINE-13[Urgent]: 0.66. 1 person. Pick up two very close but different product.
# TODO BASELINE-14[Urgent]: 0.66. 1 perosn. Very simple case, not sure why wrong.
# TODO BASELINE-15: 1.0. 1 person. Simple.
# TODO BASELINE-16: 0.28. 1 person. Misplaced items and close weight.
# TODO BASELINE-17: 0.33. 1 person. Hold an item for very long time and pick it up.
# TODO BASELINE-18: 0.5. 1 person. At the same pick up one water A at plate 3, 2 waters B at plate 6. Same shelf. Then put back B at A's place, they are same weight, so difficult.
# TODO BASELINE-19: 0.8. 1 person. Pickup 3 chips A, two chips B, one chip C. Put back one 1 chip A to its original place.
# TODO BASELINE-20[Urgent]: 0.0. 1 person. Pick up three very close but different product, then putback one.
# TODO BASELINE-21: 0.71. 1 person. Very quickly pick up N close items one by one, then putback one.
# TODO BASELINE-22: 0.25. 1 person. Slowly pickup 1 item.
# TODO BASELINE-23[Urgent]: 0.66. 1 person. Putback item and retake, should be simple.
# TODO BASELINE-24[Urgent]: 0.75. 1 person. Pick up two very close but different product.
# TODO BASELINE-25: 1.0. 1 person. Pick 4 items, one by one, simple.
# TODO BASELINE-26: 1.0. 1 person. Pickup 2 same products adjacent plates.
# TODO BASELINE-27: 1.0. 1 person. Pickup and put back.
# TODO BASELINE-28: 0.12. 1 person. Hold 2 items on shelf for a long time, then only pick up 1.
# TODO BASELINE-29: 0.85. 1 person. Pick up adjacent items quickly.
# TODO BASELINE-30: 0.66. 1 person. Pick 3 items, leave 1 at floor.