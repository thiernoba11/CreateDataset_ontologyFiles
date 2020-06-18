# -*- coding: utf-8 -*-

from urllib.parse import urljoin
import scrapy
import requests
import json


class BioportalSpider(scrapy.Spider):
    name = "bioportal"
    allowed_domains = ['bioportal.bioontology.org']
    start_urls = ['https://bioportal.bioontology.org/ontologies']

    def parse(self, response):
        #  get all scripts on the page and get the 10th script (index 9)
        scriptData = response.xpath("//script").getall()[9]
        # As only the 3rd line in the script (index 2) has all the ontology data we are selecting,
        # then we are splitting it by the variable name and selecting the 2nd element (index 1)
        # and as each JS line ends with ; and we don't want that we are selecting [:-1]
        ontologies = json.loads(scriptData.split("\n")[2].split("jQuery(document).data().bp.fullOntologies = ")[1][:-1])

        # Save all owl files
        owl_items = []
        print(">>>--------------------------------<<<")
        for ontology in ontologies:
            # Ignore files with no  format data attached to the ontology
            if 'format' in ontology:
                # Filter owl format
                if ontology['format'] == "OWL":
                    # Create a data with the required details and add to owl_items
                    owl_data = {
                        "name": ontology["name"],
                        "acronym": ontology["acronym"],
                        "url": "https://bioportal.bioontology.org/ontologies/" + ontology["acronym"]
                    }
                    owl_items.append(owl_data)
        # printing the count of the items
        print("OWL items Found: ", len(owl_items))
        print("<<<-------------------------------->>>")

        # callback to the parseOWL function with the owl_item
        for owl_item in owl_items:
            yield response.follow(url=owl_item["url"], callback=self.parseOWL, meta=owl_item)

    def parseOWL(self, response):
        # The download page has an anchor tag with aria-label "Download latest version",  select that element and get the href attribute
        download_url = response.xpath("//a[@aria-label='Download latest version']/@href").get()
        # print
        print("==>>> Downloading: ", download_url)
        # link_splits = download_url.split('&')
        # if len(link_splits) > 1:
        # print("--> ", link_splits[1])
        # Download it with the file name as equivalent to acronym
        resp = requests.get(download_url, allow_redirects=True)
        # content_type = resp.headers['Content-Type']
        # print(content_type)
        open(response.request.meta["acronym"], "wb").write(resp.content)
