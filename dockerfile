FROM python:3.11-slim

WORKDIR /app

COPY gs.py .

RUN pip install requests

ENTRYPOINT ["python", "gs.py"]

CMD []
