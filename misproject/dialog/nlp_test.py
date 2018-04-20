import nltk
import requests
import json
from bs4 import BeautifulSoup
import urllib
import time
import os

url = "http://www.commonhealth.com.tw/article/article.action?eturec=1&block=subchannel-pop&nid=77028"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
text = soup.get_text(strip=True)
print(text)

'''''
stm = []
for i in soup.find_all('div', 'commonArticle'):
    for l in i.find_all('p'):
        if "img" in str(l):
            print("err")
        else:
            stm.append(str(l))




for num in range(len(stm)):
    if "img" in stm[num]:
        del stm[num]
'''
print(text)
