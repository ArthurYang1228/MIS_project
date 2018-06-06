# coding=utf-8
import re
import string
import os
import sys
import datetime
import arrow

chs_arabic_map = {u'零':0, u'一':1, u'二':2, u'三':3, u'四':4,
        u'五':5, u'六':6, u'七':7, u'八':8, u'九':9,
        u'十':10, u'百':100, u'千':10 ** 3, u'万':10 ** 4,
        u'〇':0, u'壹':1, u'贰':2, u'叁':3, u'肆':4,
        u'伍':5, u'陆':6, u'柒':7, u'捌':8, u'玖':9,
        u'拾':10, u'佰':100, u'仟':10 ** 3, u'萬':10 ** 4,
        u'亿':10 ** 8, u'億':10 ** 8, u'幺': 1,
        u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
        u'５':5, u'６':6, u'７':7, u'８':8, u'９':9}

def convertChineseDigitsToArabic (chinese_digits):


    result  = 0
    tmp     = 0
    hnd_mln = 0
    for count in range(len(chinese_digits)):
        curr_char  = chinese_digits[count]
        curr_digit = chs_arabic_map.get(curr_char, None)
        # meet 「亿」 or 「億」
        if curr_digit == 10 ** 8:
            result  = result + tmp
            result  = result * curr_digit
            # get result before 「亿」 and store it into hnd_mln
            # reset `result`
            hnd_mln = hnd_mln * 10 ** 8 + result
            result  = 0
            tmp     = 0
        # meet 「万」 or 「萬」
        elif curr_digit == 10 ** 4:
            result = result + tmp
            result = result * curr_digit
            tmp    = 0
        # meet 「十」, 「百」, 「千」 or their traditional version
        elif curr_digit >= 10:
            tmp    = 1 if tmp == 0 else tmp
            result = result + curr_digit * tmp
            tmp    = 0
        # meet single digit
        elif curr_digit is not None:
            tmp = tmp * 10 + curr_digit
        else:
            return result
    result = result + tmp
    result = result + hnd_mln
    return result

# Predefined strings.
numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18| \
         |19|20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40|41| \
          |42|43|44|45|46|47|48|49|50|51|52|53|54|55|56|57|58|59|60)"
chinesenums = "(一|二|兩|三|四|五|六|七|八|九|十|十一|十二|十三|十四|十五|十六|十七|十八|十九|二十|二十一|二十二|二十三|二十四|二十五|二十六| \
              |二十七|二十八|二十九|三十|三十一|三十二|三十三|三十四|三十五|三十六|三十七|三十八|三十九|四十|四十一|四十二|四十三|四十四|四十五|\
              |四十六|四十七|四十八|四十九|五十|五十一|五十二|五十三|五十四|五十五|五十六|五十七|五十八|五十九)"

half = "(半)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|星期一|星期二|星期三|星期四|星期五|星期六|星期日)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday|星期一|星期二|星期三|星期四|星期五|星期六|星期日)"
month = "(january|february|march|april|may|june|july|august|september| \
          october|november|december)"
