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
    f = open('competition/test_cases.json')

    test_cases = json.load(f)
    myCashier = Cashier()
    userID = '5ea023be-b530-4816-8eda-5340cfabe9b0'
    output_paths = []
    for test_db in test_cases:
        print(test_db['name'])
        dbName = test_db['name']
        if ('DAY-1' in dbName and 'TEAM-3' not in dbName):
            continue
        dbId = test_db['uuid']
        receipts = myCashier.process(dbName)
        # Generate output file
        path = "outputs/output-{}.json".format(dbName)
        output_paths.append(path)
        output_json(dbId, userID, receipts, path=path)
    return output_paths

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
    f = open("competition/results.md", "a")
    # output_str = ""
    for path in output_paths:
        with open(path, 'r') as file:
            raw_string = file.read().replace('\n', '')
        cmd = pre_cmd + '\'' + raw_string + '\''
        head_str = "\n=============== Receive feedbacks for %s ===============\n" % path
        f.write(head_str)
        print(head_str)
        # output_str += head_str + '\n'
        # Option 1 Record 
        stream = os.popen(cmd)
        output = stream.read()
        print(output)
        json.dump(output, f)
        output_dict = json.loads(output)
        f1_scores.append(output_dict['f1_score'])

    print("Average F1 score over all test cases: ", cal_avg(f1_scores))
    # Save to file
    # f.write(output_str)
    f.close()

if __name__ == '__main__':
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    output_paths = generate_output()
    print("Submitting: ", output_paths)
    # output_paths = ['outputs/output-BASELINE-1.json', 'outputs/output-BASELINE-2.json', 'outputs/output-BASELINE-3.json', 'outputs/output-BASELINE-4.json', 'outputs/output-BASELINE-5.json', 'outputs/output-BASELINE-6.json', 'outputs/output-BASELINE-7.json', 'outputs/output-BASELINE-8.json', 'outputs/output-BASELINE-9.json', 'outputs/output-BASELINE-10.json', 'outputs/output-BASELINE-11.json', 'outputs/output-BASELINE-12.json', 'outputs/output-BASELINE-13.json', 'outputs/output-BASELINE-14.json', 'outputs/output-BASELINE-15.json', 'outputs/output-BASELINE-16.json', 'outputs/output-BASELINE-17.json', 'outputs/output-BASELINE-18.json', 'outputs/output-BASELINE-19.json', 'outputs/output-BASELINE-20.json', 'outputs/output-BASELINE-21.json', 'outputs/output-BASELINE-22.json', 'outputs/output-BASELINE-23.json', 'outputs/output-BASELINE-24.json', 'outputs/output-BASELINE-25.json', 'outputs/output-BASELINE-26.json', 'outputs/output-BASELINE-28.json', 'outputs/output-BASELINE-27.json', 'outputs/output-BASELINE-28.json', 'outputs/output-BASELINE-29.json', 'outputs/output-BASELINE-30.json', 'outputs/output-TEAM-5-DAY-2-TEST-1.json', 'outputs/output-TEAM-3-DAY-2-TEST-1.json', 'outputs/output-TEAM-3-DAY-2-TEST-2.json', 'outputs/output-TEAM-6-DAY-2-TEST-2.json', 'outputs/output-TEAM-6-DAY-2-TEST-1.json', 'outputs/output-TEAM-6-DAY-2-TEST-3.json', 'outputs/output-TEAM-3-DAY-2-TEST-3.json', 'outputs/output-BENCHMARK-1.json', 'outputs/output-BENCHMARK-2.json']
    output_paths += ['outputs/output-TEAM-99-DAY-2-TEST-1.json']
    get_score(output_paths)