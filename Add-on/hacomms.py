#!/usr/bin/env python3.6
# coding: utf-8

import json
import requests

class HAComms:
    def __init__(self, token, url = None):
        if not url:
            self.url = "http://homeassistant:8123/api/alexa/smart_home"
        else:
            self.url = url #for testing
            
        self.token = token

    def handle_event(self, event):
        session = requests.Session()
        session.headers = {
            'Authorization': f'Bearer {self.token}',
            'content-type': 'application/json',
        }

        try:
            r = session.post(self.url, data=json.dumps(event), timeout=(None, None))
            r.raise_for_status()
            return r.json()
        except requests.exceptions.ReadTimeout:
            return None
