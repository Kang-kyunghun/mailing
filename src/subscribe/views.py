import json
import re

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models                import Subscribe

class SubscribeView(View):
    def get(self, request):
        return JsonResponse({'message':'pong'}, status= 200)

        