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
    return HttpResponse("Hello, world. You're at the polls index.")


def elk():
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
    s = Search(index = 'compend').using(client).query('match_all')
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
