import musicbrainzngs
import json

def set_useragent():
    musicbrainzngs.set_useragent("Sorwave", "1.0", "abrahamescalona@live.com")

def musicbrainzngs_query(file_name):
    query = {'recording': file_name, 'limit': 1, 'fmt': 'json'}
    return query

def musicbrainzngs_json_to_metadata(data):
    metadata = data['recording-list'][0]
    return metadata