#!/bin/bash

mkdir -p plots

plot() {
    file="$1"
    filename=$(basename "$file" .data)
    output_file="plots/${filename}.png"

    echo "$file -> $output_file"

    gnuplot <<- EOF
        set terminal pngcairo size 700,600 enhanced font 'Verdana,10'
        set output '$output_file'
        set autoscale fix
        set view map
        plot '$file' with image
EOF
}

export -f plot

parallel --jobs 0 plot ::: /results/*.data
