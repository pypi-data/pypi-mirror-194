import sys
import requests

from . import json_xp as json
from .class_small_db import Small_db 

from .kraken_class_thing import Thing
from kraken_thing.kraken_api import Kraken_api



class Things:
    """
    A class used to represent several Thing 

    ...

    Attributes
    ----------
    json : str
        json representation of the content    

    Methods
    -------
    load(records)
        Loads alist of records into several Thing class objects
    dump()
        Dumps all included Thing objects as list of dict
    update_record_ref()
        Updates all record_ref (record_type, record_id) for all Thing objects and values in Thing objects
    attributes:    
            api:    access get, exists,  post to db api
    """

    def __init__(self):


        self.db = Small_db(2)
        
        self.db_index = {}

        self.db_ids = Small_db(2)    # Keeps track of previous ids

        self.api = Kraken_api(self)

    
    def __str__(self):
        '''
        '''

        content = 'Things collection size: ' + str(len(self.db)) + '\n'
        for i in self.get():
            content += str(i.record_type) + '/' + str(i.record_id) + ' '
            if i.name:
                content += str(i.name) + ' '
            if i.url:
                content += str(i.url) + ' '
            content += '\n'
        
        return content
        
    
    def __repr__(self):
        '''
        '''
        return self.json

    def __len__(self):
        '''
        '''
        return len(self.db)
        
    def __contains__(self, thing):
        '''
        '''
        thing = self.get(thing.record_type, thing.record_id)
        if thing:
            return True
        return False
        
    def __iter__(self):
        '''
        '''
        for i in self.get():
            yield i
        
    
    def __add__(self, other):
        '''
        '''
        things = Things()

        for i in self.get():
            things.append(i)
        for i in other.get():
            things.append(i)

        return things

    def append(self, thing):
        '''Add thing to self database
        '''

        # Add self-reference to thing
        if not thing._things:
            thing._things = self
        
        # Deal with list
        if isinstance(thing, list):
            for i in thing:
                self.append(i)
            return


        # Create if doesn't exist
        db_record_id = self.db_ids.get(thing.record_type, thing.record_id)
        
        if not db_record_id:
            self.db.post(thing, thing.record_type, thing.record_id)
            self.db_ids.post(thing.record_id, thing.record_type, thing.record_id)

        # Merge if exist
        for record_id in thing.get('@id'):
            db_record_id = self.db_ids.get(thing.record_type, record_id)
            if db_record_id:
                db_thing = self.db.get(thing.record_type, db_record_id)
                
                if db_thing and db_thing is not thing:
                    r_id1 = db_thing.record_id
                    r_id2 = thing.record_id
                    
                    db_thing.merge(thing)
                    thing._observations = db_thing._observations
                    thing = db_thing
                    self.db.post(thing, thing.record_type, thing.record_id)
                    
                    # Update record_ref
                    old_record_id = r_id1 if r_id1 != thing.record_id else r_id2
                    self.update_record_ref(thing.record_type, old_record_id, thing.record_type, thing.record_id)
                    

        # Delete old record_ids
        for i in thing.get('@id'):
            if i != thing.record_id:
                self.db.delete(thing.record_type, i)
        
        # Create records for previous record ids
        for i in thing.get('@id'):
            self.db_ids.post(thing.record_id, thing.record_type, i)
            
        
    def drop(self, record_type, record_id):
        '''Removes thing from database if exist
        '''
        thing = self.get(record_type, record_id)
        self.db.remove(thing)
        self.db_index[record_type][record_id] = None
        return
        

    def new(self, record_type = None, record_id = None):
        '''
        '''
        if record_type and record_id:
            t = self.get(record_type, record_id)

        if not t:
            t = Thing(record_type, record_id)
            self.set(t)
            
        return t
    
    def get(self, record_type=None, record_id=None):
        '''
        '''

        if record_id:
            default = None
        else:
            default = []

        if not record_id:
            return self.db.get(record_type, record_id, default)
            
        official_record_id = self.db_ids.get(record_id)
        if official_record_id:
            record_id = official_record_id
        
        return self.db.get(record_type, record_id, default)


    def load(self, records):
        '''
        '''

        if not isinstance (records, list):
            records=[records]

        for i in records:
            t = Thing()
            t.load(i)
            self.append(t)
            
        return            

    
    def dump(self):
        '''Returns list of dict of all Things
        '''

        records = []
        for i in self.db:
            records.append(i.dump())

        return records

    """observations
    """

    def get_observation(self, observation_id):
        '''Retrieve a single observation from things
        '''

        if not observation_id:
            return None
        
        for i in self.get():
            o = i.get_observation(observation_id)
            if o:
                return o

        return None
            

    
    """properties
    """
    @property
    def json(self):
        '''
        '''
        return json.dumps(self.dump())


    @property
    def info(self):
        '''Returns dict with details on collection
        '''

        # Get record_types
        record_types = {}
        for i in self.db:
            if not record_types.get(i.record_type, None):
                record_types[i.record_type] = 0
            record_types[i.record_type] +=1

        # Assmeble results
        record = {
            'len': len(self.db),
            'record_types': record_types,
            'memory (kb)': self.memory_size

        }
        return record
            


    
    
    '''Methods
    '''

    def update_record_ref(self, old_record_type, old_record_id, new_record_type, new_record_id):
        '''Updates all values with new record_ref
        '''

        if old_record_type == new_record_type and old_record_id == new_record_id:
            return 
        
        # Update  
        for i in self.db:

            # Update type and id
            if i.record_type == old_record_type and i.record_id == old_record_id:
                i.record_type = new_record_type
                i.record_id = new_record_id

            # Update values
            i.update_record_ref(old_record_type, old_record_id, new_record_type, new_record_id)
        


    
    def reindex_original_record_ids(self, records = None):
        '''return list of tuples of ids that were added
        '''
        if not records:
            records = self.db.get()
            
        if not isinstance(records, list):
                records = [records]

        new_ids = []
        for i in records:
            for record_id in i.record_ids:
                t = self.db_ids.get(i.record_type, record_id)
                if not t and i.record_id != record_id:
                    new_ids.append((i.record_type, record_id))
                self.db_ids.post(i.record_type, record_id, i.record_id)
        return new_ids
            
    '''db_ids
    '''

    def set_id(self, record_type, old_record_id, new_record_id):
        '''Add old id to db
        '''
        if not self.db_ids.get(record_type, None):
            self.db_ids[record_type] = {}
                
        self.db_ids[record_type][old_record_id] = new_record_id

        
        
    
    '''System properties
    '''
    @property
    def memory_size(self):
        '''Returns memory size taken by object
        '''
        size = 0
        size += sys.getsizeof(self) / 1024

        for i in self.db:
            size += i.memory_size
        
        return round(size, 2)