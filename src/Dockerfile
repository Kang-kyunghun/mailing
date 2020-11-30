FROM python:3.8

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

## THE LIFE SAVER
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.2.1/wait /wait
RUN chmod +x /wait

## Launch the wait tool and then your application
CMD /wait 



