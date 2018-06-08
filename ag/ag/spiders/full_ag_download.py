# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 15:56:54 2016

@author: Adwait
"""

import scrapy
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "fulld"
    allowed_domains = ["aathavanitli-gani.com"]
    custom_settings = {
        "DOWNLOAD_DELAY": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 6
    }

    def start_requests(self):
        with open('C:\\Users\\Adwait\\ag\\song_list.txt') as f:
            urls = f.read().splitlines() 

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
            print 'done listing songs under url: %s' % url

    def parse(self, response):
        page = response.url.split("/")[-1].replace(',','')
        filename = 'songsdb//%s.txt' % page
        with open(filename, 'wb') as f:
            song_text = response.css('div.songText')[1].extract().encode('utf-8','ignore')
            soup = BeautifulSoup(song_text,"lxml")
            f.write(soup.get_text().encode('utf-8','ignore'))
        self.log('Saved file %s' % filename)