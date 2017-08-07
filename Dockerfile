FROM python:3-alpine

RUN pip install requests
COPY upload_gh.py bin/

ENTRYPOINT ["bin/upload_gh.py"]
