from .models import Member, Dialog, Keyword , Symptom
import requests
import json
import csv
import urllib
from selenium import webdriver
import time
import os
import shutil

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
              "Authorization": "Basic NjY5NDBjMjItOTkwZS00YjY2LTgxOGMtMDA0OTllOTliZTQ1"}

    payload = {"app_id": "53af60e2-5c37-49e4-9b46-f58c6e329366",
               "included_segments": ["All"],
               "chrome_web_icon": "https://raw.githubusercontent.com/ArthurYang1228/MIS_project/master/misproject/LOGO(%E7%B2%89%2B%E8%97%8D).png",
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

    header = {"Content-Type": "application/json; charset=utf-8",
              "Authorization": "Basic NjY5NDBjMjItOTkwZS00YjY2LTgxOGMtMDA0OTllOTliZTQ1"}

    payload = {"app_id": "53af60e2-5c37-49e4-9b46-f58c6e329366",
               "included_segments": ["All"],
               "chrome_web_icon": "https://raw.githubusercontent.com/ArthurYang1228/MIS_project/master/misproject/LOGO(%E7%B2%89%2B%E8%97%8D).png",
               # "include_player_ids":["90621e10-88aa-4e9a-a5ba-5e69f3e0bd48"],
               #"send_after": "2018-05-26 00:30:00 am UTC+8:00 ",
               "contents": {"en": "Crobot 提醒您吃藥囉!"}}

    requests.post("https://onesignal.com/api/v1/notifications", headers=header, data=json.dumps(payload))


