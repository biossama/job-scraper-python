from bs4 import BeautifulSoup
import requests
import csv
from itertools import zip_longest
import re


url = 'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start=0'
HEADERS = {"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
response = requests.get(url, headers=HEADERS)
response = response.text

print("this script run over all pages of website and scrapt the tagred information")

with open("./jobs_scraping.csv", "w") as f1:
                  file = csv.writer(f1)
                  file.writerow(["job title","compaany name","local job", "jobs experience", "link", "date offer"])
count = 0
while True:
        url = f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={count}'
        response = requests.get(url, headers=HEADERS)
        response = response.text
        soup = BeautifulSoup(response, 'html')
        jobs_title = soup.find_all("h2", class_ = "css-m604qf")
        name_companys = soup.find_all("a", class_ = "css-17s97q8")
        jobs_local = soup.find_all("span", class_ = "css-5wys0k")
        jobs_experience = soup.find_all("div", class_ ="css-y4udm8")
        date_offer = soup.find_all("div", class_ = "css-d7j1kk")
        print(len(jobs_title), f'https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={count}')
        count+=1
        for i in range(len(jobs_title)):
            if len(jobs_experience) == len(name_companys) == len(jobs_title) == len(jobs_local) == len(date_offer):
                # remove unwanted text using regrex
                pattern = re.compile(r'\..*?}')
                title_jobs = pattern.sub('',jobs_title[i].text )
                experience_jobs = pattern.sub('', jobs_experience[i].text )
                offer_date = ' '.join(date_offer[i].text.split(",")[-1].split()[-3:-1])
                link_info = jobs_title[i].find("a").attrs['href']
                name_company = name_companys[i].text.strip(' -')
                link_job = jobs_title[i].find("a").attrs['href']
                job_local = jobs_local[i].text
                src = requests.get(jobs_title[i].find("a").attrs['href']) 
                with open("./jobs_scraping.csv", "a") as f2:
                    file=csv.writer(f2)
                    file.writerow([title_jobs, name_company, job_local, experience_jobs, link_job, offer_date])
        if len(jobs_title) != 15:
            with open("./jobs_scraping.csv", "a") as f2:
                file=csv.writer(f2)
                file.writerow([title_jobs, name_company, job_local, experience_jobs, link_job, offer_date])
            break
