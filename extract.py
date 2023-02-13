import requests
import pandas
import json
import math
import connection

#global variables
global page_no
global page_size
global searchreq 

url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'

#initializing the global variables to default values to check for total items
page_no = 0
page_size = 1
fields_list = ["id","summary","title","submissionDate","authors","publicationDate","productionType","keywords"]
search_fields = ["summary","title"]
query_string = "artificial intelligence"

searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":page_size,"sourceFields":fields_list}


#requesting the API for the data using the search request parameter to calculate no.of loops required
payload = requests.post(url, json=searchreq)
json_pl = payload.json()
iter = math.ceil(json_pl.get('total')/len(json_pl.get('results')))

print("total items:",json_pl.get('total'))
file1 = open("./Code/output.txt",'w+', encoding="utf-8")


#to extract the each value parameter's data (one at a time)
for page_no in range(0,iter):
    searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":page_size,"sourceFields":fields_list}
    payload = requests.post(url, json=searchreq)
    payload = payload.json()

    #for item in range(0,page_size):
    pub = payload.get('results')[0].get('value')
    if(str(pub.get('productionType'))=='thesis'):
        try:
            file1.write(str(pub))
        except Exception as e:
            print(e)
    #if iter==100:
    #   break
file1.close()