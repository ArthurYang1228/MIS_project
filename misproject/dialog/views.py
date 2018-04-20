from datetime import datetime
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Member, Dialog, Keyword
import requests
import json
import time



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
    current_time = datetime.now()
    member = Dialog.objects.filter(member=Member.objects.get(pk=pk))
    name = Member.objects.get(pk=pk)

    if request.method == "POST":
        text = request.POST['data']
        unit = Dialog.objects.create(content=text, time='', member=name)
        unit.save()
        if  Keyword.objects.filter(keyword=text):
            key = Keyword.objects.get(keyword=text)
            if key.response_type == 1:
                unit = Dialog.objects.create(content=key.response, time='', member=name, who=False)
                unit.save()
            elif key.response_type == 2:

                response = key.response.split(';')
                unit = Dialog.objects.create(content=response[0], time='', member=name, who=False)
                unit.save()
                choice = response[1]



        else:
            get_res(text, pk)


    else:
        text=""
    return render(request, 'dialog.html', locals())



def get_res(text, pk, port=8080):

    url = "http://127.0.0.1:{}/chatterbot/".format(port)
    current_time = datetime.now()
    member = Dialog.objects.filter(member=Member.objects.get(pk=pk))
    name = Member.objects.get(pk=pk)
    try:
        r = json.loads(requests.post(url, json={'text': text}).content.decode())
        unit = Dialog.objects.create(content=r['text'], time='', member=name, who=False)
        unit.save()
    except:
        unit = Dialog.objects.create(content="I don't know", time='', member=name, who=False)
        unit.save()

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
		Keyword.objects.create(keyword=keyword, response=response, response_type=response_type)
	return render(request,"insert_keyword.html",locals())

def update_key_word(request, id):
	keyword_id = request.GET['id']
	update = Keyword.objects.filter(id=keyword_id)
	if 'update' in request.POST:
		keyword = request.POST['keyword']
		response = request.POST['response']
		response_type = request.POST['response_type']
		update.update(keyword=keyword, response=response, response_type=response_type)
	return render(request, 'update_keyword.html',locals())

def delete_key_word(request, id):
	keyword_id = request.GET['id']
	delete = Keyword.objects.filter(id=keyword_id)
	delete.delete()
	return render(request,"delete_keyword.html",locals())




