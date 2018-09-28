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

#% Regular expression functions:
def avalia_regex(dataset, regex, nsamples=True, returnList=False):
    '''Função auxiliar para avaliar o resultado de uma dada expressão regular (regex) em um texto (string type). 
    Syntaxe: avalia_regex(dataset, regex, nsamples=True, returnList=False),
        dataset = texto tipo string que será avaliado;
        regex = expressão regular a ser encontrada;
        nsamples = True, mostra todas as amostras encontradas e, em caso contrário, apenas as 3 primeiras, se houver. 
        returnList = false. Se veradeiro, retorna uma lista com as expressões encontradas.
        
    Exemplo de uso: avalia_regex(t03, '\.{2,}\s')'''
    filtro = re.findall(regex, dataset)
    count = len(filtro)
    print('Foram encontrados {} matches para a expressão "{}."'.format(count, regex))
    if nsamples:
        for item in filtro:
            print(item, end=', ')
    else:
        if count > 2:
            print('\te.g.: {}, {}, {}.'.format(filtro[0], filtro[1], filtro[2]))
        elif count > 0:
            print('\te.g.: {}.'.format(filtro[0]))
    if returnList:
        return filtro
    else:
        return


def substitui_regex(dataset, regex, subst):
    '''Função auxiliar para substituir a coincidência de uma dada expressão regular (regex) em um texto (string type). 
    Syntaxe: avalia_regex(dataset, regex, subst), onde dataset é o texto tipo string; regex é a expressão regular a ser encontrada; subst é a string a qual será substituída. A função retorna a nova string.'''
    filtro = re.findall(regex, dataset)
    count = len(filtro)
    print('Foram encontrados {} matches para a expressão "{}."'.format(count, regex))
    newText = re.sub(regex, subst, dataset)
    return newText


#%% Getting acquainted to the dataset
def count_tags(filename):
    tags = {}
    for event, element in ET.iterparse(filename):
        if element.tag not in tags:
            tags[element.tag] = 1
        else: 
            tags[element.tag] += 1
    return tags

tags = count_tags(FILENAME)
pprint.pprint(tags)

#%% Finding the cities in the dataset
def list_cities(filename):
    cities = []
    for _, elem in ET.iterparse(filename):
        if elem.tag == 'tag':
            k = elem.attrib['k']
            v = elem.attrib['v'].lower()  #Lowering the uppercase text
            if k == 'addr:city':
                if v not in cities:
                    cities.append(v)
    print('There are {0} distinct cities in the dataset.'.format(len(cities)))
    return cities

cities = list_cities(FILENAME)

#%% Cleaning the cities names:
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "Crescent", "West", "South", "East", "North", "Vista",
            "Gardens", "Circle", "Gate", "Heights", "Park", "Way", "Mews", "Keep", "Westway", "Glenway",
            "Queensway", "Wood", "Path", "Terrace", "Appleway"]

street_mapping = {"Ave ": "Avenue",
                   "St. ": "Street",
                   "Rd.": "Road",
                   "StreetE": "Street East",
                   "AvenueE": "Avenue East",
                   "W. ": "West",
                   "E. ": "East",
                   "StreetW": "Street West",
                   "StreetW.": "Street West",
                   "StreetE.": "Street East",
                   "Robertoway": "Roberto Way"
                   }

#%% TESTE!!
## There are similar cities, the problem is that they are capitalized or with accentuation.
## In order to solve it, I will use regEx to normalize the expressions:

# i. Tornando o texto lower_case:
text_i = raw.lower()
# iv. Remove as demais pontuações e caracteres de controle:
text_iv = substitui_regex(text_iii, '[\t\n\b\r()\'"%&*]+?', ' ')  #Espaçamento duplicado será removido abaixo


#%% Auditing and cleaning the cities names:
sete_Povos = ['São Miguel das Missões',
              'Santo Ângelo',
              'São Borja',
              'São Nicolau',
              'São Luiz Gonzaga',
              'São Lourenço',
              'Entre-Ijuís']

def audit_cities():
    

#%%
            
            if k.startswith('addr:'):
                addr = k.split(':')
                
                
            if elem.attrib['k'] == 'addr:city':
                try: # Try to convert the elevation to an integer
                    elevation = int(elem.attrib['v'])
                    if elevation > 320 or elevation < 124: # Elevation limits in meters identified from the USGS
                        suspect_elevations.append(elevation)
                except: #
                    invalid_elevations.append(elem.attrib['v'])
                    
                    
    ...
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
                        if is_postal_code(k):
                            v = audit_postal_code(v)
                        node['address'][address[1]] = v
                else:
                    node[k] = v
                    
    

#%% Discovering how many cities are in the selected region
def count_cities(filename):
    """
    Parse, validate and format node and way xml elements.
    Return list of dictionaries
    Keyword arguments:
    element -- element object from xml element tree iterparse
    """
    cities = {}
    tempCount = 0
    for event, element in ET.iterparse(filename):
        tempCount += 1
        if tempCount == 1000:
            return
        if element.tag == 'way' and element.attrib == '
    
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





#%% verificar o uso desta seção... Tag Types (Quiz)
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')


def key_type(element, keys):
    if element.tag == "tag":
        # YOUR CODE HERE
        if lower.search(element.attrib['k']):
            keys['lower'] += 1
        elif lower_colon.search(element.attrib['k']):
            keys['lower_colon'] += 1
        elif problemchars.search(element.attrib['k']):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
        
    return keys



def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys



def test():
    # You can use another testfile 'map.osm' to look at your solution
    # Note that the assertion below will be incorrect then.
    # Note as well that the test function here is only used in the Test Run;
    # when you submit, your code will be checked against a different dataset.
    keys = process_map('example.osm')
    pprint.pprint(keys)
    assert keys == {'lower': 5, 'lower_colon': 0, 'other': 1, 'problemchars': 1}


if __name__ == "__main__":
    test()



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

#%% Alternativa:
def printPostcodes():
    for event, elem in ET.iterparse(OSMFILE, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                
                if 'k' in tag.attrib and tag.attrib['k'] == 'addr:postcode' and tag.attrib['v'] != None:
                    print(tag.attrib['v'].encode("utf-8"))
        elem.clear() # discard the element

if __name__ == '__main__':
    printPostcodes()

#%%
test()    
    
    
    
    
    
    
    
    




