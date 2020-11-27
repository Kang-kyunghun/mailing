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
            
            if re.findall('[@.]', email) != ['@', '.']:
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
           
            if Subscribe.objects.filter(email = email).exists():
                subscribe = Subscribe.objects.get(email = email)
                if subscribe.is_subscribe == True:
                    my_data = {
                        'message':'Ths email is already subscriber',
                        "error" : {
                                        "email" : email
                                    }
                    }           
                    return JsonResponse({'myData':my_data}, status=409)
                else:
                    subscribe.is_subscribe = True
                    subscribe.save()
            else:
                subscribe = Subscribe.objects.create(
                                email = email,
                                name = name
                            )  
            my_data = {
                    'message':'Success subscribe',
                    "result" : {
                                    "id"           : subscribe.id,
                                    "email"        : subscribe.email,
                                    "name"         : subscribe.name,
                                    "is_subscribe" : subscribe.is_subscribe,
                                    "create_at"    : subscribe.created_at,
                                    "update_at"    : subscribe.updated_at
                                }
                }           
            return JsonResponse({'myData': my_data}, status=201)
        except KeyError as error:
            my_data = {
                    'message': 'Key error',
                    'error'  : {
                                    "key" : str(error)
                                }
                }
            return JsonResponse({'myData': my_data}, status=400)
    
    def patch(self, request, *args, **kwargs):
        try:
            data         = json.loads(request.body)
            email        = data['email']
           
            if not Subscribe.objects.filter(email = email).exists():
                my_data = {
                    'message':'Email is not existed',
                    "error" : {
                                    "email" : email
                                }
                }           
                return JsonResponse({'myData':my_data}, status=404)
            
            if re.findall('[@.]', email) != ['@', '.']:
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
           
            subscribe = Subscribe.objects.get(email = email)
            subscribe.is_subscribe = False
            subscribe.save()
            my_data = {
                    'message':'Success subscribe',
                    "result" : {
                                    "id"           : subscribe.id,
                                    "email"        : subscribe.email,
                                    "name"         : subscribe.name,
                                    "is_subscribe" : subscribe.is_subscribe,
                                    "create_at"    : subscribe.created_at,
                                    "update_at"    : subscribe.updated_at
                                }
                }           
            return JsonResponse({'myData': my_data}, status=201)
        except KeyError as error:
            my_data = {
                    'message': 'Key error',
                    'error'  : {
                                    "key" : str(error)
                                }
                }
            return JsonResponse({'myData': my_data}, status=400)

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
                    'message':f'Data(email{subscribe.email}) is deleted',
                    "error" : {
                                    "id"    : subscribe.id,
                                    "email" : subscribe.email,
                                    "name"  : subscribe.name,
                                    "create_at" : subscribe.created_at,
                                    "update_at" : 000#datetime.now 
                                }
                }
                subscribe.delete()          
            return JsonResponse({'myData': my_data}, status=200)
        
        except ObjectDoesNotExist:
            my_data = {
                    'message':'Not found',
                    "error" : {
                                    "id"    : subscribe_id,
                                }
                }
            return JsonResponse({'myData':my_data}, status=404)



        