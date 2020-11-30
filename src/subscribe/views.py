import json
import re

import django_rq

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models                import Subscribe
from utils  import send_email, authorization
        

class SubscribeView(View):       
    def post(self, request, *args, **kwargs):
        try:
            data  = json.loads(request.body)
            email = data['email']
            name  = data['name']
            
            if re.findall('[@.]', email) != ['@', '.']: #email 형식 validation
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
           
            if Subscribe.objects.filter(email = email).exists(): #DB에 email 등록 여부 확인
                subscribe = Subscribe.objects.get(email = email)
                
                if subscribe.is_subscribe == True: #이미 구독중
                    my_data = {
                        'message':'Ths email is already subscriber',
                        "error" : {
                                        "email" : email
                                    }
                    }           
                    return JsonResponse({'myData':my_data}, status=409)
                
                else: #DB에는 있지만 구독자가 아닌 email 구독자로 변경
                    subscribe.is_subscribe = True
                    subscribe.save()
            
            else: #DB에 없는 새로운 구독자 생성
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
            
            if re.findall('[@.]', email) != ['@', '.']: #email 형식 validation
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
            
            if not Subscribe.objects.filter(email = email).exists(): #DB에 email 존재 하지 않음
                my_data = {
                    'message':'Email is not existed',
                    "error" : {
                                    "email" : email
                                }
                }           
                return JsonResponse({'myData':my_data}, status=404)
            
            # 구독 취소로 변경
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
        try:
            if not kwargs: #데이터 전체 삭제
                Subscribe.objects.all().delete()
            
            else: #특정 데이터 삭제
                subscribe_id = kwargs['subscribe_id']
                subscribe = Subscribe.objects.get(id = subscribe_id).delete()
                          
            my_data = {
                        'message':'No contents',
                    }           
            return JsonResponse({'myData':my_data}, status=204)
        
        except ObjectDoesNotExist:
            my_data = {
                    'message':'Not found',
                    "error" : {
                                    "id"    : subscribe_id,
                                }
                }
            return JsonResponse({'myData':my_data}, status=404)
    
    @authorization
    def get(self, request, *args, **kwargs):
        if not kwargs:
            subscribes = Subscribe.objects.all()
            my_data = {
                'message':'Success subscribe',
                'count'  : subscribes.count(),
                "result" : [{
                                "id"           : subscribe.id,
                                "email"        : subscribe.email,
                                "name"         : subscribe.name,
                                "is_subscribe" : subscribe.is_subscribe,
                                "create_at"    : subscribe.created_at,
                                "update_at"    : subscribe.updated_at
                            } for subscribe in subscribes]
            }  
        else:
            subscribe_id = kwargs['subscribe_id']
            subscribe = Subscribe.objects.get(id = subscribe_id)
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
        return JsonResponse({'myData': my_data}, status=200)

class SendEmailToSubscribe(View):
    def post(self, request, *args, **kwargs):
        try:
            data            = json.loads(request.body)
            subject         = data['subject']
            content         = data['content']
            subscriber_list = Subscribe.objects.filter(is_subscribe=True)
          
            q = django_rq.get_queue('default')
            q.empty()
            q.enqueue(send_email, subscriber_list, subject, content, result_ttl=30)
            
            my_data = {
                    'message':'Accepted',
            }           
            return JsonResponse({'myData': my_data}, status=203)
        
        except KeyError as error:
            my_data = {
                    'message': 'Key error',
                    'error'  : {
                                    "key" : str(error)
                                }
                }
            return JsonResponse({'myData': my_data}, status=400)
    