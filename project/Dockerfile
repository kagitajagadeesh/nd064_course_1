FROM python:3.8
LABEL maintainer="Jagadeesh.K"

COPY . /project/techtrends
WORKDIR /techtrends

RUN pip install -r ./techtrends/requirements.txt
RUN python3 ./techtrends/init_db.py

EXPOSE 3111

CMD ["python", "app.py"]
