FROM python:3.11.5

WORKDIR /home
COPY requirements.txt ./

#RUN pip install --upgrade pip 
RUN pip install --upgrade pip -r requirements.txt