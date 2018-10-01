from datetime import datetime
from django.shortcuts import get_object_or_404, render
from bots.models import Bot
from bots.ml_model.entrena_modelo import train_model


def train(request, id_model=None):
    """
    /opi/bot/<int:id_model>/train/

    Vista que entrena el modelo en cuestion
    y versiona el modelo
    """
    bot = get_object_or_404(Bot, id=id_model)
    version = datetime.now().strftime('%Y%m%d')

    if request.METHOD == 'POST':
        try:
            current_version = train_model(id_model, version)
            bot.current_version = current_version
            bot.save()
        except Exception as error:
            return render(request, 'train.html', {'bot': bot, 'error': error})
        
        return JsonResponse({'model': bot.id, 'version': current_version})
    
    if request.METHOD == 'GET':
        return render(request, 'train.html', {'bot': bot})


