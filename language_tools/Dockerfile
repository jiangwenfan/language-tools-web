FROM python:3.11.2-buster


WORKDIR /language_tools
COPY ./requirements.txt /language_tools/requirements.txt
RUN pip install --upgrade pip

# RUN pip install -r requirements.txt -i https://mirrors.cloud.tencent.com/pypi/simple
RUN pip install -r requirements.txt

WORKDIR /language_tools
COPY . /language_tools


CMD ["/bin/sh", "start.sh"]