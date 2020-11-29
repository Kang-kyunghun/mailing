import json
import re
import requests

from django.views           import View
from django.http            import JsonResponse
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .models                import Subscribe

class SubscribeView(View):
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message':'pong'}, status= 200)
    
    #구독자 생성
    def post(self, request, *args, **kwargs):
        try:
            data  = json.loads(request.body)
            email = data['email']
            name  = data['name']
            
            #email 형식 validation
            if re.findall('[@.]', email) != ['@', '.']:
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
           
            #DB에 email 등록 여부 확인
            if Subscribe.objects.filter(email = email).exists():
                subscribe = Subscribe.objects.get(email = email)
                #이미 구독중
                if subscribe.is_subscribe == True:
                    my_data = {
                        'message':'Ths email is already subscriber',
                        "error" : {
                                        "email" : email
                                    }
                    }           
                    return JsonResponse({'myData':my_data}, status=409)
                #DB에는 있지만 구독자가 아닌 email 구독자로 변경
                else:
                    subscribe.is_subscribe = True
                    subscribe.save()
            #DB에 없는 새로운 구독자 생성
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
    
    #구독 취소 but DB에 데이터는 남김
    def patch(self, request, *args, **kwargs):
        try:
            data         = json.loads(request.body)
            email        = data['email']
            
            #email 형식 validation
            if re.findall('[@.]', email) != ['@', '.']:
                my_data = {
                    'message':'Not include "@" or "." at email',
                    "error" : {
                                    "email" : email,
                                }
                }           
                return JsonResponse({'myData': my_data}, status=400)
            
            #DB에 email 존재 하지 않음
            if not Subscribe.objects.filter(email = email).exists():
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

    #DB에서 데이터 삭제
    def delete(self, request, *args, **kwargs):
        #데이터 전체 삭제
        try:
            if not kwargs:
                Subscribe.objects.all().delete()
            
            #특정 데이터 삭제
            else:
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

class SendEmailToSubscribe(View):
    def send_email(subscriber_list, subject, content):
        URL     = 'http://python.recruit.herrencorp.com/api/v1/mail'
        headers = {
                "Authorization" : "herren-recruit-python",
                "content_type"  : "application/x-www-form-urlencoded"
        }
        for subscribe in subscriber_list:
            formbody =  {
                    "mailto"  : subscribe.email,
                    "subject" : subject,
                    "content" : content
            }
        response = requests.post(URL, headers=headers, data=formbody)
        
    def get(self, request, *args, **kwargs):
        return JsonResponse({'message':'pong'}, status= 200)
    
    #구독자 생성
    def post(self, request, *args, **kwargs):
        try:
            data            = json.loads(request.body)
            subject         = data['subject']
            content         = data['content']
            subscriber_list = Subscribe.objects.filter(is_subscribe=True)

            send_email(subscriber_list, subject, content)
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
    