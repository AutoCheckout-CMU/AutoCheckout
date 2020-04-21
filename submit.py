from cashier import Cashier
import subprocess
import json
import os

def output_json(db_id, user, receipts, path):
    print ('=======================')
    output = {}
    output['testcase'] = db_id
    output['user'] = user
    receipts_json = []
    for id_result in receipts:
        receipt = receipts[id_result]
        receipt_json = {}
        receipt_json['target_id'] = id_result
        products = []
        for purchase in receipt.purchaseList:
            product = {}
            product['barcode'] = purchase
            product['quantity'] = receipt.purchaseList[purchase][1]
            products.append(product)
        receipt_json['products'] = products
        receipts_json.append(receipt_json)
    output['receipts'] = receipts_json
    with open(path, 'w') as outfile:
        json.dump(output, outfile)

def generate_output():
    # Load JSON
    f = open('competition/day1-tests.json')

    test_cases = json.load(f)
    myCashier = Cashier()
    userID = '5ea023be-b530-4816-8eda-5340cfabe9b0'
    output_paths = []
    for test_db in test_cases:
        print(test_db['name'])
        dbName = test_db['name']
        dbId = test_db['uuid']
        receipts = myCashier.process(dbName)
        # Generate output file
        path = "outputs/output-{}.json".format(dbName)
        output_paths.append(path)
        output_json(dbId, userID, receipts, path=path)

def cal_avg(scores):
    if (len(scores) == 0):
        return None
    total = 0
    for score in scores:
        total += score
    return total / len(scores)

def get_score(output_paths=['outputs/output-BASELINE-1.json']):
    # Send a POST Request
    # command_line = [
    #     'curl', '--location', '--request' ,'POST', '\'cps-week.internal.aifi.io/api/v1/results\'',\
    #     '--header', '\'TOKEN: 5ea023be-b530-4816-8eda-5340cfabe9b0\'',\
    #     '--header', '\'Content-Type: application/json\'',\
    #     '--data-raw'
    # ]
    pre_cmd = 'curl --location --request POST \'cps-week.internal.aifi.io/api/v1/results\' --header \'TOKEN: 5ea023be-b530-4816-8eda-5340cfabe9b0\' --header \'Content-Type: application/json\' --data-raw '
    f1_scores = []
    for path in output_paths:
        with open(path, 'r') as file:
            raw_string = file.read().replace('\n', '')
        cmd = pre_cmd + '\'' + raw_string + '\''
        print("=============== Receive feedbacks for %s ===============" % path)
        # Option 1 Record 
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
        output_dict = json.loads(output)
        f1_scores.append(output_dict['f1_score'])

    print("Average F1 score over all test cases: ", cal_avg(f1_scores))

if __name__ == '__main__':
    output_paths = ['outputs/output-BASELINE-%d.json'%i for i in range(1, 13)]
    # generate_output()
    get_score(output_paths)