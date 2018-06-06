from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden, JsonResponse
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
from linebot.models import *
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



def response_line(pk, text):
	name = Member.objects.get(pk=pk)
	member = Dialog.objects.filter(member= name)
	loc = None
	choice = None
	back = {}
	if len(member)>1 and Keyword.objects.filter(key=text, father_key__key = member[len(member)-2].content) :
		key = Keyword.objects.get(key=text, father_key__key = member[len(member)-2].content)
		Dialog.objects.create(content=text, member=name,from_key=key)

		if key.response_type == 1:
			back={'type':1, 'text': key.response}
			Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)

		elif key.response_type == 2:
			res = key.response.split(';')
			Dialog.objects.create(content=res[0], member=name, who=False, from_key=key)
			back = {'type': 2, 'text': key.response}

		elif key.response_type == 3:
			if ';' in key.response:
				response = key.response.split(';')
				for i in range(0,len(response),1):
					Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
				back = {'type': 3, 'text': key.response}

			else:
				Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)
				back = {'type': 1, 'text': key.response}


		elif key.response_type == 4:
			response = key.response.split('def')
			unit = Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
			unit.save()

	elif Keyword.objects.filter(key=text, father_key__key = None):
		key = Keyword.objects.get(key=text, father_key__key = None)
		Dialog.objects.create(content=text, member=name,from_key=key)
		if key.response_type == 1:
			Dialog.objects.create(content=key.response, member=name, who=False,from_key=key)
			back = {'type': 1, 'text': key.response}
		elif key.response_type == 2:
			response = key.response.split(';')
			Dialog.objects.create(content=response[0], member=name, who=False,from_key=key)
			back = {'type': 2, 'text': key.response}
		elif key.response_type == 3:
			if ';' in key.response:
				response = key.response.split(';')
				for i in range(0,len(response),1):
					Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
				back = {'type': 3, 'text': key.response}
			else:
				Dialog.objects.create(content=key.response, member=name, who=False, from_key=key)
				back = {'type': 3, 'text': key.response}
		elif key.response_type == 4:
			response = key.response.split('def')
			Dialog.objects.create(content=response[0], member=name, who=False, from_key=key)
			back = {'type': 1, 'text': response[0]}


	elif len(member) > 1 and member[len(member) - 1].content == "Crobot提醒你吃藥拉" and text == '明天也繼續提醒我吧':
		Dialog.objects.create(content=text, member=name)
		oneTime = member[len(member) - 1].time


		for t in tomorrow(str((oneTime.hour+8)%24)+":"+str(oneTime.minute)):
			url = "https://140.119.19.33:8080/schedule"

			# try:
			requests.post(url, json={'time': t, 'line_id': name.email})
			print (name.email)
			# except:
			#     print('fail')
			  # TODO.......................................................
		Dialog.objects.create(content='好的明天同時間提醒您', member=name, who=False)
		back = {'type': 1, 'text': '好的明天同時間提醒您'}

	elif len(member)>1 and member[len(member)-1].content=="請問Crobot要什麼時候提醒你呢?":
		set_time = list(tomorrow(text))

		Dialog.objects.create(content=text, member=name)
		if  len(set_time) == 0:
			Dialog.objects.create(content='無法判斷時間抱歉', member=name, who=False)
			back = {'type': 1, 'text': '無法判斷時間抱歉'}
		else:
			for oneTime in set_time:
				# a = int(set_time[i][0])
				# b = int(set_time[i][1])
				url = "https://140.119.19.33:8080/schedule"
				# try:
				requests.post(url, json={'time': oneTime, 'line_id': name.email})
				print (name.email)
				# except:
				#     print('fail')
			Dialog.objects.create(content='已為您設好時間', member=name, who=False)
			back = {'type': 1, 'text': '已為您設好時間'}




	elif len(member)>1 and member[len(member)-1].content=="可以描述一下你的症狀嗎？":

		Dialog.objects.create(content=text, member=name, from_key=member[len(member)-1].from_key)
		response, desease = get_advice(text)
		Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member)-1].from_key)
		back = {'type': 1, 'text': response}

		if not response == "無法判別，請提供更多資訊":

			choice = "T"
			all = ["查詢預防"+desease[-1][0], '嚴重疾病', '尋找醫院','知道了謝謝']
			back = {'type': 2, 'text': response + ";" + ",".join(all)}

		else:
			choice = "T"
			all = ["症狀查詢" , '知道了謝謝']
			back = {'type': 2, 'text': response + ";" + ",".join(all)}
	elif text == '嚴重疾病' and len(member)>1:
		Dialog.objects.create(content=text, member=name, from_key=member[len(member) - 1].from_key)
		response, desease = get_advice(member[len(member)-2].content,False)
		Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member) - 1].from_key)
		back = {'type': 1, 'text': response}

		if not response == "無法判別，請提供更多資訊":
			choice = "T"
			all = ["查詢預防" + desease[0][0], '尋找醫院', '知道了謝謝']
			back = {'type': 2, 'text': response + ";" + ",".join(all)}
		else:
			choice = "T"
			all = ["症狀查詢" , '知道了謝謝']
			back = {'type': 2, 'text': response + ";" + ",".join(all)}

	elif "查詢預防" in text and len(member)>3 and (member[len(member)-3].content=="可以描述一下你的症狀嗎？" or member[len(member)-2].content=="其他疾病"):
		Dialog.objects.create(content=text, member=name, from_key=member[len(member) - 1].from_key)
		response = Symptom.objects.get(name=text.strip("查詢預防")).prevention
		Dialog.objects.create(content=response, member=name, who=False, from_key=member[len(member) - 1].from_key)
		choice = "T"
		all = ['知道了謝謝']
		back = {'type': 2, 'text': response + ";" + ",".join(all)}



	else:
		Dialog.objects.create(content=text, member=name)
		res = get_res(text)
		Dialog.objects.create(content=res, member=name, who=False)
		back = {'type': 1, 'text': res}

	return back


