from django.urls import path
from .views.api import model_is_in_training, tag_message_with_model, pre_rules_model


urlpatterns = [
    path('tag-new-message/bot/<int:id_model>/', tag_message_with_model),
    path('model-is-in-training/bot/<int:id_model>/', model_is_in_training),
    path('pre-model-rules/bot/<int:id_model>/', pre_rules_model)
]
