from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from .models import Member, Dialog, Keyword , Symptom
import requests
import json
import time
from django_q.tasks import async, result
from django_q.models import Schedule
import arrow
from dialog.time_x import *
from dialog.tasks import *



from django.views.decorators.csrf import csrf_exempt
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent, TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    StickerSendMessage,
    ButtonsTemplate, ConfirmTemplate, CarouselTemplate,
    PostbackTemplateAction, MessageTemplateAction, URITemplateAction,
    CarouselColumn
)
import random
import jieba
import jieba.posseg as psg
import jieba.analyse


line_bot_api = LineBotApi('M1N5WC/S4CduQ9HP9HIAoL2Q/Hpy1Tj6uYrfxEGXGESLXWofPewC901SvBOMnkxBpklwGJt1XgyFcaHzTcp+6Xa/6Y/SWBhNEhTXXi+bMK8MOaQvZQuue9Yo9ZdYqpjWZMYd+ZB0iHkD1YeeB1Pd6QdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('00c4e070d24133d8c3329ed65ebc5246')
@csrf_exempt


def get_key(stm):
    jieba.set_dictionary('dict.txt.big')
    jieba.load_userdict('sym.txt')
    words = jieba.analyse.extract_tags(stm,5,withWeight=True,allowPOS="n")

    return words

def get_advice(stm, common= True):

    array = []
    dict = {}
    symptom = set(get_key(stm))
    res = ""
    division = []

    for k in symptom:


        for sym in Symptom.objects.filter(symptom__contains=k[0]):

            array.append(sym.name)
            if sym.name in dict.keys():

                dict[sym.name][1] += 1
            else:
                d = sym.symptom
                d = d.strip("['")
                d = d.strip("']")
                d_array = d.split("．")
                dict[sym.name] = [sym.level,1,len(d_array)]

    final_dict = {}
    for sym in set(array):
        a = dict[sym]
        normal = 1/(float(a[0])+1)
        stm_fitness = a[1]/len(symptom)
        dis_fitness = a[1]/a[2]
        final_dict[sym] = normal*stm_fitness*dis_fitness
    sorted_d =sorted(final_dict.items(), key=lambda x:x[1])

    result = []
    if common:

        for dea in sorted_d[::-1]:

            if dict[dea[0]][0]=="0" :
                result.append(dea)

            if len(result)==3:
                break

    if len(result)<3 or (not common) :

        for dea in sorted_d[::-1]:
            print(dea)
            if dict[dea[0]][0] == "2" or dict[dea[0]][0]=="3" or dict[dea[0]][0]=="1":
                result.append(dea)

            if len(result) == 3:
                break



    if len(result) ==0:
        res += "無法判別，請提供更多資訊"
        return res, sorted_d

    res += "可能是："

    for r in result:
        res += r[0]
        division.append(Symptom.objects.get(name=r[0]).division)

    for sym in result:
        if dict[sym[0]][0] != '0':
            res += "有可能是較嚴重的疾病，建議進一步諮詢" + division[0]
            return res, sorted_d


    res += "可以自我照顧，但如果持續太久還是需要諮詢一下" + division[0]

    return res, sorted_d



def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):
                if isinstance(event.message, TextMessage):
                    text = event.message.text
                    if  Keyword.objects.filter(key=text):
                        key = Keyword.objects.get(key=text)
                        if key.response_type == 1:
                            message = TextSendMessage(text=key.response)
                            message2 = StickerSendMessage(package_id = "2" , sticker_id = "149")
                            line_bot_api.reply_message(event.reply_token,[message, message2])


                        elif key.response_type == 2:
                            response = key.response.split(';')
                            choices = response[1].split(',')
                            action=[]
                            for choice in choices:
                                action.append(MessageTemplateAction(
                                            label=choice,
                                            text=choice))

                            message = TemplateSendMessage(
                                alt_text='Confirm template',
                                template=ConfirmTemplate(
                                    text=response[0],
                                    actions = action
                                )
                            )
                            line_bot_api.reply_message(event.reply_token,message)

                    else:
                        url = "https://crobott.herokuapp.com/chatterbot/"
                        r = json.loads(requests.post(url, json={'text': text}).content.decode())
                        message = TextSendMessage(text=r['text'])
                        line_bot_api.reply_message(event.reply_token,message)

                else:
                    message = TextSendMessage(text="抱歉Crobot目前沒辦法解讀非文字訊息！但我會隨機生成貼圖QQ")
                    message2 = StickerSendMessage(package_id = "2" , sticker_id = random.randint(140,179))
                    line_bot_api.reply_message(event.reply_token,[message, message2])

        return HttpResponse()
    else:
        return HttpResponseBadRequest()


