FROM python:3.8
LABEL maintainer="Jagadeesh.K"

COPY . /app
WORKDIR /app

RUN pip install -r ./project/techtrends/requirements.txt
RUN python3 ./project/techtrends/init_db.py

EXPOSE 3111

CMD ["python", "./project/techtrends/app.py"]
