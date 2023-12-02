FROM python:3.9.18-alpine3.18

WORKDIR /app

COPY requirements.txt .
COPY main.py .

RUN pip install -r requirements.txt

CMD ["python", "-u", "main.py"]

