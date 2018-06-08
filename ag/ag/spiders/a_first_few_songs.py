# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 12:45:52 2016

@author: Adwait
"""

import scrapy
from bs4 import BeautifulSoup

class QuotesSpider(scrapy.Spider):
    name = "songs"

    def start_requests(self):
        urls = [
            'http://www.aathavanitli-gani.com/Song/A_Aa_Aai,_Ma_Ma_Maka',
            'http://www.aathavanitli-gani.com/Song/Akrura_Neu_Nako_Madhava',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-1].replace(',','')
        filename = 'songsdb//song-%s.txt' % page
        with open(filename, 'wb') as f:
            song_text = response.css('div.songText')[1].extract().encode('utf-8','ignore')
            soup = BeautifulSoup(song_text,"lxml")
            f.write(soup.get_text().encode('utf-8','ignore'))
        self.log('Saved file %s' % filename)