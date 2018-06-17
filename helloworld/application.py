#!flask/bin/python
#added this code from gist 1 slack 15-04-18
import sys, os
sys.path.append(os.path.join(os.path.dirname(sys.path[0])))

import json
from flask import Flask, Response, request, render_template
from helloworld.flaskrun import flaskrun
#add this for th
import requests
import boto3
import datetime

application = Flask(__name__)

@application.route('/', methods=['GET'])
def get():
    return Response(json.dumps({'Output': 'Hello Get World'}), mimetype='application/json', status=200)
    
  #adding a route for getting the IP address
@application.route('/get_ip', methods=['GET'])

#added this function for getting the IP address  
def get_ip():
    #print(get_ip_meta())
    return Response(json.dumps(get_ip_meta()), mimetype='application/json', status=200)
    
    

    # return Response(json.dumps({'Output': 'Hello Get All World'}), mimetype='application/json', status=200)
@application.route('/temp/<temp>', methods=['POST'])

def get_temp(temp):
    # get ip metadata from the fuction
    response = get_ip_meta()
    # create a session for boto to access the credentials that the ec2 holds
    my_ses = boto3.Session(region_name = 'us-east-2')
    # connect to the resource dynmodb using the session
    dynamodb = my_ses.resource('dynamodb')
    # refer to the table
    table = dynamodb.Table('eb_try_logger')

    item={
    'ip_addr': str(response), 
    'path': temp,
    'datetime': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    'time': datetime.datetime.now().strftime("%H:%M:%S"),
    'ip_meta' : response, # res_data
    'name':'yonatan'
    }
    
    print(item)
    # insert the item
    table.put_item(Item=item)
    
    return Response(json.dumps(item), mimetype='application/json', status=200)

@application.route('/', methods=['POST'])
def post():
    return Response(json.dumps({'Output': 'Hello Post World in cloud 9'}), mimetype='application/json', status=200)


def get_ip_meta():
    user_ip = str(request.environ['REMOTE_ADDR'])
    service_url = 'http://ipinfo.io/{}'.format(user_ip) 
    return requests.get(service_url).json()

@application.route('/<string:form>/')
def static_page(form):
    return render_template('%s.html' % form)
    
if __name__ == '__main__':
    flaskrun(application)