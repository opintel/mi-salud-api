from django.urls import path
from .views.api import record_response_tag, tag_message


urlpatterns = [
    path('tag-new-message/bot/<int:id_model>/', tag_message),
    path('record-response-tag/bot/<int:id_model>/message/<str:id_message>', record_response_tag)
]
