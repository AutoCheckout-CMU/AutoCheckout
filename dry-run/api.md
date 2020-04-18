# submission
curl --location --request GET 'cps-week.internal.aifi.io/api/v1/testcases' --header 'TOKEN: 5ea023be-b530-4816-8eda-5340cfabe9b0'
curl --location --request POST 'cps-week.internal.aifi.io/api/v1/results' --header 'TOKEN: 5ea023be-b530-4816-8eda-5340cfabe9b0' --header 'Content-Type: application/json' --data-raw {"test_case" xxxx }