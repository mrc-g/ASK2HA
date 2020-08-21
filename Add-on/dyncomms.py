import boto3
from time import sleep
import json
import time
from decimal import Decimal

class DynComms:

    def __init__(self, access_key, access_secret, region, table):

        self.access_key = access_key
        self.access_secret = access_secret
        self.region =region

        # Get the service resource
        self.dynamodb = boto3.resource('dynamodb',aws_access_key_id = self.access_key, aws_secret_access_key = self.access_secret, region_name = self.region)
        self.table = self.dynamodb.Table(table)

    def send_response(self, response):
        response = json.loads(json.dumps(response),parse_float=Decimal)
        self.table.put_item(
            Item=response
        )

    def purge(self):
        print(self.table.creation_date_time)

        scan = self.table.scan()
        try:
            print(len(scan['Items']))
            with self.table.batch_writer() as batch:
                for each in scan['Items']:
                    batch.delete_item(
                        Key={
                            'messageId': each['messageId'],
                    }
                )
        except KeyError:
            pass

    def search_directive(self, directive):
        timeout = time.time() + 2.1
        sleep(0.5)
        while time.time() < timeout:
            try:
                response = self.table.get_item(
                    Key={
                        'messageId': directive,
                    }
                )
                item = response['Item']["body"]

                self.table.delete_item(
                    Key={
                        'messageId': directive,
                    }
                )

                return item
            except KeyError:
                sleep(0.)
        raise
