import logging
import requests
import random
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

while True:
    random_number = random.randint(1, 50)

    response = requests.post(f"http://python-counter-backend.default.svc.cluster.local:8080/increase/{random_number}")

    if response.ok:
        logging.info(f"Succesfully increased the counter by {random_number}")
        value = response.json()["counter"]
        logging.info(f"New counter value is {value}")
    else:
        logging.error(response.status_code)
        logging.error(response.text)

    time.sleep(random.randint(1, 5))
