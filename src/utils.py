import requests

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