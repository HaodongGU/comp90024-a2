FROM python:3.8

COPY requirements.txt /app/
COPY Mastodon_Harvester.py /app/
COPY mastodon_toots_processing.py /app/

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python", "Mastodon_Harvester.py"]
