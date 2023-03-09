import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json
from main2 import logger

 
def get_headers():
    return Headers(browser="firefox", os="win").generate()


DATA_URL = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
# KEYWORDS = ['Django', 'django', 'Flask', 'flask']
keywords = ["Django","Flask"]

response = requests.get(DATA_URL, headers=get_headers())
response_text = response.text
# print(response_text)

soup = BeautifulSoup(response_text, features='lxml')

vac_list = soup.find('div', class_='vacancy-serp-content')

vacancy = vac_list.find_all(class_='serp-item')

# print(len(vacancy))

pared = []

@logger('log_hh.log')
def foo():
    for vacan in vacancy:
        title = vacan.find('h3')
        company = vacan.find(class_="vacancy-serp-item__meta-info-company")

        company_parsed = company.text
        title_parsed = title.text

        a_tag = title.find('a')
        
        link_absolute = a_tag['href']

        response = requests.get(link_absolute, headers=get_headers())
        hh_serp = BeautifulSoup(response.text, features='lxml')
        hh_serp_tag_branded = hh_serp.find('div', class_='vacancy-branded-user-content')
        hh_serp_tag = hh_serp.find('div', class_='g-user-content')

        if hh_serp_tag_branded == None:
            hh_serp_text = hh_serp_tag.text
        else:
            hh_serp_text = hh_serp_tag_branded.text

        for search in keywords:
            if (search.lower() in title_parsed.lower()) or (search.lower() in hh_serp_text.lower()):
                pared.append({
                    'Title': title_parsed,
                    'Company': company_parsed,
                    'Link': link_absolute
                })   
    return 'data.json update'


if __name__ == '__main__':
    foo()
    with open('data.json', 'w') as outfile:
        json.dump(pared, outfile)
    