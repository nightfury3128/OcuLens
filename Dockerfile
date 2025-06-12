FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libgl1

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "main.py"]