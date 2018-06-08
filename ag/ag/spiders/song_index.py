# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 14:21:39 2016

Print all the links from page
http://www.aathavanitli-gani.com/Anukramanika

@author: Adwait
"""

import scrapy

class QuotesSpider(scrapy.Spider):
    name = "index"

    def start_requests(self):
        urls = [
            'http://www.aathavanitli-gani.com/Anukramanika'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = 'index-links.txt'
        url_list = response.xpath('//div[@id="alpha"]/a/@href').extract()
        with open(filename, 'wb') as f:
            for alpha_url in url_list:
                f.write('http://www.aathavanitli-gani.com/'+alpha_url+'\n')
        self.log('Saved file %s' % filename)
