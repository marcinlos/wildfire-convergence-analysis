#!/usr/bin/env bash

rm -f data/*
mkdir -p data

for file in data-raw/*; do
    name="${file#*/}"
    awk -F ' +' -f process-data.awk "${file}" > "data/${name}"
done
