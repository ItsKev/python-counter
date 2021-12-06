# Python counter PoC

## Architecture
![Python Counter](architecture/python-counter.svg)


## Query
irate(request_total{namespace="default", deployment="python-counter-backend", direction="inbound", target_port="8080"}[30s])