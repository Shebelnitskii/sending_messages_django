from django.contrib import admin
from .models import Client, Mailing, Message


# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'surname', 'email', 'comment')
    list_filter = ('email',)
    search_fields = ('first_name', 'email')


admin.site.register(Client, ClientAdmin)


class MailingAdmin(admin.ModelAdmin):
    list_display = ('message', 'mailing_time', 'periodicity', 'mailing_status')
    list_filter = ('message',)
    search_fields = ('periodicity', 'mailing_status')




admin.site.register(Mailing, MailingAdmin)

class MessageAdmin(admin.ModelAdmin):
    list_display = ('client', 'letter_subject', 'letter_body')
    list_filter = ('client',)

admin.site.register(Message, MessageAdmin)