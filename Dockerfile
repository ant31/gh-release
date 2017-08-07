FROM python:3-alpine

RUN mkdir /code
WORKDIR /code
COPY . .
RUN pip install -e .

ENTRYPOINT ["ghrelease"]
