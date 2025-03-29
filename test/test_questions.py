import requests
import json

BASE_URL = "http://127.0.0.1:5000/api/"

def test_question(question, expected_output):
    print(f"\nTesting: {question}")
    headers = {"User-Agent": "HTTPie/3.2.4", "Content-Type": "application/json"}
    
    # Send the request with JSON payload
    response = requests.post(BASE_URL, json={"question": question}, headers=headers)

    print("\nRaw Response:", response.text)  # Print full response before JSON decoding
    
    try:
        response_json = response.json()
    except requests.exceptions.JSONDecodeError:
        print("Error: Server response is not JSON. Check if FastAPI is running!")
        return

    if "answer" not in response_json:
        print("Error: 'answer' key missing in response!")
        return
    
    # Attempt to decode the answer if it's a stringified JSON
    answer = response_json["answer"]
    
    try:
        decoded_answer = json.loads(answer)  # Convert string to actual JSON
        print("\nProper JSON Response:", json.dumps(decoded_answer, indent=4))  # Pretty-print
    except json.JSONDecodeError:
        decoded_answer = answer  # Keep as string if not a JSON
    
    # Check expected output
    if expected_output and expected_output not in str(decoded_answer):
        print(f"Test Failed! Expected: {expected_output}, Got: {decoded_answer}")
    else:
        print("Test Passed!")
# import requests
# import json

# BASE_URL = "http://127.0.0.1:5000/api/"

# def test_question(question, expected_output):
#     print(f"\nTesting: {question}")
#     headers = {"User-Agent": "HTTPie/3.2.4"}
#     response = requests.post(BASE_URL, data={"question": question}, headers=headers)

#     # Send request
#     #response = requests.post(BASE_URL, data={"question": question})
    
#     print("\nRaw Response:", response.text)  # Print full response before JSON decoding
    
#     try:
#         response_json = response.json()
#     except requests.exceptions.JSONDecodeError:
#         print("Error: Server response is not JSON. Check if FastAPI is running!")
#         return

#     if "answer" not in response_json:
#         print("Error: 'answer' key missing in response!")
#         return
    
#     # Attempt to decode the answer if it's a stringified JSON
#     answer = response_json["answer"]
    
#     try:
#         decoded_answer = json.loads(answer)  # Convert string to actual JSON
#         print("\nProper JSON Response:", json.dumps(decoded_answer, indent=4))  # Pretty-print
#     except json.JSONDecodeError:
#         decoded_answer = answer  # Keep as string if not a JSON
    
#     # Check expected output
#     if expected_output and expected_output not in str(decoded_answer):
#         print(f"Test Failed! Expected: {expected_output}, Got: {decoded_answer}")
#     else:
#         print("Test Passed!")

def run_tests():
    # test_question("What is the output of code -s?", "")
    # test_question("Send a HTTPS request to https://httpbin.org/get", "23f2000599@ds.study.iitm.ac.in")
    # test_question("What is the output of the command? (npx -y prettier@3.4.2 README.md | sha256sum)", "")
    # test_question("How many Wednesdays", "1532")
    test_question("Let's make sure you can write formulas in Google Sheets.","")
    # test_question("Let's make sure you can write formulas in Excel.","")
    # test_question("Download and unzip file q-extract-csv-zip.zip", "")
    # test_question("Sort this JSON array of objects by the value of the age field", "[{\"name\":\"Oscar\",\"age\":1},{\"name\":\"Alice\",\"age\":8}]")


run_tests()
print("\nAll tests completed!")
