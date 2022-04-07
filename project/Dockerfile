FROM python:3.8
LABEL maintainer="Jagadeesh.K"

COPY . /techtrends
WORKDIR /techtrends

RUN pip install -r ./project/techtrends/requirements.txt
RUN python ./project/techtrends/init_db.py

EXPOSE 3111

CMD ["python", "./techtrends/app.py"]
