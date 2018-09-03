from datetime import datetime
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bots.models import Bot, HistoricalMessage
from bots.ml_model.pre_rules import procesa_reglas


@csrf_exempt
def tag_message(request, id_model):
    bot = get_object_or_404(Bot, id=int(id_model))
    message = request.POST.get('message', 'Buenas tardes quiero saber algo sobre mi salud!')
    flow = request.POST.get('flow_id')
    id_message = request.POST.get('id_message')
    id_rp_user = request.POST.get('id_rp_user')

    category = procesa_reglas(message)
    if category['result'] == 'modelo':
        message_record = HistoricalMessage(
            message=message,
            message_date=datetime.now(),
            flow=flow,
            model_tag=category['result'],
            id_message=id_message,
            id_rp_user=id_rp_user,
            id_bot=bot.id
        )

        message_record.save()

    return JsonResponse({'category': category['result']})


@csrf_exempt
def record_response_tag(request, id_model, id_message):
    bot = get_object_or_404(Bot, id=int(id_model))
    id_message_response = request.POST.get('id_message_response')
    user_tag = request.POST.get('user_tag')

    message_record = get_object_or_404(HistoricalMessage, id_message=id_message)
    message_record.id_message_response = id_message_response
    message_record.user_tag = user_tag

    message_record.save()

    return JsonResponse({'status': 'ok'})
