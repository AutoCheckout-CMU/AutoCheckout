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


# TODO: cps-test-13, person A pickup product, then give to person B, whose receipt? assume person A
# TODO: cps-test-17, 4 people in store, person A pickup a product which is closer to person B's head
# TODO: cps-test-20, pickup N items at the same time
# TODO: cps-test-23, put back to wrong place