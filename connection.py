from neo4j import GraphDatabase
import json
from datetime import datetime
import math

# ------------ABSTRACTING THE PYTHON CONNECTOR FUNCTION TO NEO4J----------------------
def get_creds(key): #get the creentials to access the DB
    f = open("auth2.json") #file storing the creds in json format {"neo4j creds":[<DB Name>,<password>]}
    creds = json.load(f)
    username = creds.get(key)[0]
    password = creds.get(key)[1]
    f.close()
    return(username,password) #returning the username & password of the DB

def est_connection(): #establishing the connection with the DB via username-password authentication and returning the connection request/port
    URI = "neo4j://localhost/7474"
    AUTH = get_creds('neo4j creds')
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            session_ = driver.session(database="neo4j")
            return session_
        except Exception as e:
            print("Error:",e)
            return(e)

# ------------ FUNCTIONS TO CREATE DATA IN NEO4J ---------------------- 

#to create the publication(with required parameters) and its searched keyword(primary) nodes with relation
def create_main_nodes(tx,id,prodType,ttype,title,summary,pubdate,lastupdate,keyword):
    result = tx.run("""MERGE (p:Publication {name:$ptype,id:$id,type:$ttype,flag:"True",title:$title,summary:$summary,publicationDate:datetime({epochSeconds:$pubdate}),LastUpdatedatScanR:datetime({epochSeconds:$lastupdate})})
    MERGE (k:keyword {name:$keyword,type:"primary"})
    MERGE (p)<-[r:FOUND_IN]-(k)
    """,id=id,ptype=prodType,ttype=ttype,title=title,summary=summary,pubdate=pubdate,lastupdate=lastupdate,keyword=keyword)
    summary = result.consume()
    return summary

#To create the associated affiliations made to publish the article/paper and create a relation b/w them
def create_affiliation_nodes(tx,p_id,id,kind,label,address,city,country):
    result = tx.run("""MATCH (p:Publication {id:$p_id})
    MERGE (f:Affiliation {id:$id,kind:$kind,label:$label,address:$address,city:$city,country:$country})
    MERGE (p)-[i:PRODUCED_BY]->(f)
    """,p_id=p_id,id=id,kind=kind,label=label,address=address,city=city,country=country)
    summary = result.consume()
    return summary

#To create the authors of the published article/papaer and create a relation b/w them
def create_author_nodes(tx,p_id,id,firstname,lastname,gender,role):
    result = tx.run("""MATCH (p:Publication {id:$p_id})
    MERGE (a:Author {id:$id,name:$role,firstName:$firstname,lastName:$lastname,gender:$gender})
    MERGE (p)-[r:AUTHORED_BY]->(a)
    """,p_id=p_id,id=id,role=role,firstname=firstname,lastname=lastname,gender=gender)
    summary = result.consume()
    return summary

#To create the keyword nodes (primary/secondary) extracted using NLP from the publications and create a relation b/w them
def create_keynodes(tx,p_id,keyword,flag):
    result = tx.run("""MATCH (p:Publication {id:$p_id}) 
    MERGE (k:keyword {name:$keyword,type:$flag})
    MERGE (p)<-[r:FOUND_IN]-(k)
    """,p_id=p_id,keyword=keyword,flag=flag)
    summary = result.consume()
    return summary

# ------------ FUNCTIONS TO FETCH DATA FROM NEO4J ----------------------
      
# to get the keyword nodes and its last updated time (flag=1 gives only the publication ids)
def get_keyword_nodes(tx,k_type,flag):
    result = tx.run("""MATCH (k:keyword {type:$k_type}) return k.name,k.lastupdated
    """,k_type=k_type)
    if(flag==1):
        results = result.values()
    else:
        results = result.value()   
    return results

#To get the publication IDs and its summary (on which the NLP hasn't been performed)
def get_pub_summary(tx):
    result = tx.run("""MATCH (p:Publication {flag:'True'}) return p.id as id, p.summary as summary""")
    results = result.to_df()
    return results

#To get the publication IDs (fetches its associated publications, if given a primary keyword)
def get_pub_ids(tx,keyword):
    if(keyword=='all'):
        result = tx.run("""MATCH (p:Publication) return p.id""")
        results = result.value()
        return results
    else:
        result = tx.run("""MATCH (p:Publication) MATCH(k:keyword {name:$keyword,type:"primary"}) where (p)-[:FOUND_IN]-(k) RETURN p.id""",keyword=keyword)
        results = result.value()
        return results     

