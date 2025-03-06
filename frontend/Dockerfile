FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY fletapp.py .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir env

CMD ["flet", "run", "--web", "--port", "8080", "fletapp.py"]
