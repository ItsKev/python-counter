#!/bin/bash

kind create cluster --config configs/kind-config.yaml

helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm install redis --namespace redis --create-namespace bitnami/redis --values configs/redis-values.yaml