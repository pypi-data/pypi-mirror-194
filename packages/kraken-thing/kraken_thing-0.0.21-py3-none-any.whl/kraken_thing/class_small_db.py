

class Small_db:


    def __init__(self, no_params=1):

        self.db = {}
        self.no_params = no_params


    def __len__(self):
        '''
        '''
        records = self.get()
        return len(records)


    def __iter__(self):
        '''
        '''
        for i in self.get():
            yield i

    def post(self, value, param1=None, param2=None):
        '''
        '''
        return self.set(value, param1, param2)

    
    def set(self, value, param1=None, param2=None):
        '''
        '''
        if param1 and not param2:
            self.db[param1] = value
        
        elif param1 and param2:
            if not self.db.get(param1, None):
                self.db[param1] = {}
                
            self.db[param1][param2] = value

        
        
    def get(self, param1 = None, param2 = None, default = None):
        '''
        '''


        if self.no_params == 1:

            if param1:
                return self.db.get(param1, default)
            
            else:
                records = []
                for i in self.db.values():
                    records.append(i)
                return records
        
        
        elif self.no_params == 2:
            
            
            if not param1 and not param2:
                records = []
                for p1 in self.db.values():
                    for i in p1.values():
                        records.append(i)
                return records
            
            
            elif param1 and not param2:
                records = []
                for i in self.db.get(param1, default).values():
                    records.append(i)
                return records

             
        
            elif param1 and param2:
                return self.db.get(param1, {}).get(param2, default)
        
        

    
    def delete(self, param1 = None, param2 = None):
        '''
        '''
        if not param1 and param2:
            return

        elif not param2:
            self.db[param1] = None

        else:
            self.db[param1].pop(param2, None)


    
    @property
    def param1(self):
        '''returns the values in param1
        '''

        return self.db.keys()

    @property
    def param2(self, param1):
        '''returns the values in param1
        '''

        return self.db.get(param1, {}).keys()