import json
import requests
import re
from django.http            import JsonResponse

def send_email(subscriber_list, subject, content):
        
        
        for subscribe in subscriber_list:
            formbody =  {
                    "mailto"  : subscribe.email,
                    "subject" : subject,
                    "content" : content
            }
            
            p_google = re.compile('@google.com')
            p_naver = re.compile('@naver.com')
            
            #mailing version2
            if p_google.search(subscribe.email) or p_naver.search(subscribe.email):
                URL     = 'http://python.recruit.herrencorp.com/api/v2/mail'
                headers = {
                        "Authorization" : "herren-recruit-python",
                        "content_type"  : "application/json"
                }
                response = requests.post(URL, headers=headers, data=json.dumps(formbody))
            
            #mailing version1
            else:
        
                URL     = 'http://python.recruit.herrencorp.com/api/v1/mail'
                headers = {
                        "Authorization" : "herren-recruit-python",
                        "content_type"  : "application/x-www-form-urlencoded"
                }
                response = requests.post(URL, headers=headers, data=formbody)

def authorization(func):
    def wrapper(self, request, *args, **kwargs):
        if not request.headers.get('Authorization'): 
            return JsonResponse({'myData':{'message':'NO_TOKEN'}}, status=403)
        
        token = request.headers['Authorization']
        if token == 'herren-recruit-python':
            return func(self, request, *args, **kwargs)
        else:
            return JsonResponse({'myData':{'message':'INVALID_TOKEN'}}, status=403)       
    return wrapper