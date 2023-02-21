from neo4j import GraphDatabase
import json

item1 = {'id': 'hal-01324914', 'productionType': 'publication', 'title': {'default': 'AN ILLUMINANT-INDEPENDENT ANALYSIS OF REFLECTANCE AS SENSED BY HUMANS, AND ITS APPLICABILITY TO COMPUTER VISION'}, 'authors': [{'role': 'author', 'firstName': 'Alban', 'lastName': 'Flachot', 'fullName': 'Alban Flachot'}, {'person': {'id': 'idref231568061', 'firstName': 'Edoardo', 'lastName': 'Provenzi', 'fullName': 'Edoardo Provenzi', 'gender': 'M', 'affiliations': [{'structure': {'id': '200416333R'}, 'startDate': 1354320000000, 'endDate': 1419984000000, 'sources': ['hal-02286869', 'hal-02286868', 'hal-02288396', 'hal-02288397', 'hal-02286871', 'hal-02286870']}, {'structure': {'id': '200711916B'}, 'startDate': 1480550400000, 'endDate': 1640908800000, 'sources': ['hal-03029722', 'hal-03276183', 'hal-03276191', 'hal-03268152', 'hal-02480258', 'hal-02543955', 'hal-02546380', 'hal-02479897', 'hal-03276158', 'hal-02336556']}, {'structure': {'id': '18009202500022'}, 'startDate': 1354320000000, 'endDate': 1419984000000, 'sources': ['hal-02286869', 'hal-02286868', 'hal-02288396', 'hal-02288397', 'hal-02286871', 'hal-02286870']}, {'structure': {'id': '200412801B'}, 'startDate': 1354320000000, 'endDate': 1577750400000, 'sources': ['doi10.1109/sitis.2013.75', 'doi10.1016/j.jmp.2016.10.005', 'tel-01339682', 'hal-02141503', 'hal-01054307', 'doi10.1117/1.jei.26.3.031202', 'hal-01386173', 'hal-01256503', 'doi10.1109/euvip.2016.7764601', 'hal-02145070', 'doi10.1016/j.visres.2015.02.025', 'doi10.1142/s0219887816300087', 'doi10.1007/978-3-030-26980-7_64', 'doi10.1109/qomex.2016.7498953', 'hal-01324912', 'hal-01386171']}, {'structure': {'id': '200319327Z'}, 'startDate': 1354320000000, 'endDate': 1419984000000, 'sources': ['hal-02286869', 'hal-02286868', 'hal-02288396', 'hal-02286870', 'hal-02288397', 'hal-02286871']}], 'externalIds': [{'id': '1062407', 'type': 'docid_hal'}, {'id': '822133', 'type': 'docid_hal'}, {'id': '11623462', 'type': 'docid_hal'}, {'id': '231568061', 'type': 'idref'}, {'id': '182650', 'type': 'id_hal'}, {'id': '1106405', 'type': 'docid_hal'}], 'lastUpdated': 1666102308265}, 'role': 'author', 'firstName': 'Edoardo', 'lastName': 'Provenzi', 'fullName': 'Edoardo Provenzi', 'affiliations': [{'structure': '200412801B'}]}, {'role': 'author', 'firstName': 'J Kevin', 'lastName': "O'Regan", 'fullName': "J Kevin O'Regan", 'affiliations': [{'structure': '201420751Z'}]}], 'isOa': False, 'publicationDate': 1477353600000, 'keywords': {'default': ['Illuminant independency', 'Joint diagonality', "Philipona-O'Regan's model", 'Von Kries model'], 'en': ['Von Kries model', "Philipona-O'Regan's model", 'Illuminant independency', 'Joint diagonality']}}

#req_item = {'id': 'hal-01324915', 'productionType': 'publication', 'title': 'AN ILLUMINANT-INDEPENDENT ANALYSIS OF REFLECTANCE AS SENSED BY HUMANS, AND ITS APPLICABILITY TO COMPUTER VISION'}

def get_creds(key):
    f = open("auth.json")
    creds = json.load(f)
    username = creds.get(key)[0]
    password = creds.get(key)[1]
    return(username,password)


# def create_node(tx,id,ptype,title):
#     result = tx.run("""
#     MERGE (p:Paper {id:$id,ptype:$ptype,title:$title})
#     """,id=id,ptype=ptype,title=title)
#     summary = result.consume()
#     return summary

#print(json.loads(item1))
#MERGE (k:keyword {name:$keyword})
def create_node(tx,id,productionType,title,keyword):
    result = tx.run("""MERGE (p:Paper {id:$id,ptype:$ptype,title:$title})
    
    """,id=id,ptype=productionType,title=title,keyword=keyword)
    #,id=str(kwargs.get('id')),ptype=str(kwargs.get('productionType')),title=str(kwargs.get('title').get('default')))
    summary = result.consume()
    return summary

list1 = [str(item1.get('id')),str(item1.get('productionType')),str(item1.get('title').get('default'))]
#print(list1)

def est_connection():
    URI = "neo4j://localhost/7474"
    AUTH = get_creds('neo4j creds')
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            driver.verify_connectivity()
            session = driver.session(database="neo4j")
            return session
            #with driver.session(database="neo4j") as session:
            #   summary = session.execute_write(create_node,**req_item)
            #    #print(summary.counters)
        except Exception as e:
            print("Error:",e)
            return(e)


#print(type(item1))

#print(item1.get('title').get('default'))

session = est_connection()
session.execute_write(create_node,*list1)
#print("Query counters: ",summary.counters)





'''
def checking_creation_net(variable):

    if(len(variable.get(authors))<2):


def create_network(tx,id,title,productiontype,publicationDate,keywords,authors):
    result = tx.run("""
    MERGE (p:Production {productiontype:$productiontype,id:$id,title:$title})
    MERGE (a:authors) {id}
    MERGE (k:Keyword {text:$keyword})
    MERGE (k)->[:EXISTS_IN]-(p)
    return k,p
    """)

    else:

  def create_network(tx,id,title,productiontype,publicationDate,keywords,authors):
    result = tx.run("""
    MERGE (p:Production {productiontype:$productiontype,id:$id,title:$title})
    MERGE (a:authors) {id}
    MERGE (a:co-author) {id}
    MERGE (k:Keyword {text:$keyword})
    MERGE (k)->[:EXISTS_IN]-(p)
    return k,p
    """)
    

conn = est_connection()
print(conn)
print(type(conn))
'''

                
    
