#!/bin/bash

kind create cluster --config configs/kind-config.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo update

helm install redis --namespace redis --create-namespace bitnami/redis --values configs/redis-values.yaml

linkerd install | kubectl apply -f -
linkerd viz install | kubectl apply -f -

helm install prometheus-adapter prometheus-community/prometheus-adapter --namespace linkerd-viz --values configs/prometheus-adapter.values.yaml