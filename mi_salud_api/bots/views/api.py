from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from bots.models import Bot


def tag_message(request, id_model):
    bot = get_object_or_404(Bot, id=int(id_model))
    return JsonResponse({})


def record_response_tag(request, id_model, id_message):
    bot = get_object_or_404(Bot, id=int(id_model))

    return JsonResponse({})
