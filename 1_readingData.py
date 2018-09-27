#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 27 02:36:48 2018

@author: tbnsilveira
"""

#%%  Initial statements 

import xml.etree.cElementTree as ET
import pprint
import re

# Dataset file name:
FILENAME = 'Missoes.osm'


#%% GET ACQUAINTED TO THE DATASET
def count_tags(filename):
    tags = {}
    for _, elem in ET.iterparse(filename):
        tag = elem.tag
        if tag not in tags.keys():
            tags[tag] = 1
        else:
            tags[tag] += 1
    return tags

tags = count_tags(FILENAME)
pprint.pprint(tags)


#%% VALIDATING 'k' ATTRIBUTE
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        # search returns matchObject which is always true or None when 'false'
        if lower.search(element.attrib['k']):
            keys["lower"] += 1
        elif lower_colon.search(element.attrib['k']):
            keys["lower_colon"] += 1
        elif problemchars.search(element.attrib['k']):
            keys["problemchars"] += 1
        else:
            keys["other"] += 1
    return keys


def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys


def test():
    keys = process_map(FILENAME)
    pprint.pprint(keys)

# test()

#%% POSTAL CODE VALIDATION
postal_codes = re.compile(r'^[ABCEGHJKLMNPRSTVXY][0-9][ABCEGHJKLMNPRSTVWXYZ][\s]?[0-9][ABCEGHJKLMNPRSTVWXYZ][0-9]')

def audit_postal_code(postal_code):
    postal_code = postal_code.upper()
    if postal_codes.match(postal_code):
        return postal_code

    bad_postal_codes.append(postal_code)
    return postal_code


def is_postal_code(address_key):
    return address_key == 'addr:postcode'



#%%
test()    
    
    
    
    
    
    
    
    




