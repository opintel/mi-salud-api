from datetime import datetime
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from bots.models import Bot, HistoricalMessage
from bots.ml_model.script_reglas import procesa_reglas
from bots.ml_model.model import predice_modelo


@csrf_exempt
def tag_message(request, id_model):
    """
    Endpoint: /opi/tag-new-message/bot/<int:id_model>/
    GET:
    - flow_id
    - id_rp_user
    """

    bot = get_object_or_404(Bot, id=int(id_model))

    id_rp_user = request.GET.get('id_rp_user')
    user_tag = request.GET.get('user_tag')
    message = request.GET.get('message')

    # messages = query_rp_api(id_rp_user)
    category = procesa_reglas(message)
    print(category)
    if category['result'] == 'modelo':
        print("Entro a modelo")
        print(settings.RP_TOKEN)
        category = predice_modelo(id_rp_user, message, settings.RP_TOKEN)

    message_record = HistoricalMessage(
        message=message,
        message_date=datetime.now(),
        flow="mi salud",
        model_tag='',
        id_message="id",
        id_rp_user=id_rp_user,
        id_bot=bot.id,
        user_tag=user_tag
    )

    message_record.save()
    print(category)

    return JsonResponse({'category': category['pred']})


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


def query_rp_api(id_user):
    import requests

    endpoint_url = settings.RP_API_URL+'/api/v2/messages.json?contact=%s&top=True'%(id_user)
    token = 'token %s' % settings.RP_TOKEN

    headers = {'content-type': 'application/json', 'Authorization': token}
    response = requests.get(endpoint_url, headers = headers)
    results = response.json()['results']

    return results