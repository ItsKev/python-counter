#!/bin/bash

cd ../application
docker build -t python-counter-application:0.1.0 .

cd ../backend
docker build -t python-counter-backend:0.1.0 .

kind load docker-image python-counter-application:0.1.0 python-counter-backend:0.1.0

cd ../infrastructure
kubectl apply -f ./k8s