from django.contrib import admin
from dialog.models import Member, Dialog, Keyword





class MemberAdmin(admin.ModelAdmin):
    list_display=('id','name','gender','email','password','birthday')
    ordering = ('id',)

admin.site.register(Member,MemberAdmin)


class DialogAdmin(admin.ModelAdmin):
    list_display = ('member_name', 'time', 'content')

    def member_name(self, instance):
        return instance.member.name
admin.site.register(Dialog,DialogAdmin)

admin.site.register(Keyword)