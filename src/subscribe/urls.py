from django.urls import path

from .views import SubscribeView

urlpatterns = [
        path('', SubscribeView.as_view()),
        path('/<int:subscribe_id>', SubscribeView.as_view()),
]