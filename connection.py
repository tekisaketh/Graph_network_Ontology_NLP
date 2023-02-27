from neo4j import GraphDatabase
import json
from datetime import datetime



#item1 = {'id': 'doi10.1007/978-0-387-31439-6', 'productionType': 'publication', 'title': {'default': 'Computer Vision'}, 'authors': [{'person': {'id': 'idref059347856', 'firstName': 'François', 'lastName': 'Chaumette', 'fullName': 'François Chaumette', 'gender': 'M', 'affiliations': [{'structure': {'id': '198018249C'}, 'startDate': 1354320000000, 'endDate': 1388448000000, 'sources': ['doi10.1016/j.robot.2013.06.010']}, {'structure': {'id': '200518339S'}, 'startDate': 1543622400000, 'endDate': 1577750400000, 'sources': ['doi10.1109/lra.2019.2893611']}, {'structure': {'id': '180089047'}, 'startDate': 1417392000000, 'endDate': 1514678400000, 'sources': ['doi10.1016/j.actaastro.2017.06.003', 'doi10.1016/j.actaastro.2016.06.018', 'doi10.1007/978-1-4471-5058-9_170']}, {'structure': {'id': '200418341Y'}, 'startDate': 880934400000, 'endDate': 1514678400000, 'sources': ['doi10.1109/iros.2014.6942649', 'doi10.1016/j.robot.2013.06.010', 'hal-01398925', 'hal-01385400', 'hal-01159882', 'doi10.1109/icra.2017.7989237', 'hal-00949346', 'hal-01399774', 'doi10.1109/icra.2015.7140045', 'doi10.1109/tro.2016.2637912', 'hal-01277589', 'doi10.1177/0278364912460413', 'hal-01060196', 'hal-01572366', 'hal-00821230', 'doi10.1007/978-0-387-31439-6', 'doi10.1109/tits.2014.2308977', 'hal-01358639', 'hal-00949169', 'hal-01258925', 'hal-00949336', 'hal-01385408', 'doi10.1016/j.actaastro.2016.06.018', 'tel-00843890', 'hal-01241732', 'hal-01088961', 'doi10.1109/tro.2014.2365652', 'hal-00949176', 'hal-00949173', 'hal-00949163', 'doi10.1109/tcyb.2013.2251331', 'doi10.1109/lra.2016.2521907', 'hal-01121120', 'hal-01358124', 'hal-01572362', 'hal-01445486', 'hal-01304728', 'hal-01355384', 'hal-01355382', 'hal-01185841', 'lirmm-00808317', 'doi10.1016/j.robot.2014.10.017', 'doi10.1109/tro.2013.2281560', 'hal-00851997', 'hal-01259750', 'hal-00821234', 'hal-01589882', 'doi10.1007/978-1-4471-5058-9_170', 'hal-01121631', 'hal-01355394', 'hal-01576084', 'hal-01385401', 'hal-01589887', 'hal-01572353', 'hal-01400575', 'hal-01435811', 'hal-01332999', 'hal-01121630', 'hal-00807642', 'hal-01784234', 'hal-01445484', 'hal-01408422', 'doi10.1109/lra.2016.2645512', 'hal-01421734']}, {'structure': {'id': '201822637G'}, 'startDate': 1448928000000, 'endDate': 1640908800000, 'sources': ['doi10.1109/iros.2018.8594003', 'hal-01935405', 'hal-01935395', 'doi10.1109/tro.2018.2830379', 'doi10.1145/3359566.3360085', 'doi10.1109/lra.2018.2806560', 'doi10.1007/978-1-4471-5102-9_170-2', 'doi10.1109/lra.2020.2965033', 'hal-01956087', 'doi10.1017/aer.2019.136', 'hal-02315122', 'doi10.1177/0278364919872544', 'doi10.1109/tro.2018.2876765', 'doi10.1109/mra.2019.2943395', 'hal-02495837', 'doi10.1109/lra.2018.2856526', 'hal-01935409', 'doi10.1007/978-3-030-20751-9_7', 'doi10.1109/lra.2018.2883375', 'doi10.1109/icra.2018.8461068', 'hal-01863424', 'hal-03180717', 'doi10.1111/cgf.13629', 'hal-02406552', 'hal-01888659', 'doi10.1109/lra.2019.2893611', 'hal-01877667', 'hal-01877761']}, {'structure': {'id': '193509361'}, 'startDate': 628473600000, 'endDate': 662601600000, 'sources': ['these1990REN10102']}], 'externalIds': [{'id': '675383', 'type': 'docid_hal'}, {'id': 'ArDkB', 'type': 'paysage'}, {'id': '1352008', 'type': 'docid_hal'}, {'id': '15722', 'type': 'id_hal'}, {'id': '059347856', 'type': 'idref'}, {'id': '98162', 'type': 'docid_hal'}], 'awards': [{'label': 'IEEE Fellow', 'date': 1356998400000, 'url': 'https://www.ieee.org/membership/fellows/index.html'}], 'lastUpdated': 1666101742414}, 'role': 'author', 'firstName': 'François', 'lastName': 'Chaumette', 'fullName': 'François Chaumette', 'affiliations': [{'structure': '200418341Y'}]}], 'isOa': False, 'publicationDate': 1388534400000, 'summary': {'default': 'Visual servoing refers to the use of computer vision data as input of real time closed loop control schemes to control the motion of a dynamic system, a robot typically [8,1].'}, 'keywords': {'default': []}}
#item1 = {'id': 'doi10.1016/j.cviu.2016.04.009', 'productionType': 'publication', 'title': {'default': 'Bio-inspired computer vision: Towards a synergistic approach of artificial and biological vision'}, 'authors': [{'role': 'author', 'firstName': 'N. V. Kartheek', 'lastName': 'Medathati', 'fullName': 'N. V. Kartheek Medathati', 'affiliations': [{'structure': '198318250R'}, {'structure': '201622040S'}]}, {'role': 'author', 'firstName': 'Heiko', 'lastName': 'Neumann', 'fullName': 'Heiko Neumann', 'affiliations': [{'structure': 'grid.6582.9'}]}, {'person': {'id': 'idref136863884', 'firstName': 'Guillaume S.', 'lastName': 'Masson', 'fullName': 'Guillaume S. Masson', 'gender': 'M', 'affiliations': [{'structure': {'id': '191318427'}, 'startDate': 754704000000, 'endDate': 788832000000, 'sources': ['these1994AIX11076']}, {'structure': {'id': '201220346T'}, 'startDate': 1354320000000, 'endDate': 1546214400000, 'sources': ['hal-01131100', 'doi10.1016/j.jphysparis.2013.08.001', 'doi10.1371/journal.pcbi.1005068', 'hal-01131099', 'doi10.1007/978-3-319-70742-6_6', 'doi10.1117/1.nph.4.3.031222', 'doi10.1016/j.neuropsychologia.2016.08.021', 'doi10.1167/16.15.6', 'hal-01377606', 'doi10.1152/jn.01152.2015', 'doi10.1016/j.cub.2017.04.022', 'hal-01589983', 'doi10.1002/9783527680863.ch12', 'hal-00783525', 'doi10.1038/nn.3411', 'doi10.1016/j.visres.2014.12.015', 'doi10.1021/acs.joc.7b02909', 'doi10.1016/j.visres.2015.03.013', 'doi10.3389/fncom.2013.00112', 'hal-01215526', 'hal-01131645', 'doi10.3389/fncir.2016.00037', 'hal-00850097']}, {'structure': {'id': '200012689X'}, 'startDate': 1448928000000, 'endDate': 1483142400000, 'sources': ['doi10.1016/j.neuropsychologia.2016.08.021']}], 'externalIds': [{'id': '180089', 'type': 'id_hal'}, {'id': '136863884', 'type': 'idref'}, {'id': '1143876', 'type': 'docid_hal'}, {'id': '1617955', 'type': 'docid_hal'}, {'id': '876222', 'type': 'docid_hal'}, {'id': '756530', 'type': 'docid_hal'}], 'lastUpdated': 1666102071697}, 'role': 'author', 'firstName': 'Guillaume S.', 'lastName': 'Masson', 'fullName': 'Guillaume S. Masson'}, {'person': {'id': 'idref060716800', 'firstName': 'Pierre', 'lastName': 'Kornprobst', 'fullName': 'Pierre Kornprobst', 'gender': 'M', 'affiliations': [{'structure': {'id': '200218384D'}, 'startDate': 1164931200000, 'endDate': 1199059200000, 'sources': ['tel-00457491']}, {'structure': {'id': '190609313'}, 'startDate': 880934400000, 'endDate': 915062400000, 'sources': ['these1998NICE5201']}, {'structure': {'id': '201622040S'}, 'startDate': 1448928000000, 'endDate': 1640908800000, 'sources': ['hal-01131645', 'doi10.1101/050393', 'hal-01377307', 'doi10.1523/eneuro.0134-15.2016', 'hal-02177784', 'hal-03396760', 'hal-03087009', 'hal-01383118', 'doi10.1016/j.cviu.2016.04.009', 'hal-01589983', 'hal-01292700', 'hal-01900574', 'hal-01589975', 'hal-01478391', 'hal-01377606', 'hal-02321739', 'hal-01896505', 'doi10.1016/j.cviu.2017.11.013', 'hal-01588737', 'hal-01482294', 'doi10.1038/s41598-017-11373-z', 'doi10.1038/srep24086', 'hal-01589946', 'hal-01368757', 'hal-01279999', 'doi10.1167/16.15.6', 'doi10.1088/1742-6596/756/1/012006']}, {'structure': {'id': '200919005Y'}, 'startDate': 1354320000000, 'endDate': 1483142400000, 'sources': ['hal-01215537', 'hal-01026507', 'doi10.1007/978-3-642-31208-3', 'doi10.1167/16.15.6', 'hal-01026508', 'hal-00920543', 'hal-01215541', 'hal-00920528', 'hal-01205376', 'hal-01078117', 'hal-01019953', 'hal-01131100', 'doi10.1016/j.image.2015.04.006', 'hal-00783525', 'hal-01235324', 'hal-01131099', 'doi10.1007/s10827-012-0409-5', 'hal-00850097', 'hal-01215526']}, {'structure': {'id': '0062126D'}, 'startDate': 1512086400000, 'endDate': 1546214400000, 'sources': ['doi10.1016/j.cviu.2017.11.013']}, {'structure': {'id': '198318250R'}, 'startDate': 1354320000000, 'endDate': 1640908800000, 'sources': ['doi10.1088/1742-6596/756/1/012006', 'doi10.1038/srep24086', 'doi10.1038/s41598-017-11373-z', 'doi10.1167/16.15.6', 'doi10.1007/s10827-013-0465-5', 'doi10.1101/050393', 'hal-01131645', 'hal-01292700', 'hal-01482294', 'doi10.1016/j.cviu.2017.11.013', 'hal-01588737', 'hal-01478391', 'doi10.1007/978-3-319-20904-3_2', 'hal-01900574', 'hal-01279999', 'hal-01368757', 'hal-01589946', 'hal-01383118', 'hal-03396760', 'hal-03087009', 'hal-02321739', 'hal-01896505', 'hal-01377606', 'hal-01589975', 'hal-02177784', 'doi10.1523/eneuro.0134-15.2016', 'hal-01377307', 'hal-01589983', 'doi10.1016/j.cviu.2016.04.009']}], 'externalIds': [{'id': '060716800', 'type': 'idref'}, {'id': '0000-0003-4906-1368', 'type': 'orcid'}, {'id': '6602268862', 'type': 'Scopus Author ID'}, {'id': '15713', 'type': 'id_hal'}, {'id': '195121', 'type': 'docid_hal'}], 'lastUpdated': 1666101759241}, 'role': 'author', 'firstName': 'Pierre', 'lastName': 'Kornprobst', 'fullName': 'Pierre Kornprobst', 'affiliations': [{'structure': '198318250R'}, {'structure': '201622040S'}]}], 'isOa': False, 'publicationDate': 1472688000000, 'summary': {'default': 'Studies in biological vision have always been a great source of inspiration for design of computer vision algorithms. In the past, several successful methods were designed with varying degrees of correspondence with biological vision studies, ranging from purely functional inspiration to methods that utilise models that were primarily developed for explaining biological observations. Even though it seems well recognised that computational models of biological vision can help in design of computer vision algorithms, it is a non-trivial exercise for a computer vision researcher to mine relevant information from biological vision literature as very few studies in biology are organised at a task level. In this paper we aim to bridge this gap by providing a computer vision task centric presentation of models primarily originating in biological vision studies. Not only do we revisit some of the main features of biological vision and discuss the foundations of existing computational studies modelling biological vision, but also we consider three classical computer vision tasks from a biological perspective: image sensing, segmentation and optical flow. Using this task-centric approach, we discuss well-known biological functional principles and compare them with approaches taken by computer vision. Based on this comparative analysis of computer and biological vision, we present some recent models in biological vision and highlight a few models that we think are promising for future investigations in computer vision. To this extent, this paper provides new insights and a starting point for investigators interested in the design of biology-based computer vision algorithms and pave a way for much needed interaction between the two communities leading to the development of synergistic models of artificial and biological vision.'}, 'keywords': {'default': ['Canonical computations', 'Dynamic sensors', 'Event based processing', 'Feedback', 'Form-motion interactions', 'Lateral interactions', 'Multiplexed representation', 'Population coding', 'Soft selectivity'], 'en': ['Dynamic sensors', 'Multiplexed representation', 'Population coding', 'Event based processing', 'Canonical computations', 'Soft selectivity', 'Feedback', 'Lateral interactions', 'Form-motion interactions']}}
#keyword='machine learning'
#req_item = {'id': 'hal-01324915', 'productionType': 'publication', 'title': 'AN ILLUMINANT-INDEPENDENT ANALYSIS OF REFLECTANCE AS SENSED BY HUMANS, AND ITS APPLICABILITY TO COMPUTER VISION'}

