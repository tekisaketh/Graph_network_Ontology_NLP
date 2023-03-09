import connection
import requests
import json


def update_network(session,*data_pair):

    url = 'https://scanr-api.enseignementsup-recherche.gouv.fr/api/v2/publications/search'
    page_no = 0
    page_size = 1
    fields_list = ["id"]
    search_fields = ["summary","title"]
    query_string = str(data_pair[0])
    print(query_string)
    lastupdated = str(data_pair[1])[:-6]+"Z"
    print(lastupdated)

    data, summary = session.execute_read(connection.get_pub_ids,query_string)
    print(len(data),type(data))

    searchreq = {"lang":"en","searchFields":search_fields,"query":query_string,"page":page_no,"pageSize":page_size,"sourceFields":fields_list,"filters":{"productionType":{"type":"MultiValueSearchFilter","op":"any","values":["thesis","publication"]},
    "lastUpdated":{"type":"DateRangeFilter","min":"2023-02-08T20:45:48.940000000Z"},"id":{"type":"MultiValueSearchFilter","op":"any","values":data}}}
    payload = requests.post(url, json=searchreq)
    json_pl = json.loads(payload.text)
    
    if(len(json_pl.get('total'))>0):
        searchreq['pageSize']=json_pl.get('total')
        searchreq['fields_list'] = ["*"]
        payload = requests.post(url, json=searchreq)
        json_pl = json.loads(payload.text)
        loop = len(json_pl.get('results'))
        for item in range(0,loop):
            try:
                pub = json_pl.get('results')[item].get('value')
                #code to update nodes (need to modify the create_network function to call new update queries)
            except Exception as e:
                print(e)
    else:
        print("No updates for {} nodes".format(query_string))
    
    session.close()

#update_network(*data[0])

if __name__ == '__main__':

    session = connection.est_connection()
    data, summary = session.execute_read(connection.get_keyword_nodes,'primary')
    update_network(session,*data)
    session.close()
