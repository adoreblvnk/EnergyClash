FROM python:3.9.13-buster  

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# add your dependencies here!
RUN apt-get update 

COPY . .

EXPOSE 5000

CMD ["python3", "app.py"]
