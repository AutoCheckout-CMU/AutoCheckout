DEBUG = 1 (include putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12']
Ground truth version:  ground_truth/v10.json
Overall products detection rate is: 96.8%
Overall association accuracy is: 96.6%
Overall precision is: 98.3%
Overall recall is: 95.2%

DEBUG = 0 (countereract putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12']
Ground truth version:  ground_truth/v10.json
Overall products detection rate is: 97.5%
Overall association accuracy is: 97.4%
Overall precision is: 97.4%
Overall recall is: 95.0%

# TODO Yixin: rotation?
# TODO Yixin: adapt weight score!!!

# TODO Leo: 3D/2D?

# TODO Mengmeng: fusion total score
event 560g delta
weight socre productA 530g 70%
weight socre productB 610g 30%
location productA 100%


# TODO: cps-test-13, 3 people, taken many items. person A pickup product, then give to person B, whose receipt? assume person A
# TODO: cps-test-14, 2 people, person A pickup product, then put back, at this time personB's head is closer to the put back position
# TODO: cps-test-15, 2 people, they tend to touch things and put back quickly; they also take items at same time for the same position
# TODO: cps-test-16, 4 people, taken many items
# TODO: cps-test-17, 4 people, taken many items, more complex than test-16. Very close to each other, even the head is very close. Putback items to wrong places. Touch items at wrong places.
# TODO: cps-test-18, 4 people, taken many items, more complex than test-16. Only use head may be a problem.
# TODO: cps-test-19, 1 person, for item at wrong place caused by test-17, pick it up, then put back to another wrong place?
# TODO: cps-test-20, 1 person, pickup N items at the same time
# TODO: cps-test-21, 1 person, simple.
# TODO: cps-test-22, 1 person, simple.
# TODO: cps-test-23, put back to wrong place N times. Complicated.
# TODO: cps-test-24, 1 person, hold the plate first for a while, then pickup the product.