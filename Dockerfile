FROM python:3.11.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "src/main.py"]