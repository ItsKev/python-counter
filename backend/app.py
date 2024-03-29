import logging
from redis import Redis
from flask import (Flask, request)
from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.opencensus.trace_exporter import (
    OpenCensusSpanExporter,
)
from opentelemetry.propagate import set_global_textmap
from opentelemetry.propagators.b3 import B3MultiFormat

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "python-counter-backend"})))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OpenCensusSpanExporter(endpoint="collector.linkerd-jaeger:55678"))
)
set_global_textmap(B3MultiFormat())

app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
redis = Redis(host="redis-master.redis.svc.cluster.local", port=6379)


@app.route("/increase/<amount>", methods=["POST"])
def increase_counter(amount):
    print(dict(request.headers))
    result = redis.incr(name="tmp", amount=amount)
    return "{\"counter\": " + str(result) + "}"


if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)
