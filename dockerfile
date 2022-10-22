FROM python:3.9

COPY ./ /app/
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE  8080

CMD ["python", "app.py"]