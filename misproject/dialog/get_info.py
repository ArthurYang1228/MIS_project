#encoding = utf-8
import requests
import json
from bs4 import BeautifulSoup
import csv
import urllib

def get_udn():
    url = 'https://health.udn.com/health/disease_list'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    body = soup.find('div', id ='diagnosis_body')



    with open('example4.csv', 'w') as csvfile:
        fieldnames = ['疾病名', '英文病名', '科別','器官','簡介','症狀','預防和治療']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        url_detail = 'https://health.udn.com'
        for u in body.find_all('a'):
            into = requests.get(url_detail + u['href'])
            into_soup = BeautifulSoup(into.text, 'html.parser')
            a = into_soup.find('div',id = 'story_body_content')
            address = into_soup.find('address')
            section = into_soup.find('section')
            str = []
            for i in address.find_all('h3'):
                str.append(i.text)
            try:
                s = []
                for i in section.text.split('症狀'):
                    if '.' in i or '．' in i:
                        s.append(i.split('好發族群')[0])
                writer.writerow({'疾病名':a.find('h1').text, '英文病名':str[0], '科別':str[1], '器官':str[2]
                                , '簡介':address.find('p').text, '症狀':s
                                , '預防和治療':section.find_all('ol')[1].find('li').text})
            except:
                pass
            print("finish"+a.find('h1').text)

    '''
    url = 'https://health.udn.com/health/disease_list'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    body = soup.find('div', id ='diagnosis_body')
    body.find_all('span')
    stm = []

    for i in body.find_all('a'):
        stm.append(i.string)


    stm = {'udn':stm}
    print(stm)
    file = open('Symptom.csv', 'w',newline='',encoding='utf-8')
    csvCursor = csv.writer(file)

    csvCursor.writerow(stm)
    csvCursor.writerow(stm['udn'])
    file.close()

url = 'https://www.top1health.com/Category/%E6%9C%8D%E5%8B%99/%E6%9F%A5%E7%97%87%E7%8B%80'
r = urllib.request.urlopen(url).read().decode('UTF-8')
soup = BeautifulSoup(r, 'html.parser')

with open('example4.csv','r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row['症狀'])
'''
get_udn()