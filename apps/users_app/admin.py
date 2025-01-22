from django.contrib import admin

from .models import BotUser

@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    list_display = ('tg_id', 'username', 'fullname', 'phone', 'location', 'chat_lang', 'registered_at')