def get_creds(key):
    f = open("auth.json")
    creds = json.load(f)
    username = creds.get(key)[0]
    password = creds.get(key)[1]
    return(username,password)


def create_main_nodes(tx,id,productionType,title,summary,pubdate,keyword):
    result = tx.run("""MERGE (p:Paper {id:$id,ptype:$ptype,title:$title,summary:$summary,publicationDate:datetime({epochSeconds:$pubdate})})
    MERGE (k:keyword {name:$keyword})
    MERGE (p)-[r:CONTAINS]->(k)
    """,id=id,ptype=productionType,title=title,summary=summary,pubdate=pubdate,keyword=keyword)
    summary = result.consume()
    return summary

# def create_main_nodes(tx,id,productionType,keyword):
#     result = tx.run("""MERGE (p:Paper {name:'Paper',id:$id,ptype:$ptype})
#     MERGE (k:keyword {name:$keyword})
#     MERGE (p)-[r:CONTAINS]->(k)
#     """,id=id,ptype=productionType,keyword=keyword)
#     summary = result.consume()
#     return summary

def create_author_nodes(tx,p_id,id,role,fullname,gender):
    result = tx.run("""MATCH (p:Paper {id:$p_id})
    MERGE (a:Author {id:$id,role:$role,name:$fullname,gender:$gender})
    MERGE (p)-[r:WRITTEN_BY]->(a)
    """,p_id=p_id,id=id,role=role,fullname=fullname,gender=gender)
    summary2 = result.consume()
    return summary2

