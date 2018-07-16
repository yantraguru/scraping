# -*- coding: utf-8 -*-
"""
Created on Thu Sep 28 22:02:35 2017

@author: Adwait
"""

import os
import time
import csv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

def find_by_xpath(driver,locator):
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, locator))
    )
    return element
    
def get_downloaed_file_list():    
    tracker_file_path = 'D:\\store\\download_log.csv'
    with open(tracker_file_path, 'r') as tracker_file:
        downloaded_list = [line.strip() for line in tracker_file]
        
    return downloaded_list
    
def is_downloded(downloaded_list,company_name):
    if company_name in downloaded_list:
        return True
    else:
        return False
        
def is_file_present(company_code):
    data_file_path_1 = "C:\\Users\\Adwait\\Downloads\\{}.csv".format(company_code)
    data_file_path = "D:\\store\\{}.csv".format(company_code)
    if os.path.exists(data_file_path) or os.path.exists(data_file_path_1):
        return True
    else:
        return False
        
def get_driver():        
    driver = webdriver.Chrome()
    driver.get("http://www.bseindia.com/markets/equity/EQReports/StockPrcHistori.aspx?scripcode=512289&flag=sp&Submit=G")
    return driver
    
def download_price_history(driver,company_name):
    
    type_element = find_by_xpath(driver,'//*[@id="ctl00_ContentPlaceHolder1_rad_no2"]')
    type_element.click()
    
    scrip_code_element = find_by_xpath(driver,'//*[@id="ctl00_ContentPlaceHolder1_GetQuote1_smartSearch2"]')
    scrip_code_element.clear()
    for char_count,char in enumerate(company_name.upper()):
        scrip_code_element.send_keys(char)
        if char_count % 4 == 0:
            time.sleep(0.5)
        if char_count > 6:
            break
        
    try:
        #auto_suggest_menu = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listEQ"]')))
        auto_suggest_menu = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="listMF"]')))
        #time.sleep(1)
    except TimeoutException:
        print "Loading took too much time!"        
        return
    
    scrip_code_element.send_keys(Keys.ENTER)
    
    frmDt_element = find_by_xpath(driver,'//*[@id="ctl00_ContentPlaceHolder1_txtFromDate"]')
    if frmDt_element.get_attribute('value') != '01/01/1980':
        frmDt_element.clear()
        frmDt_element.send_keys('01/01/1980')
        
    find_by_xpath(driver,'//*[@id="ctl00_ContentPlaceHolder1_btnSubmit"]').click()
    
    try:
        csv_download_btn = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_btnDownload"]')))
    except TimeoutException:
        print "Loading took too much time!"
    
    csv_download_btn.click() 

def update_download_tracker(company_name):
    tracker_file_path = 'D:\\store\\download_log.csv'
    if os.path.exists(tracker_file_path):
        with open(tracker_file_path, "a") as tracker_file:
            tracker_file.write("{}\n".format(company_name))
    else:
        with open(tracker_file_path, "w") as tracker_file:
            tracker_file.write("{}\n".format(company_name))
    
#download
driver = get_driver()
downloaded_list = get_downloaed_file_list()
    
scrips_list = csv.reader(open('D:\\store\\ListOfScrips.csv'))
fields = scrips_list.next()
for row in scrips_list:
    company_code = row[0]
    company_name = row[1]
    
    if not is_downloded(downloaded_list,company_name) and not is_file_present(company_code):
            start = time.time()
            download_price_history(driver,company_name)
            stop = time.time()
            update_download_tracker(company_name)
            #print '%s company data is downloaded! in %4f sec.' % (company_name,(stop-start))
    #else:
        #print '%s company data is already downloaded!' % company_name

driver.close()
 
#remaining download
driver = get_driver()
downloaded_list = get_downloaed_file_list()
    
scrips_list = csv.reader(open('D:\\store\\remaning_download.csv'))
for row in scrips_list:
    company_name = row[0]
    if not is_downloded(downloaded_list,company_name) and not is_file_present(company_code):
        start = time.time()
        download_price_history(driver,company_name)
        stop = time.time()
driver.close()
  
#test
company_name = 'ABB'
download_price_history(company_name)

#check files not downloaded
scrips_list = csv.reader(open('D:\\store\\ListOfScrips.csv'))
fields = scrips_list.next()
for row in scrips_list:
    company_code = row[0]
    company_name = row[1]
    if is_file_present(company_code):
        update_download_tracker(company_name)        
        
#print files not dowloaded
scrips_list = csv.reader(open('D:\\store\\ListOfScrips.csv'))
remaining_path = 'D:\\store\\remaning_download.csv'

remaining_file_list = []    
fields = scrips_list.next()
for row in scrips_list:
    company_code = row[0]
    company_name = row[1]
    if not is_file_present(company_code):
        remaining_file_list.append(company_name)

if os.path.exists(remaining_path):
    mode = 'a'
else:
    mode = 'w'

with open(remaining_path, mode) as remaining_file:        
    for company in remaining_file_list:
        remaining_file.write("{}\n".format(company))

remaining_file.close()        
            
#cleanup files            
import glob

file_list = glob.glob("C:\\Users\\Adwait\\Downloads\\*.csv")
for filename in file_list:
    if '(' in filename and ')' in filename:
        os.remove(filename)

'''        
scrips_list = csv.reader(open('D:\\store\\ListOfScrips.csv'))
updated_log_path = 'D:\\store\\update_log.csv'
fields = scrips_list.next()


if os.path.exists(updated_log_path):
    mode = 'a'
else:
    mode = 'w'

with open(updated_log_path, mode) as updated_log_file:        
    for row in scrips_list:
        company_code = row[0]
        company_name = row[1]

        remaining_file.write("{}\n".format(company))

remaining_file.close()  

'''      

        