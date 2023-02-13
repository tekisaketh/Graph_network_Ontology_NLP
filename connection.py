from neo4j import GraphDatabase
import json

def get_creds(key):
    f = open("./Code/auth.json")
    creds = json.load(f)
    username = creds.get(key)[0]
    password = creds.get(key)[1]
    return(username,password)

def est_connection():
    URI = "neo4j://localhost/7474"
    AUTH = get_creds('neo4j creds')
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try: 
            driver.verify_connectivity()
            with driver.session(database="neo4j") as session:
                return session
        except Exception as e:
            print("Error connecting to DB:",e)
            return(e)


                
    
