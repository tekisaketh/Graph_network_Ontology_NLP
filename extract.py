import requests
#import pandas
import json
import math
import connection
from multiprocessing import Process
import time

#global variables
global page_no
global page_size
global searchreq 

def getdata(**kwargs):

    session = connection.est_connection()

    for keyword in kwargs.get('keywords_list'):
        
        url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'

        #initializing the global variables to default values to check for total items
        page_no = 0
        page_size = 1
        fields_list = ["*"]
        search_fields = ["summary","title"]
        query_string = keyword
        searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":page_size,"sourceFields":fields_list,"filters":{"productionType":{"type":"MultiValueSearchFilter","op":"any","values":["thesis","publication"]}}}

        #requesting the API for the data using the search request parameter to calculate no.of loops required
        payload = requests.post(url, json=searchreq)
        json_pl = json.loads(payload.text)
        size1 = kwargs.get('size1')
        #iter = math.ceil(json_pl.get('total')/size1)
        print("keyword: ",keyword)
        
        #file1 = open("output_pub.txt","w+",encoding='utf-8')
        data, summary = session.execute_read(connection.get_pub_ids,keyword)
        #to extract the each value parameter's data (one at a time)
        for page_no in range(0,1):

            searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":size1,"sourceFields":fields_list,"filters":{"productionType":{"type":"MultiValueSearchFilter","op":"any","values":["thesis","publication"]}}}
            payload = requests.post(url, json=searchreq)
            json_pl = json.loads(payload.text)

            if(json_pl.get('results')):
                loop = len(json_pl.get('results'))
                for item in range(0,loop):
                    try:
                        #file1.write(str(pub))
                        #file1.write("\n\n")
                        pub = json_pl.get('results')[item].get('value')
                        if(pub.get('id') not in data):
                            connection.create_network(session,keyword,**pub)   
                    except Exception as e:
                        print(e)
            else:
                print("No results found")
                
    session.close()

if __name__ == '__main__':
    
    keywords = ['computer vision','deep learning','machine learning','artificial intelligence','neural networks','frugal ai','linear regression','logistic regression','Random Forests','recurrent neural network','convolutional neural network']
    dict1 = {'size1':500,'keywords_list':keywords}
    tasks = Process(target=getdata,kwargs=dict1)
    tasks.start()
    tasks.join()