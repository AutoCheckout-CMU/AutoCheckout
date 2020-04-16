DEBUG = 1 (include putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12']
Ground truth version:  ground_truth/v10 (test-12 tbd).json
Overall products detection rate is: 100.0%
Overall association accuracy is: 83.0%
Overall precision is: 93.0%
Overall recall is: 93.0%

DEBUG = 0 (countereract putback event)
================== Evaluation Summary ==================
Databases:  ['cps-test-01', 'cps-test-2', 'cps-test-4', 'cps-test-5', 'cps-test-6', 'cps-test-7', 'cps-test-8', 'cps-test-9', 'cps-test-10', 'cps-test-11', 'cps-test-12']
Ground truth version:  ground_truth/v10 (test-12 tbd).json
Overall products detection rate is: 102.9%
Overall association accuracy is: 81.2%
Overall precision is: 88.9%
Overall recall is: 91.4%

# TODO Leo: ground truth 3
# TODO Leo: adjust association
# TODO Yixin: adapt weight score


# TODO: cps-test-13, person A pickup product, then give to person B, whose receipt?
# TODO: cps-test-17, 4 people in store, person A pickup a product which is closer to person B's head
# TODO: cps-test-20, pickup N items at the same time
# TODO: cpst-test-23, put back to wrong place