def get_res(text, port=8000):

    url = "http://140.119.19.33:{}/chatterbot/".format(port)



    try:
        r = json.loads(requests.post(url, json={'text': text}).content.decode())
        return r['text']

    except:
        return "I don't know"

def auto_remind(time,pk):
    unit = Schedule.objects.create(func='dialog.tasks.med',
                                   # hook = '',
                                   args=pk,
                                   # kwargs={'title': "hi", 'text': 'trash'},

                                   schedule_type=Schedule.ONCE,
                                   next_run = time
                                   )
    # next_run = arrow.utcnow().replace(hour=a, minute=b).format(
    #     'YYYY-MM-DD HH:mm:ss')
    unit.save()

def push_to_all(time,title="",text=""):
    Schedule.objects.create(func='dialog.tasks.forecase_web_data',
                                   # hook = '',
                                   args=(title, text),
                                   schedule_type=Schedule.ONCE,
                                   next_run = time
                                   )
    # next_run = arrow.utcnow().replace(hour=a, minute=b).format(
    #     'YYYY-MM-DD HH:mm:ss')



def which_fun(str):
    fun_dict = {'get_key':get_key, 'get_advice':get_advice, 'callback':callback, 'get_res':get_res}
    return fun_dict[str]


def login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            correct = Member.objects.get(email=email)
        # 用filter 才要 correct = correct[0]
        except:
            correct = None

        if email == "f7123442@gmail.com" and password == "29948545":
            manage = True
        elif correct != None and email == correct.email and password == correct.password:
            verified = True
        # template = get_template('dialog.html')
        # html = template.render(locals())
        # return HttpResponse(html)

        else:
            verified = False

    return render(request, 'login.html', locals())


def register(request):
    if request.method == "POST":
        name = request.POST["name"]
        email = request.POST["email"]
        password = request.POST["password"]
        gender = request.POST["gender"]
        birthday = request.POST["birthday"]
        new_member = Member.objects.create(name=name, gender=gender, email=email, password=password, birthday=birthday)
        new_member.save()

        return redirect('/')
    else:
        ""
    return render(request, 'register.html', locals())






