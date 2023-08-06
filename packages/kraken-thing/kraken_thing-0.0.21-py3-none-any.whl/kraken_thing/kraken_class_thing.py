import sys
import datetime
import uuid
from urllib.parse import urlparse

from kraken_thing.kraken_api import Kraken_api

from kraken_schema_org import kraken_schema_org as kraken_schema
#from . import json_xp as json


from . import json_xp as json

from . import normalize_id
from . import normalize_value as nv
from . import key_mapping
from . import dict_helper 

from .kraken_class_observations import Observations



class Thing:

    def __init__(self, record_type = None, record_id = None):
        """
        A class to represent a schema.org Thing

        methods:
            get(key):
                retrieve all values for given key
            get_best(key):
                return single best value for given key
            set(key, value): 
                set a new value for a given key
            load(record):
                load all values in record
            dump():
                output a records with all values
        attributes:    
            api:    access get, exists, post to db api
                
        
        """
        
        self._observations = Observations()   # Gets replaced with common if in Things
                   
        self._things = None     # Reference to things collection

        # Metadata
        self._source_observations_id = []
        self._object = None
        self._agent = None
        self._instrument = None
        self._credibility = None
        self._date = None
        self.api = Kraken_api(self)
        
        
        # Load record if record instead of record_type
        if record_type and isinstance(record_type, dict):
            self.load(record_type)
        else:
            self.record_type = record_type
            self.record_id = record_id

            
        # Add id if none
        if not self.record_id:
            self.record_id = str(uuid.uuid4())

    
    def __str__(self):
        
        return str(self.summary)

    def __repr__(self):
        return str(self.dump())


    def __eq__(self, other):
        """
        """

        if not issubclass(type(other), Thing):
            return False
        
        if self.record_id and self.record_id == other.record_id and self.record_type and self.record_type == other.record_type:
            return True
        else:
            return False

    def __add__(self, other):
        """
        """
        
        new_t = Thing()

        #Load self record
        new_t._observations.set(self._observations.get())

        # Load other record
        new_t._observations.set(other._observations.get())

        return new_t

    def __setattr__(self, attr, value):
        '''
        '''
        if attr.startswith('_') or attr in self.__dict__.keys():
            self.__dict__[attr] = value
        else:
            attr = key_mapping.get(attr, attr)
            self.set(attr, value)

    def __getattr__(self, attr):
        '''
        '''
        if attr.startswith('_') or attr in self.__dict__.keys():
            return self.__dict__.get(attr, None)
            
        else:
            attr = key_mapping.get(attr, attr)
            return self.get_best(attr)
        
    
    def merge(self, other):
        '''Add obs from other in self
        '''
                
        # Copy observations
        observations = other._observations.get()
        self._observations.set(observations)
            
        return


    @property
    def summary(self):
        '''
        '''
        content = []
        content.append('@type: ' + str(self.record_type) )
        content.append('@id: ' + str(self.record_id) )
        content.append(40 * '-' )

        for i in self._observations.get():
            content.append(str(i.key) + ': ' + ((20 - len(i.key)) * ' ' )+ str(i.value) )
        return '\n'.join(content)


    @property
    def summary_sources(self):
        '''Starting with no sources, shows hierarchy
        '''
        content = []
        base_obs = []
        for i in self._observations.get():
            if not i.source_observations_id:
                base_obs.append(i)


        def recurse_relations_sources(obs, level=0):
            content = []
            for i in obs:
                hierarchy = str((level * 4 * ' ')) + str((20 - level * 4) * '-') + '  '
                content.append(hierarchy + str(i))
                content += recurse_relations_sources(i.child_observations, level + 1)
                
            return content
        
        content = recurse_relations_sources(base_obs)
        
        return '\n'.join(content)

    @property
    def summary_childs(self):
        '''For each, shows where it comes from
        '''
        content = []
        obs = self._observations.get()

        def recurse_relations_childs(obs, level=0):
            content = []
            for i in obs:
                hierarchy = str((level * 4 * ' ')) + str((20 - level * 4) * '-') + '  '
                content.append(hierarchy + str(i))
                content += recurse_relations_childs(i.source_observations, level + 1)
                
            return content
        content = recurse_relations_childs(obs)
        
        return '\n'.join(content)
            
            
    
    """ Main
    """
    
    def set(self, key, value, metadata = None):
        """Create a new observation with key value. 
        """

        metadata = metadata if metadata else self.metadata
        
        # Error handling
        if not value:
            return 
            
        # Handle lists (in reverse so it conserves proper order)
        if isinstance(value, list) and not isinstance(value, str):
            for i in reversed(value):
                self.set(key, i, metadata)
            return

        # Handle thing as value
        if isinstance(value, dict) and '@type' in value.keys():
            new_value = Thing()
            new_value.load(value)
            new_value.metadata = metadata
            value = new_value            

            
        # Initialize 
        observations = []
        
        # Get original observation (as is key value)
        o = self._observations.new(key, value, metadata)
        if o:
            observations.append(o)

        # Normalize observation key value
        o = self.normalize_observation(observations[-1])
        if o:
            observations.append(o)
        
        # normalize record_id
        o = self.normalize_record_id_from_observation(observations[-1])
        if o:
            observations.append(o)
        
        # Add obs to db
        self._observations.set(observations)
        

    def get(self, key, include_non_valid = True):
        """
        Retrieve all values for given key from best to worst

        
        Parameters
        ----------
        key: str
            Key of the value to get
        invclude_non_valid: includes obs where key or value are not validated
        """
        if not key.startswith('@') and not key.startswith('schema:'):
            key = 'schema:' + key

        obs = self._observations.get_by_key(key, include_non_valid)

        values = []                            
        for i in obs:
            if i.value not in values:
                values.append(i.value)

        return values
        

    def get_best(self, key):
        '''Returns best value
        '''
        
        obs = self._observations.get_by_key(key)

        if obs and len(obs)> 0:
            return obs[0].value
        else:
            return None


        
    def load(self, record, append=False):
        """
        Load complete record
        
        Parameters
        ----------
        record: dict
            Dict of the record to load. Also accepts json.
        append: bool
            If true, will append value to existing value
        """

        # Handle list
        if isinstance(record, list):
            for i in record:
                self.load(i)
            return
        
        # Handle json
        if isinstance(record, str):
            record = json.loads(record)
                
        # Add id if none
        for key, value in record.items():
            self.set(key, value)
            
        return
     
        

    def dump(self):
        """Dump complete record without class
        """

        # Add id if none
        if self.record_type and not self.record_id:
            self.record_id = str(uuid.uuid4())
        
        record = {}

        # Convert Things to dict
        for k in self.keys:

            if not record.get(k, None):
                record[k] = []

            values = self.get(k)
            
            if not isinstance(values, list):
                values = [values]

            for v in values:
                if issubclass(type(v), Thing):
                    v = v.dump()

                if v not in record[k]:
                    record[k].append(v)
            
        
        # Fix @type and @id
        record['@type'] = self.record_type
        record['@id'] = self.record_id
        
        # Remove lists and empty values
        record = dict_helper.clean(record)
        
        return record

    @property
    def json(self):
        """
        """
        return json.dumps(self.dump())
        
    @json.setter
    def json(self, value):
        """
        """
        record = json.loads(value)
        self.load(record)
        
    
    def normalize_observation(self, observation):
        '''Normalize key and value. If both different, create new observation
        '''

        # Get normalized key value
        normalized_record_type = kraken_schema.normalize_type(self.record_type)
        normalized_key = kraken_schema.normalize_key(observation.key) if not observation.key.startswith('@') else observation.key
        normalized_value = nv.normalize_value(normalized_record_type, observation.key, observation.value)   


        # Update input observation if key or value already normalized
        if normalized_key == observation.key:
            observation.valid_key = True
        if normalized_value == observation.value:
            observation.valid_value = True

        # Address if value is thing
        if issubclass(type(observation.value), Thing):
            observation.valid_value = True

        # Skip if already normalized
        if observation.valid_key and observation.valid_value:
            return None

        # Create new observation
        normalized_observation = observation.get_copy()
        normalized_observation.source_observations_id = observation.observation_id
        normalized_observation.instrument = 'normalize key and value'

        # Assign normalized key
        if normalized_key:
            normalized_observation.key = normalized_key
            normalized_observation.valid_key = True

        # Assign normalized value
        if normalized_value:
            normalized_observation.value = normalized_value
            normalized_observation.valid_value = True

        return normalized_observation

    def normalize_record_id_from_observation(self, observation):
        '''Records nromalized record_id if exist
        '''

        # Add observation with record_id (if new info makes it available)
        record = {
            '@type': self.record_type, 
            observation.key: observation.value
        }
        normalized_record_id = normalize_id.normalize_id(record)

        if normalized_record_id:
            normalized_observation = observation.get_copy()
            
            normalized_observation.source_observations_id = observation.observation_id            
            normalized_observation.instrument = 'normalize record_id'

            normalized_observation.key = '@id'
            normalized_observation.valid_key = True

            normalized_observation.value = normalized_record_id
            normalized_observation.valid_value = True
            
            return normalized_observation

        return None


    
    """Properties
    """
    

    @property
    def record_ref(self):
        record = {
            '@type': self.record_type,
            '@id': self.record_id
        }
        return record

    @record_ref.setter
    def record_ref(self, value):
        self.load(value)

    
    
    @property
    def keys(self, valid = False):
        '''
        '''

        # Get keys
        keys = []
        for i in self._observations.get():
            if i.key not in keys:
                if valid and not i.valid_key:
                    continue
                else: 
                    keys.append(i.key)
                    
        keys = sorted(keys)
        return keys
        
    
    
    @property
    def url_domain(self):
        '''
        '''
        data = self.get_best('schema:url')
        domain = None
        
        if data:
            domain = urlparse(data).netloc
            domain = domain.replace('www.', '')
        
        return domain


    @property
    def metadata(self):
        '''
        '''
        record = {
            '_source_observations_id': self._source_observations_id,
            '_agent': self._agent,
            '_instrument': self._instrument,
            '_credibility': self._credibility,
            '_date': self._date
        }
        return record

    @metadata.setter
    def metadata(self, record):
        '''
        '''
        for k, v in record.items():
            setattr(self, k, v)
        return
    
    '''Methods
    '''
    def update_record_ref(self, old_record_type, old_record_id, new_record_type, new_record_id):
        '''Updates all value with new record_ref
        '''
        for i in self._observations.get():
            if issubclass(type(i.value), Thing):
                if i.original_value.record_type == old_record_type and i.original_value.record_id == old_record_id:
                    i.original_value.record_type = new_record_type
                    i.original_value.record_id = new_record_id
            
        


    
    """Conditions
    """

    @property
    def is_status_active(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:ActiveActionStatus':
            return True
        return False

    @property
    def is_status_completed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:CompletedActionStatus':
            return True
        return False

    @property
    def is_status_failed(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:FailedActionStatus':
            return True
        return False

    @property
    def is_status_potential(self):
        """
        """
        if self.get_best('schema:actionStatus') == 'schema:PotentialActionStatus':
            return True
        return False

    
    """Actions
    """
    def set_status_active(self):
        """
        """
        self.set('schema:actionStatus', 'schema:ActiveActionStatus')
    
    def set_status_completed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:CompletedActionStatus')
    
    def set_status_failed(self):
        """
        """
        self.set('schema:actionStatus', 'schema:FailedActionStatus')
    
    def set_status_potential(self):
        """
        """
        self.set('schema:actionStatus', 'schema:PotentialActionStatus')


    '''System properties
    '''
    @property
    def memory_size(self):
        '''Returns memory size taken by object
        '''
        size = 0
        size += sys.getsizeof(self) / 1024

        for i in self._db:
            size += i.memory_size
        
        return round(size, 2)