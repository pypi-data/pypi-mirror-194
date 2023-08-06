


def to_list(record):
    '''Takes a dict and converts all values to list of values
    '''

    # Deal with list
    if isinstance(record, list):
        new_records = []
        for i in record:
            new_records.append(dict_to_list(i))
        return new_records

    # Convert 
    new_record = {}

    for k, v in record.items():
        if not isinstance(v, list):
            v = [v]
        new_record[k] = v
    return new_record


def clean(record):
    '''Remove empty values and lists of 1 in dict
    '''
    
    # Deal with list
    if isinstance(record, list):
        new_records = []
        for i in record:
            new_records.append(dict_clean(i))
        return new_records

    # Clean
    new_record = {}
    for k, v in record.items():
        if not v:
            continue
        if isinstance(v, list) and len(v) == 0:
            continue
        if isinstance(v, list) and len(v) == 1:
            v = v[0]
        new_record[k] = v
    
    return new_record