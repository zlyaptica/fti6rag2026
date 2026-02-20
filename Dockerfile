FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY run.py config.py /app/
COPY src/ /app/src/

CMD ["python", "run.py"]
