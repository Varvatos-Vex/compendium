from django.shortcuts import render
from django.http import HttpResponse
import json
#-------------------import fo Elastic query--------
from elasticsearch import Elasticsearch, exceptions
from elasticsearch_dsl import Search
from elasticsearch_dsl import UpdateByQuery
from elasticsearch_dsl import Q
import json, time
import csv
import ssl

from elasticsearch_dsl.search import Request

DOMAIN = "elastic:Qwaszx#123@localhost"
PORT = 9200
host = str(DOMAIN) + ":" + str(PORT)
client = Elasticsearch(
    ['localhost'],
    http_auth=('elastic', 'Qwaszx#123'),
    scheme="http",
    ca_certs=False,
    port=9200,
    verify_certs=False,
)


def index(request):
    #elk()
    #update_by_query(1)
    #ingestData()
    return HttpResponse("Hello, world. You're at the polls index.")


def elk():
    DOMAIN = "elastic:Qwaszx#123@localhost"
    PORT = 9200
    host = str(DOMAIN) + ":" + str(PORT)
    '''client = Elasticsearch(
        ['localhost'],
        http_auth=('elastic', 'Qwaszx#123'),
        scheme="http",
        ca_certs=False,
        port=9200,
        verify_certs=False,
    )'''
    global client
    s = Search(index = 'compend').using(client).query('match', uuid = '3')
    print("Search Done")
    response = s.execute()
    for res in response:
        print(res.actor)


#--------------------------This module use to find the actor details----------------
def actor_details(request,actor):
    actor_details = find_actor(actor)
    return HttpResponse(actor_details)


def find_actor(actor):
    s = Search(index = 'compend').using(client).query('match', actor = actor)
    response = s.execute()
    if response['hits']['total']['value'] >= 1:
        actor_details = ''
        for res in response:
            actor_details = res.to_dict()
        return json.dumps(actor_details)
    else:
        return ("Not Found")

import datetime

#--------------------update Query Testing----------------
def update_by_query(id):
    newDate = datetime.datetime.now()
    last_updatedBy = 'Manish'
    q= {
    "query":
        {
        "term":
            {
            "uuid.keyword":
                {
                "value": id
                }
            }
        },
        "script": 
            {
            "inline" : "ctx._source.upadate.last_updated_date = '" + str(newDate) + "'; ctx._source.upadate.last_updated_by = '" + last_updatedBy +"';",
            "lang"   : "painless"
            }
    }

    global client
    try:
        res = client.update_by_query(index = 'compend', body = q)
        print(json.dumps(res, indent=4))

    except exceptions.ConnectionError as err:
        print ("\nElasticsearch info() ERROR:", err)
        print ("\nThe client host:", host, "is invalid or cluster is not running")
        client = None



#--------------------------Insert New Data----------------
def ingestData():
    timestapDate = datetime.datetime.now()
    doc = {"@timestamp":timestapDate ,"uuid" : "3","actor" : "Lazarus","suspected_state_sponsor" : "North Korea","last_known_activity" : "April 2021","description" : "LABYRINTH CHOLLIMA is one of the most prolific Democratic People’s Republic of Korea (DPRK) adversaries tracked by CrowdStrike and has been active since 2009. CrowdStrike assesses this adversary is likely affiliated with Bureau 121 of the DPRK’s Reconnaissance General Bureau (RGB) and primarily conducts espionage operations aimed at the U.S. and Republic of Korea (RoK) militaries and defense industrial base, the technology sector, and cryptocurrency users and/or exchanges. A subsection of this adversary's activities also appear financially motivated. \n LABYRINTH CHOLLIMA maintains an extensive toolset consisting of implants targeting Windows, Linux, MacOS, and Android operating systems. In 2020, CrowdStrike Intelligence observed the deployment of a steady stream of nearly a dozen new implants, suggesting this adversary appears to be in a constant state of malware development. LABYRINTH CHOLLIMA’s Hawup, first observed operationally in 2015, defines the contours of this adversary’s modern activity. Nearly all of LABYRINTH CHOLLIMA’s tools bear some relation to Hawup—either directly or indirectly. Notably, there are numerous technical overlaps between LABYRINTH CHOLLIMA and STARDUST CHOLLIMA malware, indicating the two adversaries likely work in close collaboration and had access to the same code framework prior to subsequent tooling divergence increasingly observed between these adversaries.","recent_activity" : "During April 2021, CrowdStrike Falcon Complete identified a new variant of Jeus at a UK_ based entity in the financial sector. The initial infection vector is not known, but there was some evidence on the host of a previous variant of Jeus, using the fake Ant2Whale digital assets application package. This indicates the sample may have been deployed by a similar fake application package or a previous variant of the malware. Additionally, during the same period, CrowdStrike Intelligence observed this adversary circulating updated variants of Stackeyflate. The updated variant no longer use the OpenSSL library and appear modified as an attempt to evade signature_based detection. ","alias" : ["HIDDEN COBRA","BeagleBoyz","Lazarus Group","APT_C_26","Zinc","Black Artemis"],"suspected_victims": ["Argentina","Australia","Belgium","Brazil","Canada","China","Denmark","Estonia","Germany","Hungary","India","Ireland","Israel","Italy","Japan","Middle East North Africa (MENA)","Netherlands","New Zealand","Poland","Russian Federation","Saudi Arabia","Singapore","South Korea","Spain","Sweden","Turkey","Ukraine","United Kingdom","United States","Western Europe"],"target_inductries" : ["Academic","Aerospace","Agriculture","Cryptocurrency","Defense","Energy","Financial Services","Government","Healthcare","Industrials and Engineering","Media","Military","National Government","Opportunistic","Pharmaceuticals","Technology","Transportation"],"tags" : [],"refs": [],"upadate" :{"last_updated_date" : "","last_updated_by" : ""},"kill_chain" : {"reconnaissance" : "Undetermined","weaponization" : ["Hangul Word Processor documents", "Microsoft Word documents", "Malicious Cryptocurrency Trading Applications"],"delivery" : ["Spear phishing"],"exploitation" : ["CVE_2015_6585", "CVE _2017_8291", "Macro enablement"],"installation" : ["Hawup RAT", "TwoUp RAT", "DarkEdge RAT", "WolfRAT", "SheepRAT", "Manuscrypt RAT", "WebTroy Manuscrypt variant", "MataNet RAT", "Hawup Android Variant", "Manup Android Malware", "HtDnLoader ", "HtDnDownloader", "NedDnLoader", "Slumber Downloader", "KeyMarble RAT", "Keccak Loader", "Jeus Implant", "UnderGround RAT", "TaintedScribe", "XcTRAT", "CRAT", "Hoplight", "BUFFETLINE", "VHD Ransomware", "Hansom Ransomware", "Destover", "GOPWiper", "Joanap", "Brambul", "Dozer", "MYDOOM", "Kordos", "KorDLLBot", "Milt RAT", "Torisma", "Venus Webshell", "Stackeyflate", "HTTPHelper", "RomeoGolf", "OpenSSL Downloader", "HotPlugin"],"cnc" : ["C2 communications mimic TLS"],"action" : ["Theft of sensitive information, Currency Generation"]}}
    res = client.index(index='compend', body=doc)    
    print(res)