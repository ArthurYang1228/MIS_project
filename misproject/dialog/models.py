# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


head_img = models.ImageField(u'圖片',upload_to='images')


class Member(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, null=True)
    gender = models.CharField(max_length=2, null=True)
    email = models.EmailField(max_length=100, null=True, default=' ')
    password = models.CharField(max_length=50, null=True)
    birthday = models.DateField(null=True)
    playerid = models.CharField(max_length=500, null=True, default=' ')


    def __str__(self):
        return self.name

class Dialog(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('Member')
    who = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False, default=' ')
    from_key = models.ForeignKey('Keyword', null=True, default=None, blank=True)




class Keyword(models.Model):
    id = models.AutoField(primary_key=True)
    text = 1
    choice = 2
    picture = 3
    function = 4
    response_type_choices = (
        (text, 'TEXT'),
        (choice, 'CHOICE'),
        (picture, 'PICTURE'),
        (function, 'FUNCTION'))
    key = models.CharField(max_length=20)
    response = models.CharField(max_length=100)
    response_type = models.IntegerField(choices=response_type_choices, default=text)
    created_at = models.DateTimeField(auto_now_add=True)
    father_key = models.ForeignKey('self', default=None, null=True, blank=True)

    def __str__(self):
        return self.key

class Symptom(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100,blank=True)
    name_English = models.CharField(max_length=600,blank=True)
    division = models.CharField(max_length=600,blank=True)
    organ = models.CharField(max_length=600,blank=True)
    symptom = models.CharField(max_length=600,blank=True)
    introduction = models.TextField(blank=True)
    prevention = models.CharField(max_length=600,blank=True)

    level = models.CharField(max_length=20, choices=(
        ('0', '沒毛病吧'),
        ('1', '蠻常見的'),
        ('2', '還算聽過'),
        ('3', '什麼鬼啦')),
        default='2')

    def __str__(self):
        return self.name




