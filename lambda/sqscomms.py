import boto3
from time import sleep
import json
import time

class SQSComms:

    def __init__(self, access_key, access_secret, region, queue_url):
        self.queue_url = queue_url

        self.access_key = access_key
        self.access_secret = access_secret
        self.region = region

        # Get the service resource
        self.client = boto3.client('sqs',aws_access_key_id = self.access_key, aws_secret_access_key = self.access_secret, region_name = self.region)


    def post_message(self, message):
        response = self.client.send_message(QueueUrl = self.queue_url, MessageBody= message)
        return response


    def read_message(self):
        response = self.client.receive_message(QueueUrl = self.queue_url, MaxNumberOfMessages = 1, WaitTimeSeconds=20)
        message = response['Messages'][0]['Body']
        receipt = response['Messages'][0]['ReceiptHandle']
        response = self.client.delete_message(QueueUrl = self.queue_url, ReceiptHandle = receipt)
        return message

    def read_messages(self):
        response = self.client.receive_message(QueueUrl = self.queue_url, MaxNumberOfMessages = 10, WaitTimeSeconds=20)
        delete_batch = []
        messages = []
        for message in response.get('Messages') or []:
            messages.append(message['Body'])
            delete_batch.append({'Id': message['MessageId'],
                                'ReceiptHandle': message['ReceiptHandle']})
        if delete_batch:
            self.client.delete_message_batch(QueueUrl=self.queue_url, Entries=delete_batch)
        return messages
    
    def search_directive(self, directive):
        messages = []

        timeout = time.time() + 6
        while len(messages) == 0 and time.time() < timeout:
            response = self.client.receive_message(QueueUrl = self.queue_url, MaxNumberOfMessages = 10, WaitTimeSeconds=4)
            for message in response.get('Messages') or []:
                mess = json.loads(message['Body'])
                if mess["messageId"] == directive:
                    messages.append(mess["body"])
                    receipt = message['ReceiptHandle']
                    self.client.delete_message(QueueUrl = self.queue_url, ReceiptHandle = receipt)
            if not messages:
                sleep(1)
        if messages:
            return messages[0]
        return None