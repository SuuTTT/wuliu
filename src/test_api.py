import os
import requests
import json

# Set the headers
headers = {'Content-Type': 'application/json'}

# Set the url
url = 'http://127.0.0.1:8080/getZytpcl'

# Set the data folder and file extensions
data_folder = './data'
file_extensions = ['.json', '.txt']

# Iterate through each file in the directory
for file_name in os.listdir(data_folder):
    # Check if the file has the correct extension
    if file_name.endswith(tuple(file_extensions)):
        with open(os.path.join(data_folder, file_name), 'r') as file:
            try:
                # Load the JSON data from the file
                data = json.load(file)
            except json.JSONDecodeError:
                print(f"File {file_name} does not contain valid JSON")
                continue

            # Print the input data
            print(f"Input data for {file_name}:")
            print(json.dumps(data, indent=2))  # Pretty print JSON data
            print("-----")

            # Send the POST request to the Flask app
            response = requests.post(url, headers=headers, data=json.dumps(data))

            # Print the response
            print(f"Response for {file_name}:")
            print("Response status code:", response.status_code)
            print("Response data:", response.json())
            print("-----")
'''
add a check to see if the response is valid JSON, if not, print an analysis of the error
e.g. for this output is invalid, because the total number of goods sent from warehouse 1 exceeds the stock of goods in warehouse 1
-----
Input data for data_5.txt:
{
  "spdd": [
    {
      "ddnm": "Order1",
      "qynm": "Company1",
      "spnm": "Good1",
      "sl": 7,
      "lg": "\u679a",
      "ckdata": [
        {
          "cknm": "cknm1",
          "dwyssj": 3.0
        },
        {
          "cknm": "cknm2",
          "dwyssj": 4.0
        }
      ]
    },
    {
      "ddnm": "Order2",
      "qynm": "Company1",
      "spnm": "Good1",
      "sl": 4,
      "lg": "\u679a",
      "ckdata": [
        {
          "cknm": "cknm1",
          "dwyssj": 2.0
        },
        {
          "cknm": "cknm2",
          "dwyssj": 1.0
        }
      ]
    },
    {
      "ddnm": "Order3",
      "qynm": "Company1",
      "spnm": "Good1",
      "sl": 3,
      "lg": "\u679a",
      "ckdata": [
        {
          "cknm": "cknm1",
          "dwyssj": 1.0
        },
        {
          "cknm": "cknm2",
          "dwyssj": 3.0
        }
      ]
    }
  ],
  "ck": [
    {
      "cknm1": [
        {
          "spnm": "Good1",
          "sl": 10,
          "lg": "\u679a"
        }
      ]
    },
    {
      "cknm2": [
        {
          "spnm": "Good1",
          "sl": 2,
          "lg": "\u679a"
        }
      ]
    }
  ]
}
-----
Response for data_5.txt:
Response status code: 200
Response data: {'code': 200, 'data': [{'ddnm': 'Order1', 'cknm': 'cknm1', 'qynm': 'Company1', 'spnm': 'Good1', 'sl': 7, 'lg': '枚', 'dpsj': 21.0}, {'ddnm': 'Order2', 'cknm': 'cknm1', 'qynm': 'Company1', 'spnm': 'Good1', 'sl': 2, 'lg': '枚', 'dpsj': 4.0}, {'ddnm': 'Order2', 'cknm': 'cknm2', 'qynm': 'Company1', 'spnm': 'Good1', 'sl': 2, 'lg': '枚', 'dpsj': 2.0}, {'ddnm': 'Order3', 'cknm': 'cknm1', 'qynm': 'Company1', 'spnm': 'Good1', 'sl': 3, 'lg': '枚', 'dpsj': 3.0}]}


'''
