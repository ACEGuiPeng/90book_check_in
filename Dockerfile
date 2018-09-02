#python3 development environment
FROM registry.cn-hangzhou.aliyuncs.com/yiguo/ubuntu_python:v4
MAINTAINER pi "guipeng8789502@163.com"

WORKDIR /project/src

ADD ./src /project/src

RUN pip3 install -r requirements.txt

RUN /bin/cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

CMD ["python3.5", "90book_check_in.py"]