dmy = "(year|day|week|month)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
bigtime = "(凌晨|早上|中午|下午|晚上)"
dian = "(.)"
exp1 = "(before|after|earlier|later|ago)"
exp2 = "(this|next|last)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
hours = "(點)"
minutes = "(分)"
quote = "(:)"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + month + "))"
regxp3 = "("+bigtime+""+numbers+""+hours+""+numbers+""+minutes+")"
regxp4 = "("+ numbers + "" + hours + ")"
regxp5 = "("+ bigtime +""+numbers+""+hours+")"
regxp6 = "("+ numbers + ""+ quote +""+ numbers +")"
regxp7 = "("+bigtime+""+ chinesenums + ""+ hours +""+ half +")"
regxp8 = "("+bigtime+""+ chinesenums + ""+ hours +")"
regxp9 = "("+bigtime+""+ chinesenums + ""+ hours +""+chinesenums+""+minutes+")"
regxp10 = "("+ bigtime +""+numbers+""+hours+""+half+")"
regxp11 = "("+ bigtime +""+chinesenums+""+hours+""+numbers+""+minutes+")"
regxp12 = "("+ bigtime +""+numbers+""+dian+")"
regxp13 = "("+ bigtime +""+numbers+""+dian+""+half+")"
regxp14 = "("+bigtime+""+numbers+""+hours+""+chinesenums+""+minutes+")"
regxp15 = "("+chinesenums+""+hours+""+half+")"

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)
reg6 = re.compile(week_day)
reg7 = re.compile(regxp3, re.IGNORECASE)
reg8 = re.compile(regxp4, re.IGNORECASE)
reg9 = re.compile(regxp5, re.IGNORECASE)
reg10 = re.compile(regxp6, re.IGNORECASE)
reg11 = re.compile(regxp7, re.IGNORECASE)
reg12 = re.compile(regxp8, re.IGNORECASE)
reg13 = re.compile(regxp9, re.IGNORECASE)
reg14 = re.compile(regxp10, re.IGNORECASE)
reg15 = re.compile(regxp11, re.IGNORECASE)
reg16 = re.compile(regxp12, re.IGNORECASE)
reg17 = re.compile(regxp13, re.IGNORECASE)
reg18 = re.compile(regxp14, re.IGNORECASE)
def tag(text):

    # Initialization
    timex_found = []

    # re.findall() finds all the substring matches, keep only the full
    # matching string. Captures expressions such as 'number of days' ago, etc.
    found = reg1.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # Variations of this thursday, next year, etc
    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    # today, tomorrow, etc
    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

    # ISO
    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    # Year
    found = reg5.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg6.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg7.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg14.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg18.findall(text)
    for timex in found:
        timex_found.append(timex)



    found = reg15.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg9.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg10.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)



    found = reg11.findall(text)
    for timex in found:
        timex_found.append(timex)



    found = reg13.findall(text)
    for timex in found:
            timex_found.append(timex)

    found = reg17.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg16.findall(text)
    for timex in found:
        timex_found.append(timex)


    found = reg8.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    found = reg12.findall(text)
    for timex in found:
        timex_found.append(timex)
    # Tag only temporal expressions which haven't been tagged.
    for timex in timex_found:
        #text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)

        return timex


def subChar(str):
    match = re.compile(u'[\u4e00-\u9fa5]')
    nochinese =  match.sub(r'',str)
    string = re.sub("[\s+\.\!\/_,$%^*(+\"\']+|[+—:！，。？、~@#￥%……&*（）]+", "", nochinese)
    return string

a = "我要在早上9點的時候吃，麻煩提醒我!"
c = "我要在早上8點30分的時候吃藥，麻煩提醒我!!!!"
l = "我要在下午1點三十一分的時候吃藥"
d = "我要在23:50的時候吃藥，麻煩提醒我!!!!"
e = "我要在晚上十點三十二分的時候吃藥，麻煩提醒我!!!!"
f = "我要在晚上9點半的時候吃藥，麻煩提醒我!!!!"
g = "我要在下午三點22分的時候吃藥"
h = "我要在早上八點吃藥"
i = "我要在13:25吃藥"
z = "我希望能在晚上十二點十分、每天00:14、下午三點半以及晚上九點四十六分、晚上十點和13:45的時候吃藥"

def number(str):
    str = subChar(str)
    if len(str)==1:
        return str
    if len(str)==2:
        return str
    if len(str)==3:
        return str[0:1] , str[1:3]
    else:
        return str[0:2], str[2:4]

