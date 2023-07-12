FROM python:3.11
ENV PYTHONUNBUFFERED=1
WORKDIR /RESTAPI
COPY requirements.txt requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . /RESTAPI
EXPOSE 8000