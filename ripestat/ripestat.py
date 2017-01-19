import requests
from itertools import chain
from collections import Counter

#Returns the announced prefixes as seen by RIS collectors
def announced_prefixes(as_number):
    url = 'https://stat.ripe.net/data/announced-prefixes/data.json?resource={AS}'.format(AS=as_number)
    r = requests.get(url)
    return [prefix_data['prefix'] for prefix_data in r.json()['data']['prefixes']]

#Returns the neighbouring AS numbers as seen by RIS collectors
def asn_neighbours(as_number):
    url = 'https://stat.ripe.net/data/asn-neighbours/data.json?resource={AS}'.format(AS=as_number)
    r = requests.get(url)
    return [nei_data['asn'] for nei_data in r.json()['data']['neighbours']]

#Returns the count for each ASN before reaching originating AS number.
def prefix_upstream_asn_balance(prefix):
    url = 'https://stat.ripe.net/data/looking-glass/data.json?resource={PREFIX}'.format(PREFIX=prefix)
    r = requests.get(url)
    
    #global as_path_list
    #as_path_list = []
    looking_glass = r.json()
    #recurse_to_as_path(incoming_asn_balance)
    as_path_list = item_generator(looking_glass, 'as_path')
    return Counter([asn.split()[-2] for asn in as_path_list if len(asn.split()) >= 2])

#Get the values of target_key from a JSON structure
def item_generator(json_input, target_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == target_key:
                yield v
            else:
                for child_val in item_generator(v, target_key):
                    yield child_val
    elif isinstance(json_input, list):
        for item in json_input:
            for item_val in item_generator(item, target_key):
                yield item_val