def post(request, pk):



    member = Dialog.objects.filter(member=Member.objects.get(pk=pk))
    name = Member.objects.get(pk=pk)
    loc = None
    choice = None

    if choice==None and len(member) > 1 and member[len(member) - 1].content == "Crobot提醒你吃藥拉":
        choice = "T"
        all = ["明天也繼續提醒我吧", '明天不用了']


    if request.method == "POST":
        text = request.POST['data']
        choice = None

        if len(member)>1 and Keyword.objects.filter(key=text, father_key__key = member[len(member)-2].content) :
            key = Keyword.objects.get(key=text, father_key__key = member[len(member)-2].content)
            Dialog.objects.create(content=text, member=name,from_key=key)

            if key.response_type == 1:
                unit = Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)
                unit.save()
            elif key.response_type == 2:
                response = key.response.split(';')
                unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
                unit.save()
                choice = response[1]
                all = choice.split(',')
            elif key.response_type == 3:
                if ';' in key.response:
                    response = key.response.split(';')
                    # unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
                    # unit.save()
                    # unit = Dialog.objects.create(content=response[1], member=name, who=False, from_key=key)
                    # unit.save()
                    for i in range(0,len(response),1):
                        unit = Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
                        unit.save()
                else:
                    unit = Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)
                    unit.save()
            elif key.response_type == 4:
                response = key.response.split('def')
                unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
                unit.save()

        elif Keyword.objects.filter(key=text, father_key__key = None):
            key = Keyword.objects.get(key=text, father_key__key = None)
            Dialog.objects.create(content=text, member=name,from_key=key)
            if key.response_type == 1:
                unit = Dialog.objects.create(content=key.response, member=name, who=False,from_key=key)
                unit.save()
            elif key.response_type == 2:
                response = key.response.split(';')
                unit = Dialog.objects.create(content=response[0], member=name, who=False,from_key=key)
                unit.save()
                choice = response[1]
                all = choice.split(',')
            elif key.response_type == 3:
                if ';' in key.response:
                    response = key.response.split(';')
                    # unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
                    # unit.save()
                    # unit = Dialog.objects.create(content=response[1], member=name, who=False, from_key=key)
                    # unit.save()
                    for i in range(0,len(response),1):
                        unit = Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
                        unit.save()
                else:
                    unit = Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)
                    unit.save()
            elif key.response_type == 4:
                response = key.response.split('def')
                unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
                unit.save()


        elif len(member) > 1 and member[len(member) - 1].content == "Crobot提醒你吃藥拉" and text == '明天也繼續提醒我吧':
            Dialog.objects.create(content=text, member=name)
            oneTime = member[len(member) - 1].time


            for t in tomorrow(str((oneTime.hour+8)%24)+":"+str(oneTime.minute)):

                auto_remind(t, pk)
            Dialog.objects.create(content='好的明天同時間提醒您', member=name, who=False)

        elif len(member)>1 and member[len(member)-1].content=="請問Crobot要什麼時候提醒你呢?":
            set_time = list(tomorrow(text))

            Dialog.objects.create(content=text, member=name)
            if  len(set_time) == 0:
                Dialog.objects.create(content='無法判斷時間抱歉', member=name, who=False)
            else:
                for oneTime in set_time:
                    # a = int(set_time[i][0])
                    # b = int(set_time[i][1])
                    auto_remind(oneTime,pk)
                Dialog.objects.create(content='已為您設好時間', member=name, who=False)





        elif len(member)>1 and member[len(member)-1].content=="可以描述一下你的症狀嗎？":

            Dialog.objects.create(content=text, member=name, from_key=member[len(member)-1].from_key)
            response, desease = get_advice(text)
            Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member)-1].from_key)

            if not response == "無法判別，請提供更多資訊":
                choice = "T"
                all = ["查詢預防"+desease[-1][0], '嚴重疾病', '尋找醫院','知道了謝謝']
            else:
                choice = "T"
                all = ["症狀查詢" , '知道了謝謝']
        elif text == '嚴重疾病' and len(member)>1:
            Dialog.objects.create(content=text, member=name, from_key=member[len(member) - 1].from_key)
            response, desease = get_advice(member[len(member)-2].content,False)
            Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member) - 1].from_key)

            if not response == "無法判別，請提供更多資訊":
                choice = "T"
                all = ["查詢預防" + desease[0][0], '尋找醫院', '知道了謝謝']
            else:
                choice = "T"
                all = ["症狀查詢" , '知道了謝謝']

        elif "查詢預防" in text and len(member)>3 and (member[len(member)-3].content=="可以描述一下你的症狀嗎？" or member[len(member)-2].content=="其他疾病"):
            Dialog.objects.create(content=text, member=name, from_key=member[len(member) - 1].from_key)
            response = Symptom.objects.get(name=text.strip("查詢預防")).prevention
            Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member) - 1].from_key)
            choice = "T"
            all = ['知道了謝謝']



        elif text == '尋找醫院':
            unit = Dialog.objects.create(content=text, member=name)
            unit.save()
            loc = 'T'
            choice = 'T'
            all = ['我要尋找', '不用了謝謝']

        elif 'https://140.119.19.33:8080' in text:
            unit = Dialog.objects.create(content='我要尋找', member=name, who=True)
            unit.save()
            unit = Dialog.objects.create(content=text, member=name, who=False)
            unit.save()

        else:
            unit = Dialog.objects.create(content=text, member=name)
            unit.save()
            Dialog.objects.create(content=get_res(text), member=name, who=False)




    else:
        text=""




    member = Dialog.objects.filter(member=Member.objects.get(pk=pk))
    # except:
    #     Dialog.objects.create(content="出了點小錯抱歉等等喔", member=name, who=False)
    return render(request, 'dialog.html', locals())


def key_word(request):
    keyword_list = Keyword.objects.all()
    return render(request, 'key_word.html', {
        'keyword_list': keyword_list,
    })

def new_key_word(request):
    if 'create' in request.POST:
        keyword = request.POST['keyword']
        response = request.POST['response']
        response_type = request.POST['response_type']
        Keyword.objects.create(key=keyword, response=response, response_type=response_type)
        return redirect('https://140.119.19.33:8080/key/')
    else:
        ""
    return render(request,"insert_keyword.html",locals())

def update_key_word(request, id):
    keyword_id = request.GET['id']
    update = Keyword.objects.filter(id=keyword_id)
    if 'update' in request.POST:
        keyword = request.POST['keyword']
        response = request.POST['response']
        response_type = request.POST['response_type']
        update.update(key=keyword, response=response, response_type=response_type)
        return redirect("https://140.119.19.33:8080/key/")
    else:
        ""
    return render(request, 'update_keyword.html',locals())

def delete_key_word(request, id):
    keyword_id = request.GET['id']
    delete = Keyword.objects.filter(id=keyword_id)
    delete.delete()
    return render(request,"delete_keyword.html",locals())

def location(request, lat, lng):
    return render(request, 'location.html', locals())

def here(request):
    return render(request, 'here.html', locals())




