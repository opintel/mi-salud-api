from django.contrib import admin
from .models import Bot, HistoricalMessage, Category
from .form import BotForm


class CategoryInlineForm(admin.TabularInline):
    model = Bot.categories.through


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category
    search_fields = ('name',)
    list_display = ('name',)


@admin.register(Bot)
class BotAdmin(admin.ModelAdmin):
    model = Bot
    form = BotForm
    search_fields = ('name', 'creation_date',)
    list_filter = ('enable',)
    list_display = ('name', 'enable', 'creation_date',)
    inlines = [
        CategoryInlineForm
    ]


@admin.register(HistoricalMessage)
class HistoricalMessageAdmin(admin.ModelAdmin):
    model = HistoricalMessage
    search_fields = ('id_message', 'id_rp_user', 'id_bot',)
    list_filter = ('id_bot',)
    list_display = ('id_message', 'id_rp_user', 'id_bot', 'message_date', 'model_tag', 'user_tag', 'message')
