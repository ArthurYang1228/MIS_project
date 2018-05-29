#encoding = utf-8
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
jieba.load_userdict('sym.txt')

path = 'example4.csv'
with open(path, 'r', encoding="utf8") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)
















def get_key(s):
    words = jieba.analyse.extract_tags(s,5,withWeight=True,allowPOS="h")

    return words

def get_cut(s):
    words = psg.cut(s)
    cut = []
    for w in words:
        cut.append((w.word, w.flag))
    return cut









'''
def get_advice(stm):
    array = []
    for k in get_key(s):
        print(k[0])
        array.append(Symptom.objects.filter(symptom__contains= k[0] , level='1'))

'''