# line API
def schedule(request):
	if request.method == 'POST':
		time = request.POST["time"]
		line_id = request.POST["line_id"]
		Schedule.objects.create(func='dialog.tasks.line',
								# hook = '',
								args=line_id,
								# kwargs={'title': "hi", 'text': 'trash'},

								schedule_type=Schedule.ONCE,
								next_run=time
								)
# def call_line(request):
#     push_line_one(line_id)

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
			# 加好友事件
			if isinstance(event, FollowEvent):
				# 將id加到資料庫
				line_id = event.source.user_id
				profile = line_bot_api.get_profile(event.source.user_id)
				line_name = profile.display_name
				'''Member.objects.create(name=line_name+"_line", email=line_id, password="line")'''
				message1 = TextSendMessage(text=line_name + "\n歡迎你跟Crobot做朋友!\n快來和Crobot做朋友吧!")
				message2 = StickerSendMessage(package_id="1", sticker_id="2")
				message = [message1, message2]
				line_bot_api.reply_message(event.reply_token, message)


			# 訊息事件
			elif isinstance(event, MessageEvent):
				# 文字訊息
				if isinstance(event.message, TextMessage):
					# 抓text, pk
					text = event.message.text
					try:
						who = Member.objects.get(email=event.source.user_id)
						pk = who.id

					# 若沒pk,將使用者加到Member資料庫
					except:
						line_id = event.source.user_id
						profile = line_bot_api.get_profile(event.source.user_id)
						line_name = profile.display_name
						Member.objects.create(name=line_name + "_line", email=line_id, password="line")
						message = TextSendMessage(text="等等，你還沒被加進資料庫,沒有pk\n立刻完成動作--\n已加到資料庫!\n再傳一次吧")
						# line_bot_api.reply_message(event.reply_token, message)
						who = Member.objects.get(email=event.source.user_id)
						pk = who.id

					# line自訂狀況
					if text == "測試":
						message1 = TextSendMessage(text="你的ID : " + event.source.user_id)
						# message1 = TextSendMessage(text= str(all_id))
						profile = line_bot_api.get_profile(event.source.user_id)
						message2 = TextSendMessage(text="你的名字 : " + profile.display_name)
						message3 = TextSendMessage(text="你的照片 : " + profile.picture_url)
						message = [message1, message2, message3]
					# Dialog.objects.create(content=text, member=name)

					elif text == "資料庫id":
						who = Member.objects.get(email=event.source.user_id)
						pk = who.id
						message = TextSendMessage(text=pk)
					# Dialog.objects.create(content=text, member=name)

					# 為推播做準備的"全部id"
					elif text == "抓全部id":
						corrects = Member.objects.filter(password="line")
						all_id = []
						for correct in corrects:
							all_id.append(correct.email)
						message = TextSendMessage(text=str(all_id))
					# Dialog.objects.create(content=text, member=name)

					# 推播
					elif "aaa" in text:
						push_line_all()
						message = TextSendMessage(text="已完成推播")
					# Dialog.objects.create(content=text, member=name)
					# 吃藥
					elif "bbb" in text:
						push_line_one(who.email)



					# 尋找醫院
					elif text == "尋找醫院":
						message1 = TextSendMessage(text="Crobot不知道你在哪裡><\n傳送位置訊息給我吧!\n教學如下↓")
						message2 = TextSendMessage(text="鍵盤>箭頭>加號>位置訊息>公開所在位置\n這樣Crobot就可以幫你定位囉!")
						message = [message1, message2]
					# Dialog.objects.create(content=text, member=name)

					# 使用response_line(pk, text回訊息)
					else:
						back = response_line(pk, text)
						if back['type'] == 1:
							if "？" in back['text']:
								message1 = TextSendMessage(text=back['text'])
								message2 = StickerSendMessage(package_id="2", sticker_id="149")
								message = [message1, message2]
							elif "~" in back['text']:
								message1 = TextSendMessage(text=back['text'])
								message2 = StickerSendMessage(package_id="3", sticker_id="184")
								message = [message1, message2]
							else:
								message = TextSendMessage(text=back['text'])

						elif back['type'] == 2:
							response = back['text'].split(';')
							choices = response[1].split(',')
							action = []
							for choice in choices:
								action.append(MessageTemplateAction(
									label=choice,
									text=choice))

							message = TemplateSendMessage(
								alt_text='Button template',
								template=ButtonsTemplate(
									text=response[0],
									actions=action
								)
							)
						elif back['type'] == 3:
							if ";" in back['text']:
								response = back['text'].split(';')
								message1 = TextSendMessage(text=response[1])
								message2 = ImageSendMessage(
									original_content_url=response[0],
									preview_image_url=response[0]
								)
								message = [message1, message2]
							else:
								message = ImageSendMessage(
									original_content_url=back['text'],
									preview_image_url=back['text']
								)

					# 用api回以上任何狀況的訊息!!! 沒有這行line用戶是看不到訊息的
					line_bot_api.reply_message(event.reply_token, message)

				# 貼圖訊息
				elif isinstance(event.message, StickerMessage):
					message = TextSendMessage(text="抱歉Crobot目前沒辦法解讀非文字訊息！但我會隨機生成貼圖XD")
					message2 = StickerSendMessage(package_id="2", sticker_id=random.randint(140, 179))
					line_bot_api.reply_message(event.reply_token, [message, message2])

				# 位置訊息
				elif isinstance(event.message, LocationMessage):
					message = LocationSendMessage(
						title='回傳位置',
						address=event.message.address,
						latitude=event.message.latitude,
						longitude=event.message.longitude
					)
					# line_bot_api.reply_message(event.reply_token,message)
					lat = str(event.message.latitude)
					lng = str(event.message.longitude)
					line_bot_api.reply_message(event.reply_token, TextSendMessage(
						text="https://crobottest.herokuapp.com/location/" + lat + '-' + lng))

				# 其餘訊息
				else:
					line_bot_api.reply_message(event.reply_token, TextSendMessage(text="其餘事件"))

		return HttpResponse()
	else:
		try:
			corrects = Member.objects.filter(password="line")
			all_id = []
			for correct in corrects:
				all_id.append(correct.email)
			message1 = TextSendMessage(
				text="Crobot來暖心提醒囉！\n最近天氣很熱\n開冷氣之餘也記得別別調太低溫，以免感冒唷！\n若出現感冒症狀，請立刻使用Crobot的症狀查詢功能，以免病情加重，Crobot團隊關心您！")
			message2 = StickerSendMessage(package_id="2", sticker_id="34")
			message = [message1, message2]
			line_bot_api.multicast(all_id, message)
		except:
			pass
		return HttpResponse()


