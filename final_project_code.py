#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on Thu Sep 27 02:36:48 2018
@author: tbnsilveira

Based on: https://github.com/jasonicarter/udacity/blob/master/P3_OpenStreeMap_Data_MongoDB/src/final_project_code.py
"""

#%% Some basic statements
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json

# Dataset file name:
FILENAME = 'Missoes.osm'

#%%## Cleaning, shaping and exporting data
"""After auditing and deciding which data must be cleaned, now it's time to shape the data into the model that will be exported to a MongoDB collection.  

The output should be a list of dictionaries that look like this:
>*{  
"id": "2406124091",  
"type: "node",  
"visible":"true",  
"created": {  
          "version":"2",  
          "changeset":"17206049",  
          "timestamp":"2013-08-03T16:43:42Z",  
          "user":"linuxUser16",  
          "uid":"1219059"  
        },  
"pos": [41.9757030, -87.6921867],  
"address": {  
          "housenumber": "5157",  
          "postcode": "60625",  
          "street": "North Lincoln Ave"  
        },  
"amenity": "restaurant",  
"cuisine": "mexican",  
"name": "La Cabana De Don Luis",  
"phone": "1 (773)-271-5176"  
}*"""

"""
The following are instructions from the code given by Udacity team for this project:  

*You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB.
Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to
update the street names before you save them to JSON.
In particular the following things should be done:*  

- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings.
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:
>< tag k="addr:housenumber" v="5158"/>  
>< tag k="addr:street" v="North Lincoln Avenue"/>  
>< tag k="addr:street:name" v="Lincoln"/>  
>< tag k="addr:street:prefix" v="North"/>  
>< tag k="addr:street:type" v="Avenue"/>  
>< tag k="amenity" v="pharmacy"/>  

Should be turned into:
>{...  
>"address": {  
>    "housenumber": 5158,  
>    "street": "North Lincoln Avenue"  
>}  
>"amenity": "pharmacy",  
>...  
>}  

- for "way" specifically:
>  <nd ref="305896090"/>
>  <nd ref="1719825889"/>

should be turned into
> "node_refs": ["305896090", "1719825889"]*
"""
        
        
#%% Defining the cleaning parameters
## General attributes:
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
ATTRIB = ["id", "visible", "amenity", "cuisine", "name", "phone"]

## Street names
### IMPORTANT: Brazilian street types are in the beginning of the phrase:
street_type_re = re.compile(r'^\b\S+\.?', re.IGNORECASE)

expected = ["Rua", "Avenida", "Praça", "Via", "Estrada", "Travessa", "Linha", "Alameda", "Largo", "Parque", "Rodovia"]

street_mapping = {'Av.': 'Avenida',
           'BR ': 'BR-',
           'BR158': 'BR-158',
           'ERS-': 'RS-',
           'RS ': 'RS-'
          }

## Cities names
expected_cities = ['santa rosa', 'condor', 'ijuí', 'panambi', 'santo ângelo', 'três de maio',
            'santo cristo', 'eugênio de castro', 'santo augusto', 'cruz alta', 'vila sírio', 
            'cerro largo', 'são josé do mauá', 'são miguel das missões', 'horizontina']

mapping_cities = {'ijui': 'ijuí',
                  'santo angelo': 'santo ângelo',
                  'panambi - rs': 'panambi'
                 }

## Postcodes:
cep = re.compile(r"[0-9]{5}-[0-9]{3}") #Alternative: cep = re.compile('d{5}-d{3}')
mapping_cep = {'98910000': '98910-000'}


fixed_street_names = []
fixed_city_names = []
fixed_cep = []
bad_postal_codes = []

#%% Fixing street names
def audit_street_type(street_name):
    """Return the fixed street name or return untouched street name if expected."""
    match = street_type_re.search(street_name)
    if match:
        street_type = match.group()
        if street_type not in expected:
            return update_street_name(street_name, street_mapping)
    # TODO: rather None/null or a bad street name?
    return street_name


def update_street_name(name, mapping):
    """Replace and return new name from street name mapping."""
    for key in mapping.keys():
        if re.search(key, name):
            name = re.sub(key, mapping[key], name)
            fixed_street_names.append(name)
    return name


def is_street_name(address_key):
    return address_key == 'addr:street'

#%% Fixing cities names
def audit_city_name(city_name):
    """Return matched postal code and add bad ones to list."""
    if city_name in expected_cities:
        return city_name
    else:
        return update_city(city_name, mapping_cities)
        
def update_city(city_name, mapping_cities):
    """Replace and return new name from street name mapping."""
    for key in mapping_cities.keys():
        if re.search(key, city_name):
            city_name = re.sub(key, mapping_cities[key], city_name)
            fixed_city_names.append(city_name)
    return city_name

def is_city_name(city_name):
    return city_name == 'addr:city'

#%% Fixing postal codes
def audit_postal_code(postal_code):
    """Return matched postal code and add bad ones to list."""
    if cep.match(postal_code):
        return postal_code
    else:
        bad_postal_codes.append(postal_code)
        return update_cep(postal_code, mapping_cep)

#def is_cep(elem):
#    return (elem.attrib['k'] == "addr:postcode")
        
def update_cep(cep, mapping):
    """Replace and return new name from street name mapping."""
    for key in mapping.keys():
        if re.search(key, cep):
            cep = re.sub(key, mapping[key], cep)
            fixed_cep.append(cep)
    return cep


def is_postal_code(address_key):
    return address_key == 'addr:postcode'

#%% Shaping the data
def shape_element(element):
    """
    Parse, validate and format node and way xml elements.
    Return list of dictionaries

    Keyword arguments:
    element -- element object from xml element tree iterparse
    """
    if element.tag == 'node' or element.tag == 'way':

        # Add empty tags - created (dictionary) and type (key/value )
        node = {'created': {}, 'type': element.tag}

        # Update pos array with lat and lon
        if 'lat' in element.attrib and 'lon' in element.attrib:
            node['pos'] = [float(element.attrib['lat']), float(element.attrib['lon'])]

        # Deal with node and way attributes
        for k in element.attrib:

            if k == 'lat' or k == 'lon':
                continue
            if k in CREATED:
                node['created'][k] = element.attrib[k]
            else:
                # Add everything else directly as key/value items of node and way
                node[k] = element.attrib[k]

        # Deal with second level tag items
        for tag in element.iter('tag'):
            k = tag.attrib['k']
            v = tag.attrib['v']

            # Search for problem characters in 'k' and ignore them
            if problemchars.search(k):
                # Add to array to print out later
                continue
            elif k.startswith('addr:'):
                address = k.split(':')
                if len(address) == 2:
                    if 'address' not in node:
                        node['address'] = {}
                    if is_street_name(k):
                        v = audit_street_type(v)
                    if is_city_name(k):
                        v = audit_city_name(v)
                    if is_postal_code(k):
                        v = audit_postal_code(v)
                    node['address'][address[1]] = v
            else:
                node[k] = v

        # Add nd ref as key/value pair from way
        node_refs = []
        for nd in element.iter('nd'):
            node_refs.append(nd.attrib['ref'])

        # Only add node_refs array to node if exists
        if len(node_refs) > 0:
            node['node_refs'] = node_refs

        return node
    else:
        return None


def process_map(file_in, pretty=False):
    # You do not need to change this file
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")

        # Keep track of things
        print('Fixed street names:', fixed_street_names)
        print('Bad postal code:', bad_postal_codes)

    return data

#%% Testing
def test():
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('Missoes.osm', False)
    # pprint.pprint(data)

#%% Running
if __name__ == "__main__":
    test()
