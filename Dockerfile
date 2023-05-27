FROM python:3.9
RUN ln -sf /usr/share/zoneinfo/Asia/Kolkata /etc/localtime
#RUN apt update -y
#RUN apt install python3-pip -y
RUN mkdir /app
RUN mkdir /logs
WORKDIR /app
COPY . /app
RUN pip install -r requirement.txt
ENTRYPOINT ["python3","main.py"]