from .models import Member, Dialog, Keyword , Symptom
import requests
import json
import csv
import urllib
from selenium import webdriver
import time
import os
import shutil
from bs4 import BeautifulSoup
import re

def line(line_id):
    print (line_id)

def fluforecase(threshold=80000):
    downloadPath = "//home//kevin//下載//_門急診類流感總就診人次.csv"
    # with open(path, 'r', encoding="utf8") as file:
    #     reader = csv.reader(file)
    #     for row in reader:
    #         print(row)
    # if os.path.exists(path):
    #     shutil.move(path,"flu_predict.csv")

    path = "//home//kevin//TrueProject//misproject//dialog//fluforecase.csv"


    browser = webdriver.Chrome(executable_path= "//home//kevin//TrueProject//misproject//dialog//chromedriver")

    browser.get('https://fluforecast.cdc.gov.tw/#/AllTaiwan')
    #browser.maximize_window()
    time.sleep(3)

    browser.find_element_by_xpath("(//button[@type='button'])[9]").click()
    time.sleep(3)
    #browser.find_element_by_class_name("btn btn-download-csv")[0].click()
    browser.find_element_by_xpath("(//button[@type='button'])[6]").click()


    time.sleep(4)
    browser.close()


    if os.path.exists(downloadPath):
        if os.path.exists(path):
            os.remove(path)
        shutil.move(downloadPath, path)
        with open(path, 'r', encoding="utf8") as file:
            reader = csv.reader(file)
            for row in reader:
                    print(row)
                    if row[0] =='Ensemble':

                        send =  float(row[1])>threshold
    if send:
            return "流感爆發囉"
    else:
            return "最近流感疫情還好"




def push_info(title,text):
    for mem in Member.objects.all():
        Dialog.objects.create(content=text, time='', member=mem, who=False)

    header = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic Njc0YWRiNGMtZjc2Mi00OWMzLTliZmMtZDE2ZTRjMDcwNmU3"}

    payload = {"app_id": "a12ea3d5-3ee7-4995-b6ad-8f4fbb42aee2",
                         "included_segments": ["All"],
                         "chrome_web_icon": "https://github.com/ArthurYang1228/MIS_project/blob/master/misproject/img/logo-2.png?raw=true",
                         # "include_player_ids":["90621e10-88aa-4e9a-a5ba-5e69f3e0bd48"],
                         # "send_after": "2018-05-26 00:30:00 am UTC+8:00 ",
                         "contents": {"en": title}}

    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))


def forecase_web_data():
    title = fluforecase()
    push_info(title,title)

def med(pk):

    name = Member.objects.get(pk=pk)
    unit = Dialog.objects.create(content="Crobot提醒你吃藥拉", time='', member=name, who=False)
    unit.save()
    if re.search("[a-zA-Z]",name.name):
        name.name =  name.name
    else:
        name.name =  name.name[1:]

    header = {"Content-Type": "application/json; charset=utf-8",
                        "Authorization": "Basic Njc0YWRiNGMtZjc2Mi00OWMzLTliZmMtZDE2ZTRjMDcwNmU3"}

    payload = {"app_id": "a12ea3d5-3ee7-4995-b6ad-8f4fbb42aee2",
                         "chrome_web_icon": "https://github.com/ArthurYang1228/MIS_project/blob/master/misproject/img/logo-2.png?raw=true",
                         "include_player_ids":[name.playerid],
                         "contents": {"en": name.name+"~Crobot 提醒您吃藥囉！" }}

    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))

def get_gvm():
    #食譜
    url = "https://health.gvm.com.tw/article_list_tag_%E9%A3%9F%E8%AD%9C.html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    soup2 = soup.find("div", "def-panel")
    stm = ""
    for i in soup2.find_all("div", "item-content"):
        title = i.find("a").string
        web = "https://health.gvm.com.tw/"+i.find("a").get('href')
        content = i.find("p").string
        stm = title+'\n'+content+'\n'+'詳細食譜:'+web
        break
    return stm

def recipe():
    title = get_gvm()
    push_info(title, title)

