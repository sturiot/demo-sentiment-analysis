#!/bin/sh

sudo curl -X POST http://localhost:8080/seldon/seldon-kedro/sentiment_analysis/api/v1.0/predictions \
    -H 'Content-Type: application/json' \
    -d '{"strData": "{\"ft_1\":3, \"ft_2\":5}"}'

echo
