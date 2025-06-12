FROM python:3.11-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir flask numpy opencv-python pyvirtualcam

EXPOSE 5000

CMD ["python", "main.py"]
