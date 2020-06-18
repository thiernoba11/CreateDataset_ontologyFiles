# -*- coding: utf-8 -*-
import scrapy
import logging
import requests


class ObofoundrySpider(scrapy.Spider):
    name = 'obofoundry'

    start_urls = ["http://www.obofoundry.org"]

    def parse(self, response):
        obofoundry = response.xpath("//td/a")
        owlfiles = [owlfile for owlfile in obofoundry if owlfile.xpath(".//@href").get().endswith(".owl")]
        for owlfile in owlfiles:
            url = owlfile.xpath(".//@href").get()
            name = url.split('/')[-1].split('.')[0]
            print("==>>>  Downloading: ", name)
            # Get the data from owl url
            resp = requests.get(url, allow_redirects=True)
            # This saves the data onto the file with the name
            open(name, 'wb').write(resp.content)

            yield {'file_name': name, 'download_url': url}
