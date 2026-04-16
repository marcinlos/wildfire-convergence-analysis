# Implicit wildfire convergence analysis

## Running the test

To execute convergence tests and collect the error data, run

```bash
./test-convergence.sh <path-to-fire-implicit>
```

Collected data is available in `data-raw/` directory.

## Generating convergence plots

To create convergence plots, run

```bash
./process-data.sh
uv run plots.py
```

The plots are stored in the `plots/` directory.

## Generatign output plots

To create plots from all the `*.data` files, run

```bash
./make-solution-plots.sh
```

This requires `gnuplot` and `parallel`:

```bash
sudo apt-get install gnuplot parallel
```
