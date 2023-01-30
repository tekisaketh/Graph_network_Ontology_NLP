import requests
import pandas
import json

url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'


searchreq = {"lang":"en","searchFields":["summary","title"],"query":"deep learning","page":0,"pageSize":1}
#searchreq = {"lang":"en","page":0,"pageSize":1,}

#requesting the API for the data using the search request parameter
payload = requests.post(url, json=searchreq)

json_pl = payload.json()
info  = json_pl.get('results')
#.get('value')


#Dumping the payload in a file to test the data
file1 = open("output.txt",'w')
file1.write(str(info))
file1.close()
