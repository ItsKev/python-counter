import logging
from redis import Redis
from flask import Flask


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)
redis = Redis(host="host.docker.internal", port=6379)


@app.route("/increase/<amount>", methods=["POST"])
def increase_counter(amount):
    result = redis.incr(name="tmp", amount=amount)
    return "{\"counter\": " + str(result) + "}"


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
