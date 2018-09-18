from django.urls import path
from .views.api import record_response_tag, tag_message_with_model


urlpatterns = [
    path('tag-new-message/bot/<int:id_model>/', tag_message_with_model),
    path('model-is-in-traning/bot/<int:id_model>/', tag_message_with_model)
]
