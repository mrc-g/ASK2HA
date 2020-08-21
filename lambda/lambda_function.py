import json

from config import *
from sqscomms import *
from dyncomms import *

comms= SQSComms(access_key, access_secret, region, queue_url)
dyncomms = DynComms(access_key, access_secret, region, table)

def lambda_handler(request, context):
    try:
        req = json.dumps(request)
        comms.post_message(req)

        response = dyncomms.search_directive(request["directive"]["header"]["messageId"])
        if not response:
            comms.post_message(json.dumps({"ERROR":"EMPTY!!!"}))
        return response
    except ValueError as error: #debugging
        comms.post_message(json.dumps(error))
        raise
    except:
        comms.post_message(json.dumps({"ERROR":"aaa"}))
        raise
