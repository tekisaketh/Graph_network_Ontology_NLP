import requests
#import pandas
import json
import math
#import connection
from multiprocessing import Process

#global variables
global page_no
global page_size
global searchreq 


def getdata(**kwargs):
    for keyword in kwargs.get('keywords_list'):
        url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'

        #initializing the global variables to default values to check for total items
        page_no = 0
        count=0
        page_size = 1
        type_filter = ["thesis","publication"]
        fields_list = ["id","title","submissionDate","authors","publicationDate","productionType","keywords"]
        search_fields = ["summary","title"]
        query_string = keyword
        #query_string = "deep learning computer vision"

        searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":page_size,"sourceFields":fields_list}


        #requesting the API for the data using the search request parameter to calculate no.of loops required
        payload = requests.post(url, json=searchreq)
        json_pl = json.loads(payload.text)
        size1 = kwargs.get('size1')
        #iter = math.ceil(json_pl.get('total')/len(json_pl.get('results')))
        iter = math.ceil(json_pl.get('total')/size1)

        #using two files to store the unfiltered(raw payload) and filtered data
        file1 = open("./Code/output.txt",'w+', encoding="utf-8")
        file2 = open("./Code/raw_sample.txt",'w+', encoding="utf-8")
        file2.write(str(payload.text))
        file2.close()
        print("keyword: ",keyword)
        print("total items: ",json_pl.get('total'))
        print("No.of API hits required: ",iter)

        
        #to extract the each value parameter's data (one at a time)
        for page_no in range(0,iter):
            #print(page_no)
            searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":size1,"sourceFields":fields_list}
            payload = requests.post(url, json=searchreq)
            json_pl = json.loads(payload.text)
            loop = len(json_pl.get('results'))
            for item in range(0,loop):
                pub = json_pl.get('results')[item].get('value')
                if(str(pub.get('productionType')) in type_filter):  
                    try:
                        count+=1
                        file1.write(str(pub))
                        file1.write("\n")
                    except Exception as e:
                        print(e)

        #print("Total items found after filtering: ",count)
        file1.close()
        

if __name__ == '__main__':
    
    keywords = ['deep learning','artificial intelligence','machine learning','computer vision']
    dict1 = {'size1':1000,'keywords_list':keywords}
    tasks = Process(target=getdata,kwargs=dict1)
    tasks.start()
    tasks.join()
    #getdata(**dict1)
