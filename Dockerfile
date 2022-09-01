FROM python:3.9.13-buster  

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# add your dependencies here!
RUN apt-get update 

# tesseract
RUN apt-get install -y tesseract-ocr

# sqlite3
RUN apt-get install -y sqlite3

# library for opencv
RUN apt-get install -y python3-opencv

COPY . .

# initialise database
RUN sqlite3 database/energyclash.db < database/energyclash.sql

EXPOSE 33507

CMD ["python3", "app.py"]
