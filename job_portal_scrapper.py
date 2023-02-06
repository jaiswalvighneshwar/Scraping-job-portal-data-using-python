# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 13:44:03 2023

@author: Vighneshwar
"""

import requests 
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd

from webdriver_manager.chrome import ChromeDriverManager


url = "https://www.naukri.com/tableau-jobs?k=tableau&ctcFilter=25to50&ctcFilter=50to75"
page = requests.get(url)
page.text

driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(10)

soup = BeautifulSoup(driver.page_source,'html5lib')

driver.close

output_dataframe = pd.DataFrame(columns=['Title','Company','Ratings','Reviews',
                                         'Experience','Salary','Location',
                                         'Job_Post_History','URL'])
results = soup.find(class_ ="list")
job_elements = results.find_all('article',class_ = 'jobTuple')


for job_elem in job_elements:
    #URL for the job
    URL = job_elem.find('a',class_='title ellipsis').get('href')
 
    #Title of the job 
    Title = job_elem.find('a',class_= 'title ellipsis').text
   
    
    #name of the company 
    Company = job_elem.find('a',class_= 'subTitle ellipsis fleft').text
    
    #print(Company)
    
     #Salary offered
    salary_offered_li= job_elem.find('li',class_='fleft br2 placeHolderLi salary')
    salary_offered_span = salary_offered_li.find('span',class_='ellipsis fleft ')
    if salary_offered_span is None:
        continue
    else:
        salary_offered = salary_offered_span.text
    #Rating
    rating_span = job_elem.find('span',class_='starRating fleft dot')
    if rating_span is None:
        Ratings= ""
        
    else:
        Ratings = rating_span.text
    
    #Years of experience required 
    Years_of_exp_span = job_elem.find('span',class_ = 'ellipsis fleft expwdth')
    if Years_of_exp_span is None:
        Years_of_exp = ""
    else:
        Years_of_exp = Years_of_exp_span.text
      
    
    #lcoation 
    location_li= job_elem.find('li',class_='fleft br2 placeHolderLi location')
    location_span = location_li.find('span',class_='ellipsis fleft locWdth')
    if location_span is None:
        location=""
    else:
        location = location_span.text
        
    #no of days since posted
    post_date_span= job_elem.find('span',class_ = 'fleft postedDate')
    if post_date_span is None:
        posted_date = ""
    else:
        posted_date = post_date_span.text
    
    #append to data frame
    output_dataframe = output_dataframe.append({'URL':URL,'Title': Title,'Company':Company,'Ratings':Ratings,'Reviews':"",'Experience':Years_of_exp,'Salary':salary_offered,'Location':location,'Job_Post_History':posted_date}, ignore_index = True)
    print(output_dataframe)