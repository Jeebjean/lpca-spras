import pandas as pd
import os

results = []

dirs = [
    ("PathLinker", 5,  "data/spras_output_egfr_pathlinker_5"),
    ("PathLinker", 10, "data/spras_output_egfr_pathlinker_10"),
    ("PathLinker", 25, "data/spras_output_egfr_pathlinker_25"),
    ("PathLinker", 50, "data/spras_output_egfr_pathlinker_50"),
    ("OI1", 5,  "data/spras_output_egfr_oi1_5"),
    ("OI1", 10, "data/spras_output_egfr_oi1_10"),
    ("OI1", 25, "data/spras_output_egfr_oi1_25"),
    ("OI1", 54, "data/spras_output_egfr_oi1_54"),
    ("OI2", 5,  "data/spras_output_egfr_oi2_5"),
    ("OI2", 10, "data/spras_output_egfr_oi2_10"),
    ("OI2", 25, "data/spras_output_egfr_oi2_25"),
    ("OI2", 50, "data/spras_output_egfr_oi2_50"),
]

for algo, n_combos, path in dirs:
    cv_file = os.path.join(path, "cv_result.csv")
    matrix_file = os.path.join(path, "binary_matrix.csv")
    if os.path.exists(cv_file) and os.path.exists(matrix_file):
        m = pd.read_csv(cv_file)['best_m'][0]
        matrix = pd.read_csv(matrix_file, index_col=0)
        total_cells = matrix.shape[0] * matrix.shape[1]
        n_zeros = (matrix == 0).sum().sum()
        sparsity = round(n_zeros / total_cells * 100, 2)
        results.append({
            "Algorithm": algo,
            "Combinations": n_combos,
            "Matrix rows (edges)": matrix.shape[0],
            "Matrix cols (runs)": matrix.shape[1],
            "Best m": int(m),
            "Sparsity (% zeros)": sparsity
        })

df = pd.DataFrame(results)
print(df.to_string(index=False))
df.to_csv("data/summary_all_combos.csv", index=False)
print("\nSaved to data/summary_all_combos.csv")