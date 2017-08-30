FROM python:3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /worktask
 WORKDIR /worktask
 ADD requirements.txt /worktask/
 ADD mydata.json /worktask/
 ADD . /worktask/