def nonumber(str):
    if re.search("凌晨一點半", str):
        return "1","30"
    if re.search("凌晨1點半", str):
        return "1","30"
    if re.search("凌晨一點", str):
        return "1"
    if re.search("凌晨1點", str):
        return "1"
    if re.search("下午一點半", str):
        return "13","30"
    if re.search("下午1點半", str):
        return "13","30"
    if re.search("下午一點", str):
        return "13"
    if re.search("下午1點", str):
        return "13"
    if re.search("凌晨兩點半", str):
        return "2","30"
    if re.search("凌晨2點半", str):
        return "2","30"
    if re.search("凌晨兩點", str):
        return "2"
    if re.search("凌晨2點", str):
        return "2"
    if re.search("下午兩點半", str):
        return "14","30"
    if re.search("下午2點半", str):
        return "14","30"
    if re.search("下午兩點", str):
        return "14"
    if re.search("下午2點", str):
        return "14"
    if re.search("凌晨三點半", str):
        return "3","30"
    if re.search("凌晨3點半", str):
        return "3","30"
    if re.search("凌晨三點", str):
        return "3"
    if re.search("凌晨3點", str):
        return "3"
    if re.search("下午三點半", str):
        return "15","30"
    if re.search("下午3點半", str):
        return "15","30"
    if re.search("下午三點", str):
        return "15"
    if re.search("下午3點", str):
        return "15"
    if re.search("凌晨四點半", str):
        return "4","30"
    if re.search("凌晨4點半", str):
        return "4", "30"
    if re.search("凌晨四點", str):
        return "4"
    if re.search("凌晨4點", str):
        return "4"
    if re.search("下午四點半", str):
        return "16","30"
    if re.search("下午4點半", str):
        return "16", "30"
    if re.search("下午四點", str):
        return "16"
    if re.search("下午4點", str):
        return "16"
    if re.search("凌晨五點半", str):
        return "5","30"
    if re.search("凌晨5點半", str):
        return "5", "30"
    if re.search("凌晨五點", str):
        return "5"
    if re.search("凌晨5點", str):
        return "5"
    if re.search("下午五點半", str):
        return "17","30"
    if re.search("下午5點半", str):
        return "17","30"
    if re.search("下午五點", str):
        return "17"
    if re.search("下午5點", str):
        return "17"
    if re.search("早上六點半", str):
        return "6","30"
    if re.search("早上6點半", str):
        return "6","30"
    if re.search("早上六點", str):
        return "6"
    if re.search("早上6點", str):
        return "6"
    if re.search("晚上六點半", str):
        return "18","30"
    if re.search("晚上6點半", str):
        return "18","30"
    if re.search("晚上六點", str):
        return "18"
    if re.search("晚上6點", str):
        return "18"
    if re.search("晚上七點半", str):
        return "19","30"
    if re.search("晚上7點半", str):
        return "19","30"
    if re.search("晚上七點", str):
        return "19"
    if re.search("晚上7點", str):
        return "19"
    if re.search("早上七點半", str):
        return "7","30"
    if re.search("早上7點半", str):
        return "7","30"
    if re.search("早上七點", str):
        return "7"
    if re.search("早上7點", str):
        return "7"
    if re.search("早上八點半", str):
        return "8", "30"
    if re.search("早上8點半", str):
        return "8", "30"
    if re.search("早上八點", str):
        return "8"
    if re.search("早上8點", str):
        return "8"
    if re.search("晚上八點半", str):
        return "20", "30"
    if re.search("晚上8點半", str):
        return "20", "30"
    if re.search("晚上八點", str):
        return "20"
    if re.search("晚上8點", str):
        return "20"
    if re.search("早上九點半", str):
        return "9",'30'
    if re.search("早上9點半", str):
        return "9", '30'
    if re.search("早上九點", str):
        return "9"
    if re.search("早上9點", str):
        return "9"
    if re.search("晚上九點半", str):
        return "21", '30'
    if re.search("晚上9點半", str):
        return "21", '30'
    if re.search("晚上九點", str):
        return "21"
    if re.search("晚上9點", str):
        return "21"
    if re.search("早上十點半", str):
        return "10",'30'
    if re.search("早上10點半", str):
        return "10", '30'
    if re.search("早上十點", str):
        return "10"
    if re.search("早上10點", str):
        return "10"
    if re.search("晚上十點半", str):
        return "22", '30'
    if re.search("晚上10點半", str):
        return "22", '30'
    if re.search("晚上十點", str):
        return "22"
    if re.search("晚上10點", str):
        return "22"
    if re.search("早上十一點半", str):
        return "11",'30'
    if re.search("早上11點半", str):
        return "11",'30'
    if re.search("早上十一點", str):
        return "11"
    if re.search("早上11點", str):
        return "11"
    if re.search("晚上十一點半", str):
        return "23", '30'
    if re.search("晚上11點半", str):
        return "23", '30'
    if re.search("晚上十一點", str):
        return "23"
    if re.search("晚上11點", str):
        return "23"
    if re.search("中午十二點半", str):
        return "12","30"
    if re.search("中午12點半", str):
        return "12","30"
    if re.search("中午十二點", str):
        return "12"
    if re.search("中午12點", str):
        return "12"
    if re.search("晚上十二點半", str):
        return "0","30"
    if re.search("晚上12點半", str):
        return "0","30"
    if re.search("晚上十二點", str):
        return "0"
    if re.search("晚上12點", str):
        return "0"

