
import kraken_schema_org

def get(key, default=None):
    '''
    '''    
    # Put in lowercase
    key = key.lower()

    db = get_db()
    
    new_key_map = db.get(key, default)


    new_key_norm = kraken_schema_org.normalize_key(new_key_map)
    return new_key_norm if new_key_norm else new_key_map 

    
        


def get_db():

    
    db = {

        'record_type': '@type',
        'record_id': '@id',

        #action
        'status': 'schema:actionStatus',

        # Person
        'firstname': 'schema:givenName',
        'lastname': 'schema:familyName',

        # Address
        'street': 'schema:streetAddress',
        'city': 'schema:addressLocality',
        'province': 'schema:addressRegion',
        'state': 'schema:addressRegion',
        'country': 'schema:addressCountry',
        'zipcode': 'schema:postalCode'
    }
    return db