from django.urls import path

from .views import SubscribeView, SendEmailToSubscribe

urlpatterns = [
        path('', SubscribeView.as_view()),
        path('/<int:subscribe_id>', SubscribeView.as_view()),
        path('/send-mail', SendEmailToSubscribe.as_view()),
        path('/<int:subscribe_id>/send-mail', SendEmailToSubscribe.as_view())
]