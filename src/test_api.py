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
