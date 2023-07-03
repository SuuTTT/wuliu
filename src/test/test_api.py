import requests
import json

# Read the data from the json file
with open('data.json', 'r') as file:
    data = json.load(file)

# Set the headers
headers = {'Content-Type': 'application/json'}

# Send the POST request to the Flask app
response = requests.post('http://127.0.0.1:8080/getZytpcl', headers=headers, data=json.dumps(data))

# Print the response
print("Response status code:", response.status_code)
print("Response data:", response.json())
