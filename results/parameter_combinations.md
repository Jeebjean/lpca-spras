# Parameter Combinations Tested

## EGFR Dataset

### PathLinker
| Combo level | Parameter | Values |
|---|---|---|
| 5 | k | [10, 30, 50, 70, 90] |
| 10 | k | range(10, 110, 10) |
| 25 | k | range(10, 510, 20) |
| 50 | k | range(10, 1010, 20) |

### OmicsIntegrator1
| Combo level | b | w | d | g | r | mu | dummy_mode |
|---|---|---|---|---|---|---|---|
| 5 | [0.55, 2.5, 5, 7.5, 10] | 0.5 | 10 | 0.001 | 0.01 | 0.008 | file |
| 10 | [0.55, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 10] | 0.5 | 10 | 0.001 | 0.01 | 0.008 | file |
| 25 | 25 values from 0.55 to 7.25 | 0.5 | 10 | 0.001 | 0.01 | 0.008 | file |
| 54 | b: [0.55, 2, 4, 6, 8, 10] x w: linspace(0, 5, 9) | - | 10 | 0.001 | 0.01 | 0.008 | file |

### OmicsIntegrator2
| Combo level | b | g |
|---|---|---|
| 5 | [0.5, 1, 1.5, 2, 2.5] | 0 |
| 10 | [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5] | 0 |
| 25 | linspace(0.2, 5, 25) | 0 |
| 50 | b: linspace(0.2, 5, 10) x g: linspace(0, 0.5, 5) | - |

## Supplement Parameter Combinations (EGFR Dataset)

Parameters from Table 15 of the SPRAS registered report supplement.
Before running each combo level, all previous algorithm outputs were deleted and Snakemake was rerun from scratch.

### PathLinker (17 runs total, 3 runs)
| Run | k values |
|---|---|
| run1 | [1, 10, 50, 100, 200] |
| run2 | [500, 1000, 5000, 20000] |
| run3 | range(200, 700, 50) = [200, 250, 300, 350, 400, 450, 500, 550, 600, 650] |

### OmicsIntegrator1 (18 runs total, 3 runs)
| Run | b | w | d | mu | g | r | dummy_mode |
|---|---|---|---|---|---|---|---|
| run1 | [1, 5] | [0.5, 1, 5] | 5 | 0.0001 | 0.001 | 0.01 | file |
| run2 | [10, 15] | [0.5, 1, 5, 10] | 10 | 0.005 | 0.001 | 0.01 | file |
| run3 | [20] | [0.5, 1, 5, 10] | 15 | 0.01 | 0.001 | 0.01 | file |

### OmicsIntegrator2 (24 runs total, 3 runs)
| Run | b | g |
|---|---|---|
| run1 | [0.25, 0.75, 1] | [0, 1, 3] |
| run2 | [1, 5, 10] | [4, 5, 20] |
| run3 | [15] | [0, 1, 3, 4, 5, 20] |