from .class_small_db import Small_db 

from .kraken_class_observation import Observation



class Observations:

    def __init__(self):

        self._db = Small_db(1)
        self.param1 = 'obs'


    def new(self, key=None, value=None, metadata = None):
        '''
        '''
        o = Observation(key, value)
        o.metadata = metadata
        self.set(o)
        return o
    
    def get(self, observation_id = None):
        '''
        '''

        obs = self._db.get(observation_id)            

        if not isinstance(obs, list):
            return obs

        # Sort by importance
        obs = sorted(obs, reverse=True)

        # Sort by key
        obs = sorted(obs, key=lambda x: x.key)
        
        return obs
    

    def get_by_key(self, key = None, include_non_valid=True):
        '''
        '''
        obs = []
        for i in self.get():
            if i.key == key and (include_non_valid == True or (i.valid_key and i.valid_value)):
                obs.append(i)
        return obs



    def get_best(self, key = None, include_non_valid=True):
        '''
        '''
        obs = self.get_by_key(key, include_non_valid)

        if not obs:
            return None
        if not isinstance(obs, list):
            return obs
        if len(obs) == 0:
            return None
        
        return obs[0]

    
    def set(self, observation):
        '''
        '''

        if isinstance(observation, list):
            for i in observation:
                self.set(i)
            return

        
        self._db.set(observation, observation.observation_id)

        # Add parents and childs
        if observation.source_observations_id:
            for i in observation.source_observations_id:
                
                source_obs = self.get(i)
                
                if not source_obs:
                    continue
    
                if source_obs not in observation.source_observations:
                    observation.source_observations.append(source_obs)
                
                if observation not in source_obs.child_observations:
                    source_obs.child_observations.append(observation)

        
    def load(self, records):
        '''
        '''

        if not isinstance(records, list):
            records = [records]
            
        for i in records:
            o = Observation()
            o.load(i)
            self.set(o)

    def dump(self):
        '''
        '''
        records = []
        for o in self.get():
            records.append(o.dump())

        return records
        
            
            