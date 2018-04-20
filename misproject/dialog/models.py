# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models





class Member(models.Model):
    name = models.CharField(max_length=20, null=False)
    gender = models.CharField(max_length=2, null=False)
    email = models.EmailField(max_length=100, null=False, default=' ')
    password = models.CharField(max_length=50, null=False)
    birthday = models.DateField(null=False)


    def __str__(self):
        return self.name

class Dialog(models.Model):
    member = models.ForeignKey('Member')
    who = models.BooleanField(default=True)
    time = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=100, null=False, default=' ')




class Keyword(models.Model):
    text = 1
    choice = 2
    picture = 3
    response_type_choices = (
        (text, 'TEXT'),
        (choice, 'CHOICE'),
        (picture, 'PICTURE'))
    keyword = models.CharField(max_length=20)
    response = models.CharField(max_length=100)
    response_type = models.IntegerField(max_length=5, choices=response_type_choices, default=text)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.keyword