def push_line_all():
	try:
		corrects = Member.objects.filter(password="line")
		all_id = []
		for correct in corrects:
			all_id.append(correct.email)
		message1 = TextSendMessage(
			text="Crobot來暖心提醒囉！\n最近天氣很熱\n開冷氣之餘也記得別別調太低溫，以免感冒唷！\n若出現感冒症狀，請立刻使用Crobot的症狀查詢功能，以免病情加重，Crobot團隊關心您！")
		message2 = StickerSendMessage(package_id="2", sticker_id="34")
		message = [message1, message2]
		line_bot_api.multicast(all_id, message)
	except:
		pass


def push_line_one(line_id):
	try:
		message = TemplateSendMessage(
			alt_text='Button template',
			template=ButtonsTemplate(
				text="Crobot提醒你吃藥拉",
				actions=[
					MessageTemplateAction(
						label='明天也繼續提醒我吧',
						text='明天也繼續提醒我吧',
					),
					MessageTemplateAction(
						label='明天不用了',
						text='明天不用了'
					)
				]
			)
		)
		line_bot_api.push_message(line_id, message)
	except:
		pass


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
	Schedule.objects.create(func='dialog.tasks.push_info',
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


def refresh(request, pk):
	dialog = Dialog.objects.filter(member=Member.objects.get(pk=pk))
	member = Member.objects.filter(pk=pk)
	# #if dialog[len(dialog) - 1].time:
	# for d in dialog:
	#     if datetime.isoformat()
	newMessage = []

	if request.GET.get('playerid',''):
		playerid = request.GET.get('playerid','')
		member.update(playerid = playerid)

		newMessage.append(playerid)
	elif request.GET.get('last_id',''):


		for d in dialog:
			if int(d.id)> int(request.GET.get('last_id','')) and '/' in d.content:
			   newMessage.append(('youshouldrefresh', d.content))
			elif int(d.id)> int(request.GET.get('last_id','')) and d.who:
			   newMessage.append(('message',d.content+"("+d.time+")",d.id))
			elif int(d.id)> int(request.GET.get('last_id','')) and not d.who:
			   newMessage.append(('message2', d.content+d.time.strftime("(%Y年%m月%d日 %H:%M)"),d.id))

	return JsonResponse(newMessage, safe=False)



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
		new_member = Member.objects.create(name=name, gender=gender, email=email, password=password, birthday=birthday,
										   playerid = '')
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
					for i in range(0,len(response),1):
						unit = Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
						unit.save()
					if '/static/images/member' in key.response:
						choice = "T"
						mem = ['陽承霖','林士翔','陳瑞涓','游智凱','王超']
						all = mem
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
					for i in range(0,len(response),1):
						unit = Dialog.objects.create(content=response[i], member=name, who=False, from_key=key)
						unit.save()
					if '/static/images/member' in key.response:
						choice = "T"
						mem = ['陽承霖','林士翔','陳瑞涓','游智凱','王超']
						all = mem
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



	# time.sleep(2)
	member = Dialog.objects.filter(member=Member.objects.get(pk=pk))
	last_id = member[len(member) - 1].id
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
		return redirect("https://140.119.19.33:8080/key/")
	else:
		""
	return render(request, 'insert_keyword.html',locals())

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




