import nltk
import requests
import json
from bs4 import BeautifulSoup
import urllib
import time
import os
import jieba
import jieba.posseg as psg
import jieba.analyse

jieba.set_dictionary('dict.txt.big')
s = "我昨天一直咳嗽，還有些發燒，今天早上的時候雖然好一些了。但是仍然不斷的流鼻水的座右銘"
words = jieba.analyse.extract_tags(s,2)

for w in words:
    print(w)
'''''
url = "http://www.commonhealth.com.tw/article/article.action?eturec=1&block=subchannel-pop&nid=77028"

r = requests.get(url)

soup = BeautifulSoup(r.text, 'html.parser')
text = soup.get_text(strip=True)
print(text)

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

print(text)
'''

