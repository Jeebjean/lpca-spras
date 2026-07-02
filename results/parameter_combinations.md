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
