from selenium import webdriver
# driver = webdriver.Firefox()
# driver.get("https://www.google.com/")
import json
import requests

# url = "http://140.119.19.33:{}/chatterbot/".format("8000")
#
#
#
#
# r = json.loads(requests.post(url, json={'text': "Can I help you with anything?"}).content.decode())
# print(r)

t = "查詢自閉症"
t.strip("查詢")
print(t.strip("查詢"))