# ------------ FUNCTIONS TO UPDATE/SET SPECIFIC DATA IN NEO4J ----------------------

#to set the time of the primary keyword to its lastupdated parameter
def set_keyword_time(tx,keyword):
    tx.run("""MATCH (k:keyword {name:$keyword,type:"primary"}) set k.lastupdated=datetime()""",keyword=keyword)

#setting the publication's flag to False - this is to notify NLP script that keyword extraction is already performed on this node
def set_pub_flag(tx,p_id):
    tx.run("""MATCH (p:Publication {id:$p_id}) set p.flag="False" """,p_id=p_id)


# ------------ DATA INCONSISTENCY CHECK FUNCTIONS----------------------

#validating the key and its corresponding values existance of a dictionary
def check_value_dict(x,y):
    if(x.get(y)):
        return str(x.get(y))
    else:
        return str("")

#check and extracting values from the author dictionary into a list
def check_authors(x):
    id = check_value_dict(x,'id')   
    gender = check_value_dict(x,'gender')
    firstName = check_value_dict(x,'firstName')
    lastName = check_value_dict(x,'lastName')
    return [id,firstName,lastName,gender]

#checking and assigning appropriate summary/title based on existing value 
def check_summ_title(x):
    if(x.get('default')):
        val = str(x.get('default'))
    elif(x.get('en')):
        val = str(x.get('en'))
    elif(x.get('fr')):
        val = str(x.get('fr'))
    else:
        val = str("")
    return val

#checking and assigning the affiliation parameters to the list
def check_affiliations(x):
    id = check_value_dict(x,'id')
    if(x.get('kind')):
        kind = str(x.get('kind'))
    else:
        kind= str("")
    if(x.get('label')):
        label = check_summ_title(x.get('label'))
    else:
        label = str("")
    if(x.get('address')):
        if(len(x.get('address'))>0):
            addr = x.get('address')[0]
            address = check_value_dict(addr,'address')
            city = check_value_dict(addr,'city')
            country = check_value_dict(addr,'country')
    else:
        address,city,country = [str(""),str(""),str("")]

    return [id,kind,label,address,city,country]

#checking for existing time value and converting millisecond epoch into seconds(will return 0 - Jan 1970 if value doesn't exists)
def time_items(x,y):
    if(x.get(y)):
        return int(x.get(y)/1000)
    else:
        return 0    

# ------------ GRAPH NETWORK CREATION FUNCTION ----------------------

#To create all the network nodes and relations, based on the fetched API result(dictionary)
def create_network(con_session,keyword,**kwargs):
    
    flag1 = True
    paper_id = str(kwargs.get('id'))
    t_type = check_value_dict(kwargs,'type')
    title = check_summ_title(kwargs.get('title'))

    if(kwargs.get('summary')==None or kwargs.get('summary')==""): #setting the flag to ignore publications without any summary (from the API)
        flag1 = False
    else:
        summary = check_summ_title(kwargs.get('summary'))
    
    pubdate = time_items(kwargs,"publicationDate")
    lastupdate = time_items(kwargs,"lastUpdated")
    
    if(flag1): #will check for the flag(summary exsisting) and then proceeds to create the network 
        param_list = [paper_id,str(kwargs.get('productionType')),t_type,title,summary,pubdate,lastupdate,keyword]
        con_session.execute_write(create_main_nodes,*param_list) 
        #con_session.execute_write(set_keyword_time,keyword)

        if(kwargs.get('authors')): #checking for authors data and creating the associated nodes
            for dict_person in kwargs.get('authors'):
                if(dict_person.get('person')): #creates the network if the information on 'person' (with ID etc.) is available
                    author_lst = [paper_id]
                    author_lst += check_authors(dict_person.get('person'))
                    author_lst.append(str(dict_person.get('role')))
                    con_session.execute_write(create_author_nodes,*author_lst)
            
        if(kwargs.get('affiliations')): #checking for affiliations data and creating the associated nodes
            for dict1 in kwargs.get('affiliations'):
                aff_details = [paper_id]
                aff_details += check_affiliations(dict1)
                con_session.execute_write(create_affiliation_nodes,*aff_details)
