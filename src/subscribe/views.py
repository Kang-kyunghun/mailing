import json
import re

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models                import Subscribe

class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message':'pong'}, status= 200)
    
    def post(self, request, *args, **kwargs):
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
            my_data = {
                    'message': 'Key error',
                }
            return JsonResponse({'myData': my_data}, status=400)
    
    def patch(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        #데이터 전체 삭제
        try:
            if not kwargs:
                Subscribe.objects.all().delete()
                my_data = {
                        'message':'No contents',
                    }           
                return JsonResponse({'myData':my_data}, status=204)
            #특정 데이터 삭제
            else:
                subscribe_id = kwargs['subscribe_id']
                subscribe = Subscribe.objects.get(id = subscribe_id)
                my_data = {
                    'message':'No content',
                    "result" : {
                                    "id"    : subscribe.id,
                                    "email" : subscribe.email,
                                    "name"  : subscribe.name,
                                }
                }
                subscribe.delete()          
            return JsonResponse({'myData': my_data}, status=204)
        
        except KeyError:
            my_data = {
                    'message': 'Key error',
                }
            return JsonResponse({'myData': my_data}, status=400)
        
        except ObjectDoesNotExist:
            my_data = {
                    'message':'Not found',
                    "result" : {
                                    "id"    : subscribe_id,
                                }
                }
            return JsonResponse({'myData':my_data}, status=404)



        