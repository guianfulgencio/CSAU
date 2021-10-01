FROM python:3.6

RUN pip install --upgrade pip
RUN pip install requests
RUN pip install netmiko
RUN pip install pyyaml
RUN pip install future
RUN pip install console-menu
RUN pip install prettytable
RUN pip install ciscoconfparse
ADD . /devnet

WORKDIR "/devnet/app"

