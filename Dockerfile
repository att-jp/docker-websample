FROM alpine:3.7
MAINTAINER Shingo Kawano <shingo.ms@55mp.com>
ARG arg=0

RUN apk update && apk add \
  python2-dev \
  py2-pip \
  git \
  tzdata \
  curl

COPY *.py ./
COPY *.sh ./
COPY statics ./statics
COPY templates ./templates
COPY requirements.txt ./

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

USER nobody
ENV TZ Asia/Tokyo

CMD ["./entry.sh"]
