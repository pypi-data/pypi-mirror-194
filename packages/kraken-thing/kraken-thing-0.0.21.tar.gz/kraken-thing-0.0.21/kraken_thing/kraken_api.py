from functools import cached_property
import requests
import os
import json

cache = {}


class Kraken_api:
    '''Class taking a thing as input and adding api functionalities.
    '''

    def __init__(self, thing):
        '''
        '''
        self.url = os.getenv('API_URL')
        self.thing = thing

    @property
    def api_url(self):
        '''
        '''
        if not self.url:
            self.url = 'https://engine.krknapi.com'
        return self.url + '/api'

    @property
    def headers(self):
        '''
        '''
        headers = {'Content-Type': 'application/json'}
        return headers


        

    def cache_post(self, record):
        '''Add a record to cache
        '''
        if isinstance(record, list):
            for i in record:
                self.cache_post(i)
            return

        record_type = record.get('@type', None)
        record_id = record.get('@id', None)
        
        if not cache.get(record_type, None):
            cache[record_type] = {}
        if not cache.get(record_type, {}).get(record_id, None):
            cache[record_type][record_id] = True
        
        return

    def cache_get(self, record):
        '''
        '''
        record_type = record.get('@type', None)
        record_id = record.get('@id', None)
        
        return cache.get(record_type, {}).get(record_id, False)

    
    def get(self, query = {}):
        '''
        '''

        if query:
            params = query
        else:
            params = getattr(self.thing, 'record_ref', None)

        
        try:
            r = requests.get(self.api_url, headers=self.headers, params=params)

            if r.status_code == 200:

                records = r.json()
                self.cache_post(records)
                self.thing.load(records)
                
                return True
            return False
        except Exception as e:
            print(e)
            return e

    def post(self):
        '''
        '''
        data = self.thing.json

        try:
            r = requests.post(self.api_url, headers=self.headers, data=data)
            if r.status_code == 200:
                records = r.json()
                self.thing.load(records)
                self.cache_post(records)
                return True
            return False
        except Exception as e:
            print('Post error', e)
            return e

    #@cached_property
    @property
    def exists(self):
        '''
        '''

        # Check in cache
        if self.cache_get(self.thing.record_ref):
            return True
        return self.get()
            
    def search(self, query):
        '''
        '''
        