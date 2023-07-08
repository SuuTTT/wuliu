import pandas as pd
import json
with open('result.json', 'r') as f:
    json_data = json.load(f)  # Note that it's 'json.load()' NOT 'json.loads()'

json_data=json.loads(json_data)
data = json_data['data']

df = pd.DataFrame(data)

grouped_ddnm = df.groupby('ddnm').agg({'sl': 'sum'}).reset_index()
grouped_cknm = df.groupby('cknm').agg({'sl': 'sum'}).reset_index()

print('Sum over ddnm:')
print(grouped_ddnm)
print('\nSum over cknm:')
print(grouped_cknm)
