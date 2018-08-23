from django.contrib import admin
from .models import Bot
from .form import BotForm


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    model = Bot
    form = BotForm
    search_fields = ('name', 'creation_date',)
    list_filter = ('enable',)
    list_display = ('name', 'enable', 'creation_date',)
