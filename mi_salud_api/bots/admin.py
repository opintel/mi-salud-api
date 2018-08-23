from django.contrib import admin
from .models import Bot, HistoricalMessage
from .form import BotForm


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    model = Bot
    form = BotForm
    search_fields = ('name', 'creation_date',)
    list_filter = ('enable',)
    list_display = ('name', 'enable', 'creation_date',)


@admin.register(HistoricalMessage)
class HistoricalMessageAdmin(admin.ModelAdmin):
    model = HistoricalMessage
    search_fields = ('id_message', 'id_rp_user', 'id_bot',)
    list_filter = ('id_bot',)
    list_display = ('id_message', 'id_rp_user', 'id_bot', 'message_date')
