FROM python:3.9-alpine

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app/app.py .
EXPOSE 5000
ENTRYPOINT ["python", "app.py"]