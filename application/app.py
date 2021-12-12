import logging
import requests
import random
import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry.exporter.opencensus.trace_exporter import (
    OpenCensusSpanExporter,
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

trace.set_tracer_provider(TracerProvider(resource=Resource.create({"service.name": "python-counter-application"})))
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(ConsoleSpanExporter())
)
trace.get_tracer_provider().add_span_processor(
    BatchSpanProcessor(OpenCensusSpanExporter(endpoint="collector.linkerd-jaeger:55678"))
)

RequestsInstrumentor().instrument()

while True:
    random_number = random.randint(1, 50)

    response = requests.post(
        f"http://python-counter-backend.default.svc.cluster.local:8080/increase/{random_number}")

    if response.ok:
        logging.info(f"Succesfully increased the counter by {random_number}")
        value = response.json()["counter"]
        logging.info(f"New counter value is {value}")
    else:
        logging.error(response.status_code)
        logging.error(response.text)

    time.sleep(random.randint(1, 5))
