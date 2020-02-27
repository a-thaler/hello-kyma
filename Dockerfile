FROM python:3.7

RUN mkdir /app
WORKDIR /app
COPY app /app/
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["python", "-u", "/app/main.py"]