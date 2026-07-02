# LPCA-SPRAS

Logistic PCA (LPCA) integration into the SPRAS bioinformatics pipeline.

## Overview

This repository contains the code and results for integrating LPCA into SPRAS as a new analysis method. LPCA projects binary edge x algorithm matrices into a lower-dimensional PC space, allowing visualization of edge robustness across parameter combinations.

## Structure
## Docker Image

The LPCA Docker image is based on `rocker/r-base` with the `logisticPCA` R package installed.

```bash
docker build -t jeebjean/lpca docker/
```

## Key Results

### Best m by algorithm and parameter combinations (EGFR dataset)

| Algorithm | Combos | Matrix (edges x runs) | Best m |
|---|---|---|---|
| PathLinker | 5-50 | 103-366 x 5-50 | 20 (always at max) |
| OI1 | 5 | 958 x 5 | 17 |
| OI1 | 10-54 | 1035-1238 x 10-54 | 6-7 |
| OI2 | 5-50 | 749-789 x 5-50 | 13-14 |

### Key observations

- OI1 with many parameter combinations shows clear separation of robust vs rare edges in PC space
- PathLinker produces a geometric artifact (parabola) due to the nested structure of its outputs
- OI2 does not show clear structure regardless of parameter combinations
- k=2 captures 74-99% of deviance explained depending on algorithm and number of combinations

## Supervisor

Tony Gitter, Gitter Lab, Morgridge Institute for Research / UW-Madison
