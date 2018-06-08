# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:00:16 2016
Print all song links for index alphabet
@author: Adwait
"""

import scrapy
from urlparse import urljoin

class QuotesSpider(scrapy.Spider):
    name = "allsongs"
    allowed_domains = ["aathavanitli-gani.com"]
    custom_settings = {
        "DOWNLOAD_DELAY": 3,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 4
    }

    def start_requests(self):
        with open('index-links.txt') as f:
            urls = f.read().splitlines() 

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            print 'done listing songs under url: %s' % url

    def parse(self, response):
        filename = 'song_list.txt'
        #url_list = response.xpath('//a[contains(@href, "Song")]/@href').extract()
        url_list = response.xpath("//div[@class='marathiName']/a/@href").extract()
        with open(filename, 'a') as f:
            for alpha_url in url_list:    
                f.write(urljoin('http://www.aathavanitli-gani.com/a/b',alpha_url) +'\n')
        self.log('Saved file %s' % filename)
