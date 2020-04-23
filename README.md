# MPS: Multi-Person Shopping for Cashier-Less Store
This project shares our solution for AiFi's CPS-IoT Autocheckout [Competition](https://www.aifi.io/research). We're the winner: Team 3!
- Authors: [Yixin Bao](https://www.linkedin.com/in/yixinbao/), [Xinyue Cao](https://www.linkedin.com/in/xinyuecao/), [Chenghui Li](https://www.linkedin.com/in/leochli/), [Mengmeng Zhang](https://www.linkedin.com/in/zhangmengmeng/)
- Affiliation: Carnegie Mellon University, U.S.

![team3](competition/team3.gif)
## Sample Data

- Download Videos [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-videos.gz) (17.1MB)

- Download Data without Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-nodepth.archive) (239MB)

- Download Data with Depth Images [Here](https://storage.googleapis.com/aifi-public-data/AiFi%20Nanostore%20AutoCheckout%20Competition%20-%20CPS-IoT%20Week%202020/cps-test-01/cps-test-01-all.archive) (2.0GB)

- The complete public datasets available at http://aifi.io/research under Sample Data.

- To import the data into mongodb: 
```
mongorestore --archive="cps-test-01-nodepth.archive"
```

## Installation
```
pip3 install -r requirements.txt
```

## Get started
To test one single testcase:
```python
python3 test.py
```
To get more detaild log, change in `config.py`:
```bash
VERBOSE = 1
```
To test it against the competition API:
```
python3 submit.py
```

## Ground truth
For most of testcases in public dataset and the competition datast, we have manually labeled the [ground truth](https://github.com/AutoCheckout-CMU/AutoCheckout/tree/master/ground_truth). 
