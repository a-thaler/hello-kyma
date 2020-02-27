import os
import json
import requests
from flask import Flask, request
from redis import Redis

app = Flask(__name__)

if os.environ.get('AZ_host'):
    redisClient = Redis(ssl=True, host=os.environ.get('AZ_host'), port=os.environ.get('AZ_port'), password=os.environ.get('AZ_password'))


@app.route("/")
def hello():
    return "Hello Kyma!"

@app.route("/events", methods=['POST'])
def events():
    print("Received request " + request.data.decode('UTF-8'))

    orderCode = request.json["orderCode"]
    print("Received event with orderCode " + orderCode)

    if os.environ.get('AZ_host'):
        response = requests.get(os.environ.get('GATEWAY_URL') + "/webshop/orders/" + orderCode)
        print("Received from '" + os.environ.get('GATEWAY_URL') + "' the response '"+ response.text + "'")

        redisClient.set("order", response.text)
        print("Data stored in Redis")

    return ""


if __name__ == "__main__":
    app.run(host='0.0.0.0')
