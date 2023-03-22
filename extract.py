import requests
import json
import math
import connection
from multiprocessing import Process
import time

#global variables
global page_no
global page_size
global searchreq 

# ------------ FUNCTION TO GET THE DATA AND INVOKE THE GRAPH NETWORK CREATION ----------------------
def getdata(**kwargs):

    #establishing connection with the Neo4j DB for CRUD ops
    session = connection.est_connection()

    for keyword in kwargs.get('keywords_list'):
        
        # ------------ INITIALISING THE API - POST PARAMETERS----------------------
        # the url to fetch the data from the API
        url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'

        #initializing the variables to default values to check for total items of the search
        page_no = 0
        page_size = 1
        fields_list = ["*"]
        search_fields = ["summary","title"]
        searchreq = {"lang":"en","searchFields":search_fields,"query":keyword,"page":page_no,"pageSize":page_size,"sourceFields":fields_list,"filters":{"productionType":{"type":"MultiValueSearchFilter","op":"any","values":["thesis","publication"]}}}

        #requesting the API for the data using the search request parameter & to calculate no.of loops required based on pagesize
        payload = requests.post(url, json=searchreq)
        json_pl = json.loads(payload.text)
        searchreq['pageSize'] = kwargs.get('payload_size')
        max_iter = math.ceil(json_pl.get('total')/kwargs.get('payload_size'))
        print("keyword: ",keyword)
        

        #file1 = open("output_pub.txt","w+",encoding='utf-8')
        #getting the publication IDs from the DB, if exists
        existing_pubs = session.execute_read(connection.get_pub_ids,keyword)

        # ------------ LOOPING OVER ALL THE EXTRACTED DATA----------------------
        #Looping over the page number to get the "page sized" amount of data at a time and process it
        for page_no in range(0,1): #set 1 to get first N(page_size) data, max_iter to get all the data page wise
            
            searchreq['page']=page_no
            payload = requests.post(url, json=searchreq)
            json_pl = json.loads(payload.text)

            if(json_pl.get('results')):
                loop = len(json_pl.get('results'))  #checking for the no.of items in the page to loop (to avoid index constarints)
                for item in range(0,loop):
                    try:
                        #file1.write(str(pub)) # writing the data to a file (if required for validation)
                        #file1.write("\n\n")
                        pub = json_pl.get('results')[item].get('value')        #extracting each result and its main content to write
                        if(pub.get('id') not in existing_pubs):                #checking if the publication ID already exists in the pool(DB)
                            #print("creating network")
                            connection.create_network(session,keyword,**pub)   #calling the network create function - this creates all the relevant nodes and relations
                    except Exception as e:  
                        print(e) #catching if there are any exceptions in creating the network
            else:
                print("No results found")
                
    session.close()



if __name__ == '__main__':
    
    # ------------ INITITALISING THE INPUT VARIABLES FOR GETDATA FUNC----------------------
    session = connection.est_connection() #establishing the connection to DB
    data = session.execute_read(connection.get_keyword_nodes,'primary',0) #getting all the primary keywords present in the DB(if exists)
    if(data!=[]):
        dict1 = {'payload_size':100,'keywords_list':data} #setting up the input variable for getdata function, if data exists in DB(this just updates the network)
    else:
        keywords = open("keywords.txt",'r',encoding='utf-8').read().lower().split('\n') #setting up the primary keywords from a static file (if no new/old primary keywords exists in DB)
        dict1 = {'payload_size':100,'keywords_list':keywords}
    
    # ------------ PARALLEL PROCESSING ----------------------
    tasks = Process(target=getdata,kwargs=dict1) #will run the getdata function for each keyword in parallel(API extraction & network creation)
    tasks.start()
    tasks.join()