def est_connection():
    URI = "neo4j://localhost/7474"
    AUTH = get_creds('neo4j creds')
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        try:
            session_ = driver.session(database="neo4j")
            return session_
        except Exception as e:
            print("Error:",e)
            return(e)


def check_authors(x):
    if(x.get('role')):
        role = x.get('role')
    else:
        role = str("")
    if(x.get('gender')):
        gender = x.get('gender')
    else:
        gender = str("")
    if(x.get('fullName')):
        fullName = x.get('fullName')
    else:
        fullName = str("")
    
    return [role,fullName,gender]


def create_network(con_session,keyword,**kwargs):

    #session1 = est_connection()
    session1 = con_session

    title = " "
    if(kwargs.get('title').get('default')):
        title = str(kwargs.get('title').get('default'))
    elif(kwargs.get('title').get('en')):
        title = str(kwargs.get('title').get('en'))
    else:
        title = " "
    
    summary = " "
    if(kwargs.get('summary').get('default')):
        summary = kwargs.get('summary').get('default')
    elif (kwargs.get('summary').get('en')):
        summary = kwargs.get('summary').get('en')
    else:
        summary = " "
    
    param_list = [str(kwargs.get('id')),str(kwargs.get('productionType')),str(title),str(summary),int(kwargs.get("publicationDate")/1000),keyword]
    #param_list = [str(kwargs.get('id')),str(kwargs.get('productionType')),keyword]
    #print(param_list)
    #print(param_list)
    #time.sleep(10)
    #print(str(kwargs.get('id')))
    session1.execute_write(create_main_nodes,*param_list)
    #print("main nodes cerated")

    for dict1 in kwargs['authors']:
        #print(dict1)
        if(dict1.get('person')):
            author_lst = [str(kwargs.get('id')),dict1.get('person').get('id')]
            author_lst = author_lst + check_authors(dict1.get('person'))
        else:
            author_lst = [str(kwargs.get('id')),str("")]
            author_lst = author_lst + check_authors(dict1)


        #print(author_lst)
        session1.execute_write(create_author_nodes,*author_lst)
        #print("author nodes created")
    
    

# ss  = est_connection()
# create_network(ss,'machine',**item1)
# ss.close()
# for x in item1['authors']:
#     check_authors(x)
