import json
import re

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models                import Subscribe

class SubscribeView(View):
    def get(self, request):
        return JsonResponse({'message':'pong'}, status= 200)
    
    def post(self, request):
        try:
            data  = json.loads(request.body)
            
            email = data['email']
            name  = data['name']
           
            if Subscribe.objects.filter(email = email).exists():
                my_data = {
                    'message':'Email is already existed',
                    "result" : {
                                    "email" : email
                                }
                }           
                
                return JsonResponse({'myData':my_data}, status=409)
            
            if re.findall('[@.]', email) != ['@', '.']:
                return JsonResponse({'message':'NOT INCLUDE @ or . '}, status= 400)
           
            subscribe = Subscribe.objects.create(
                            email = email,
                            name = name
                        )  
            my_data = {
                    'message':'Success subscribe',
                    "result" : {
                                    "id"    : subscribe.id,
                                    "email" : subscribe.email,
                                    "name"  : subscribe.name,
                                }
                }           
            return JsonResponse({'myData': my_data}, status=201)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
    
    def patch(self, request):
        pass

    def delete(self, request):
        pass

        