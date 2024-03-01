from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions

import requests
from bs4 import BeautifulSoup
import regex as re
import pandas as pd

# ========================================================================

# 1. https://www.mauritius-villa.com/
with open("Mauritius Villas.html", "r", encoding="utf8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

# url = "https://www.mauritius-villa.com/en/find"
# req = requests.get(url)
# soup = BeautifulSoup(req.text, "lxml")

villa_name_list = []
full_address_list = []
n_bedrooms_list = []
# n_bathrooms_list = []
# pool_list = []
# other_facilities_list = []
price_list = []

villa_name_tag_all = soup.find_all("h2", {"property": "name"})
for villa_name_tag in villa_name_tag_all:
    villa_name = villa_name_tag.text
    villa_name_list.append(villa_name)
full_address_tag_all = soup.find_all("a", {"class": "location"})
for full_address_tag in full_address_tag_all:
    full_address = full_address_tag.text.strip()
    full_address_list.append(full_address)
n_bedrooms_tag_all = soup.find_all("div", class_="details")
for n_bedrooms_tag in n_bedrooms_tag_all:
    n_bedrooms = n_bedrooms_tag.find_all("span")[1].text.strip()
    n_bedrooms_number = int(re.findall(r"\d+", n_bedrooms)[0])
    n_bedrooms_list.append(n_bedrooms_number)
price_tag_all = soup.find_all("span", class_="dataPrice")
for price_tag in price_tag_all:
    price = int(price_tag["content"])
    price_list.append(price)

mauritius_villa_df = pd.DataFrame({"Name": villa_name_list,
                                   "Address": full_address_list,
                                   "N Bedrooms": n_bedrooms_list,
                                   "Price (idr)": price_list})
mauritius_villa_df.to_csv("mauritius_villa.csv")

# ========================================================================

# 2. https://www.villanovo.com/
with open("Villanovo.html", "r", encoding="utf8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

villa_name_list = []
full_address_list = []
n_bedrooms_list = []
n_bathrooms_list = []
# pool_list = []
# other_facilities_list = []
price_list = []

villa_name_tag_all = soup.find_all("h3", {"class": "title-lg title-listing"})
for villa_name_tag in villa_name_tag_all:
    villa_name = villa_name_tag.text.strip()
    villa_name_list.append(villa_name)
full_attribute_tag_all = soup.find_all("div", {"class": "villa-left"})
for full_attribute in full_attribute_tag_all:
    full_address = full_attribute.find_all("span")[-1].text.strip()
    full_address_list.append(full_address)

    bed_bath_tag = full_attribute.find_all("span", class_="margin-right-20")
    n_bedroom = int(bed_bath_tag[1].text.strip())
    n_bedrooms_list.append(n_bedroom)
    n_bathrooms = int(bed_bath_tag[2].text.strip())
    n_bathrooms_list.append(n_bathrooms)
price_tag_all = soup.find_all(["span", "div"], class_=re.compile(r"villa-price color-red.*"))
for price_tag in price_tag_all:
    price = price_tag.text.strip()
    price_list.append(price)

villanovo_df = pd.DataFrame({"Name": villa_name_list,
                             "Address": full_address_list,
                             "N Bedrooms": n_bedrooms_list,
                             "N Bathrooms": n_bathrooms_list,
                             "Price (eur)": price_list})
villanovo_df.to_csv("villanovo.csv")

# ========================================================================

# 3. https://smart-villas-mauritius.com/
with open("Smart Villas Mauritius.html", "r", encoding="utf8") as f:
    html = f.read()
soup = BeautifulSoup(html, "html.parser")

villa_name_list = []
# full_address_list = []
n_bedrooms_list = []
n_bathrooms_list = []
# pool_list = []
# other_facilities_list = []
price_list = []

villa_name_tag_all = soup.find_all("span", {"class": "ng-binding", "ng-bind-html": "villa.title"})
for villa_name_tag in villa_name_tag_all:
    villa_name = villa_name_tag.text
    villa_name_list.append(villa_name)
n_bedrooms_tag_all = soup.find_all("p", {"class": "bedroom_detail h5"})
for n_bedrooms_tag in n_bedrooms_tag_all:
    n_bedrooms = int(n_bedrooms_tag.text.strip())
    n_bedrooms_list.append(n_bedrooms)
n_bathrooms_tag_all = soup.find_all("p", {"class": "bathroom_detail h5"})
for n_bathrooms_tag in n_bathrooms_tag_all:
    n_bathrooms = int(n_bathrooms_tag.text.strip())
    n_bathrooms_list.append(n_bathrooms)
price_tag_all = soup.find_all("p", {"class": "blue_price vill_price ng-binding"})
for price_tag in price_tag_all:
    if not(re.search(r"\d+", price_tag.text)):
        price = None
    else:
        price = re.findall(r"\d+.\d+", price_tag.text)
        if len(price) > 1:
            price = price[0] + "-" + price[1]
        else:
            price = price[0]
    price_list.append(price)
price_list[2] = "1315"

smart_villas_mauritius_df = pd.DataFrame({"Name": villa_name_list,
                                          "N Bedrooms": n_bedrooms_list,
                                          "N Bathrooms": n_bathrooms_list,
                                          "Price (eur)": price_list})
smart_villas_mauritius_df.to_csv("smart_villas_mauritius.csv")

# url = "https://www.tokopedia.com/?utm_source=google&utm_medium=cpc&utm_campaign=[SEM]:BR|Tokopedia_prf-tp-ID51MLAB01-TT24-alon-alon"
# headers = ({'user-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#             'Accept-Language': 'en-US, en:q=0.5'})
# req = requests.get(url, headers=headers)
# print(req)
