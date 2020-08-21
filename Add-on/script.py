from sqscomms import SQSComms
from hacomms import HAComms
from dyncomms import DynComms
from botocore.exceptions import EndpointConnectionError

import json
from time import sleep
import queue
from threading import Thread

with open("/data/options.json", "r") as json_file:
    options = json.load(json_file)

    ha_token = options["home_assistant_token"]
    access_key = options["aws_access_key"]
    access_secret = options["aws_access_secret"]
    region = options["aws_region"]
    queue_url = options["sqs_queue_url"]
    table = options["dynamodb_table"]

sqscomms= SQSComms(access_key, access_secret, region, queue_url)
dyncomms = DynComms(access_key, access_secret, region, table)
hacomms = HAComms(ha_token)

print("start", flush=True)
dyncomms.purge()

def worker(r):
    print()
    directive = json.loads(r)
    if "directive" not in directive:
        print("not a directive", flush=True)
        print(directive, flush=True)
        return
    event = hacomms.handle_event(directive)
    
    response = {"messageId": directive["directive"]["header"]["messageId"], "body": event}
    print("response", response["messageId"], flush=True)
    dyncomms.send_response(response)


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print(e)
            finally:
                self.tasks.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.tasks = queue.Queue(num_threads)
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        self.tasks.put((func, args, kargs))

    def wait_end(self):
        self.tasks.join()
    
pool = ThreadPool(20)

def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + '.' + obj.__class__.__name__

try:
    while True:
        print(".", flush=True,end="")
        res = None
        try:
            res = sqscomms.read_messages()
        except EndpointConnectionError as e:
            print(e, flush=True)
            sleep(10)
            continue
        for r in res:
            pool.add_task(worker, r)
except Exception as e: 
    print(e, flush=True)
    print(get_full_class_name(e), flush=True)
    pool.wait_end()