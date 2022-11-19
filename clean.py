import pandas as pd
import json
# dd = pd.read_csv('data.csv').to_dict('records')
# for i in dd:
#     i['Category'] = i['Category'].replace('Categories: ', '')
# dds =pd.DataFrame(dd)
# dds.to_csv('data1.csv',index=False)

mn = pd.read_csv('dplgroup-data.csv').to_dict('records')
with open('result.json') as json_file:
    bb = json.load(json_file)

for er in mn:
    name = bb[er['Title']]
    er['tags'] = str(er['tags']).join([f"{dbl} " for dbl in name]).replace('nan','- ')


dds =pd.DataFrame(mn)
dds.to_csv('data2.csv',index=False)