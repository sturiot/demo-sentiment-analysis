#!/bin/sh

sudo kubectl create namespace seldon-kedro

sudo kubectl apply -f - << END

apiVersion: machinelearning.seldon.io/v1alpha2
kind: SeldonDeployment
metadata:
  name: sentiment-analysis
  namespace: seldon-kedro
spec:
  name: sentiment-analysis-deployment
  predictors:
  - componentSpecs:
    - spec:
        containers:
        - name: sentiment-analysis-pipeline-predict
          image: sturiot/sturiotio:sentiment-analysis-v1.0.1
    graph:
      children: []
      endpoint:
        type: REST
      name: sentiment-analysis-pipeline-predict
      type: MODEL
    name: sentiment-analysis-pipeline-predictor
    replicas: 1

END
