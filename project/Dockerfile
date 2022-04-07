FROM python:3.8
LABEL maintainer="Jagadeesh.K"

COPY . /techtrends
WORKDIR /techtrends

RUN python -m pip install -r ./techtrends/requirements.txt
RUN python ./techtrends/init_db.py

EXPOSE 3111

CMD ["python", "./techtrends/app.py"]
