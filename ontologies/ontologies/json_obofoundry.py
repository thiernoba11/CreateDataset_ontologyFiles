#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests

obo_json = requests.get("http://www.obofoundry.org/registry/ontologies.jsonld", allow_redirects=True)
open('obofoundry.json', 'wb').write(obo_json.content)

with open('obofoundry.json') as json_file:
    json_data = json.load(json_file)
   
ontologies = json_data['ontologies']

ontology_with_owl = []


for ontology in ontologies:
    owl_data = {}
    if ontology['activity_status'] == 'active':
        title = ontology['title']
        products = ontology['products']
        owls = [product for product in products if product['id'].endswith('.owl')]
       
        if len(owls) < 1:
            continue
        owl_url = owls[0]['ontology_purl']
       
        owl_data['title'] = title
        owl_data['owl_url'] = owl_url
       
        ontology_with_owl.append(owl_data)

       
for ontology in ontology_with_owl:
    # Downloading
    print("==>>> Downloading: ", ontology['title'])
    file_name = "_".join(ontology['title'].split(" "))
   
    resp = requests.get(ontology['owl_url'], allow_redirects=True)
    open(file_name, 'wb').write(resp.content)