def convert(str):
    tag_text = tag(str)
    a = convertChineseDigitsToArabic(tag_text[4])
    return nonumber(str), a

def remind(str):
    if re.search("\d",str):
        return number(str)
    else:
        return nonumber(str)

def convertnum(str):
    tag_text = tag(str)
    return nonumber(tag_text[0]), tag_text[4]


def converttime(str):
   bigtime = "(凌晨|早上|中午|下午|晚上)"
   numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
             eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
             eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
             ninety|hundred|thousand|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15|16|17|18|19| \
             |20|21|22|23|24|25|26|27|28|29|30|31|32|33|34|35|36|37|38|39|40| \
             |41|42|43|44|45|46|47|48|49|50|51|52|53|54|55|56|57|58|59|60)"
   minutes = "(分)"
   quotes = "(:)"
   try:
      if re.search(bigtime, str):
         tag_text = tag(str)
         if re.search(minutes, str):
            if re.search(numbers, tag_text[4]):
               return convertnum(str)
            else:
               return convert(str)
         elif type(nonumber(str)) == tuple:
             return (nonumber(str))
         else:
             return (nonumber(str), "0")
      elif re.search(quotes,str):
         return number(str)
      else:
         return "請輸入合理時間並標明早上|下午|晚上"
   except IndexError:
       return "請輸入合理時間並標明早上|下午|晚上"
   except TypeError:
       return "請輸入合理時間並標明早上|下午|晚上"



def finaltime(my_str):

    sep = "(、|跟|和|還有|及)"
    time_list = []
    for r in sep:
        my_str = my_str.replace(r, ' ')
    my_str = my_str.split()

    for i in range(len(my_str)):
        time = converttime(my_str[i])
        time_list.append(time)
    return time_list





def tomorrow(str):
  try:
     for i in range(len(finaltime(str))):
        if int((finaltime(str)[i][0])) < int(datetime.datetime.now().strftime("%H")):
          yield (arrow.now().replace(day = arrow.now().day + 1 , hour = int(finaltime(str)[i][0]) , minute = int(finaltime(str)[i][1]) , second = 0).format('YYYY-MM-DD HH:mm:ss'))
        elif int((finaltime(str)[i][0])) == int(datetime.datetime.now().strftime("%H")):
           if int(finaltime(str)[i][1]) <= int(datetime.datetime.now().strftime("%M")):
               yield (arrow.now().replace(day=arrow.now().day + 1, hour=int(finaltime(str)[i][0]), minute=int(finaltime(str)[i][1]), second=0).format('YYYY-MM-DD HH:mm:ss'))
           else:
               yield (arrow.now().replace(day=arrow.now().day, hour=int(finaltime(str)[i][0]), minute=int(finaltime(str)[i][1]), second=0).format('YYYY-MM-DD HH:mm:ss'))
        else:
            yield (arrow.now().replace(day = arrow.now().day, hour = int(finaltime(str)[i][0]) , minute = int(finaltime(str)[i][1]) , second = 0).format('YYYY-MM-DD HH:mm:ss'))
  except ValueError:
      return None
  except TypeError:
      return None

# for i in tomorrow("希望每天晚上十二點半和晚上七點四十五分以及2334的時候可以提醒我吃藥"):
#     print(i)
#



