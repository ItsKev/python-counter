#!/bin/bash

kind create cluster --config configs/kind-config.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

linkerd install | kubectl apply -f -
linkerd viz install | kubectl apply -f -
linkerd jaeger install | kubectl apply -f -

kubectl create -f k8s/redis-namespace.yaml
helm install redis --namespace redis bitnami/redis --values configs/redis-values.yaml

helm install prometheus-adapter prometheus-community/prometheus-adapter --namespace linkerd-viz --values configs/prometheus-adapter.values.yaml