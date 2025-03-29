import json
import hashlib
import zipfile
import csv
import os
import datetime
import pandas as pd

import subprocess

subprocess.run(
    [r"C:\Users\Smriti\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd", "--status"],
    capture_output=True,
    text=True
)
def execute_question(question: str):
    """
    Executes specific logic for each predefined question.
    """
    if question.startswith("What is the output of code -s?"):
        return run_code_s()

    elif question.startswith("Send a HTTPS request to"):
        return send_https_request()

    elif question.startswith("What is the output of the command? (npx -y prettier@3.4.2 README.md | sha256sum)"):
        return hash_readme()

    elif question.startswith("Let's make sure you can write formulas in Google Sheets."):
        return google_sheets_formula_evaluation(formula)

    elif question.startswith("Let's make sure you can write formulas in Excel."):
        return excel_formula_evaluation()

    elif question.startswith("Just above this paragraph, there's a hidden input"):
        return "Hidden value found using HTML scraping"

    elif question.startswith("How many Wednesdays"):
        return count_wednesdays()

    elif question.startswith("Download and unzip file q-extract-csv-zip.zip"):
        return extract_csv_answer()

    elif question.startswith("Sort this JSON array of objects by the value of the age field"):
        return sort_json()

    elif question.startswith("Download q-multi-cursor-json.txt and use multi-cursors"):
        return hash_json_data()

    elif question.startswith("Find all <div>s having a foo class"):
        return sum_div_values()

    elif question.startswith("Download and process the files in q-unicode-data.zip"):
        return process_unicode_data()

    else:
        return "Question not recognized"
import re
import numpy as np

def parse_formula(formula):
    pattern = r"SEQUENCE\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)\s*,\s*(\d+)\s*,\s*(\d+)"
    match = re.search(pattern, formula)
    if not match:
        raise ValueError(f"Invalid formula format: {formula}")
    rows, cols, start, step, take_rows, take_cols = map(int, match.groups())
    return rows, cols, start, step, take_rows, take_cols


def google_sheets_formula_evaluation(formula):
    """
    Evaluates the Google Sheets formula like:
    =SUM(ARRAY_CONSTRAIN(SEQUENCE(rows, cols, start, step), take_rows, take_cols))
    """
    # Parse the formula to get the necessary values
    rows, cols, start, step, take_rows, take_cols = parse_formula(formula)
    
    # Generate the sequence matrix
    sequence = np.arange(start, start + (rows * cols * step), step).reshape(rows, cols)

    # Apply ARRAY_CONSTRAIN (taking 'take_rows' rows and 'take_cols' columns)
    constrained_array = sequence[:take_rows, :take_cols]

    # Sum the constrained values
    result = np.sum(constrained_array)

    return result  # Return the result

# Example usage
formula = "=SUM(ARRAY_CONSTRAIN(SEQUENCE(100, 100, 4, 4), 1, 10))"
result = google_sheets_formula_evaluation(formula)



import numpy as np

def excel_formula_evaluation(values, sort_order, take_count=8):
    """Mimics =SUM(TAKE(SORTBY(values, sort_order), 1, take_count))"""
    
    # Sort by custom order
    sorted_values = [val for _, val in sorted(zip(sort_order, values))]

    # Take first 'take_count' elements
    top_values = sorted_values[:take_count]

    # Sum them
    return sum(top_values) # Return as string to match expected test output

import subprocess

def run_code_s():
    vscode_path = r"C:\Users\Smriti\AppData\Local\Programs\Microsoft VS Code\Code.exe"
    result = subprocess.run([vscode_path, "--status"], capture_output=True, text=True)
    return result.stdout.strip()


import json
import requests

def send_https_request():
    headers = {
        'User-Agent': 'HTTPie/3.2.1'
    }
    try:
        response = requests.get(
            "https://httpbin.org/get",
            params={"email": "23f2000599@ds.study.iitm.ac.in"},
            headers=headers
        )
        response.raise_for_status()
        return json.dumps(response.json(), separators=(',', ':'))
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parsing failed: {e}")
        return None

import subprocess

def hash_readme():
    command = 'npx -y prettier@3.4.2 test/README.md | sha256sum'
    
    # Run command inside Git Bash
    result = subprocess.run(["C:/Program Files/Git/bin/bash.exe", "-c", command], capture_output=True, text=True)

    if result.returncode == 0:
        return result.stdout.strip().split()[0]  # Extract only the hash value
    else:
        return f"Error: {result.stderr}"

# Test the function
print(hash_readme())


def count_wednesdays():
    start_date = datetime.date(1986, 4, 8)
    end_date = datetime.date(2015, 8, 14)
    count = sum(1 for day in range((end_date - start_date).days + 1)
                if (start_date + datetime.timedelta(days=day)).weekday() == 2)
    return str(count)

def extract_csv_answer():
    with zipfile.ZipFile("tests/q-extract-csv-zip.zip", 'r') as zip_ref:
        zip_ref.extractall("tests/")
    with open("tests/extract.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            return row["answer"]

def sort_json():
    data = [{"name":"Alice","age":8},{"name":"Bob","age":76},{"name":"Charlie","age":56},
            {"name":"David","age":21},{"name":"Emma","age":19},{"name":"Frank","age":85},
            {"name":"Grace","age":81},{"name":"Henry","age":89},{"name":"Ivy","age":59},
            {"name":"Jack","age":11},{"name":"Karen","age":26},{"name":"Liam","age":21},
            {"name":"Mary","age":72},{"name":"Nora","age":90},{"name":"Oscar","age":1},
            {"name":"Paul","age":71}]
    sorted_data = sorted(data, key=lambda x: (x["age"], x["name"]))
    return json.dumps(sorted_data, separators=(',', ':'))

def hash_json_data():
    with open("tests/q-multi-cursor-json.txt", "r") as f:
        json_data = json.load(f)
    json_string = json.dumps(json_data, separators=(',', ':'))
    return hashlib.sha256(json_string.encode()).hexdigest()

def sum_div_values():
    # Assume we have extracted the HTML and parsed with BeautifulSoup
    values = [10, 20, 30]  # Example values
    return str(sum(values))

def process_unicode_data():
    total_sum = 0
    for file, encoding in [("data1.csv", "cp1252"), ("data2.csv", "utf-8"), ("data3.txt", "utf-16")]:
        df = pd.read_csv(f"tests/{file}", encoding=encoding, sep="\t" if file.endswith(".txt") else ",")
        total_sum += df[df["symbol"].isin(["‚", "†"])]["value"].sum()
    return str(total_sum)
