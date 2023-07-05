import os
import unittest
import requests
import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.url = 'http://127.0.0.1:8080/getZytpcl'
        self.headers = {'Content-Type': 'application/json'}
        self.data_folder = './data'
        self.file_extensions = ['.json', '.txt']

    def test_flask_app(self):
        # Iterate through each file in the directory
        for file_name in os.listdir(self.data_folder):
            # Check if the file has the correct extension
            if file_name.endswith(tuple(self.file_extensions)):
                with open(os.path.join(self.data_folder, file_name), 'r') as file:
                    try:
                        data = json.load(file)
                    except json.JSONDecodeError:
                        print(f"File {file_name} does not contain valid JSON")
                        continue
                    response = requests.post(self.url, headers=self.headers, data=json.dumps(data))

                    # Assert the response status code is 200
                    self.assertEqual(response.status_code, 200)

                    # If you want to check the data returned, you can do so here
                    response_data = response.json()

                    # Uncomment the line below if you want to print response data for each file
                    # print(f"Response data for {file_name}:", response_data)

if __name__ == '__main__':
    unittest.main()
