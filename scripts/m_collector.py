import pandas as pd
import os

results = []

dirs = [
    ("PathLinker", 5,  "data/combo_tests/spras_output_egfr_pathlinker_5", "cv"),
    ("PathLinker", 10, "data/combo_tests/spras_output_egfr_pathlinker_10", "cv"),
    ("PathLinker", 25, "data/combo_tests/spras_output_egfr_pathlinker_25", "cv"),
    ("PathLinker", 50, "data/combo_tests/spras_output_egfr_pathlinker_50", "cv"),
    ("OI1", 5,  "data/combo_tests/spras_output_egfr_oi1_5", "cv"),
    ("OI1", 10, "data/combo_tests/spras_output_egfr_oi1_10", "cv"),
    ("OI1", 25, "data/combo_tests/spras_output_egfr_oi1_25", "cv"),
    ("OI1", 54, "data/combo_tests/spras_output_egfr_oi1_54", "cv"),
    ("OI2", 5,  "data/combo_tests/spras_output_egfr_oi2_5", "cv"),
    ("OI2", 10, "data/combo_tests/spras_output_egfr_oi2_10", "cv"),
    ("OI2", 25, "data/combo_tests/spras_output_egfr_oi2_25", "cv"),
    ("OI2", 50, "data/combo_tests/spras_output_egfr_oi2_50", "cv"),
    ("PathLinker", "supplement (17)", "data/supplement/spras_output_egfr_pathlinker_supplement", "cv"),
    ("OI1", "supplement (18)", "data/supplement/spras_output_egfr_omicsintegrator1_supplement", "cv"),
    ("OI2", "supplement (24)", "data/supplement/spras_output_egfr_omicsintegrator2_supplement", "cv"),
]

for algo, n_combos, path, cv_subdir in dirs:
    cv_file = os.path.join(path, cv_subdir, "cv_result.csv")
    matrix_file = os.path.join(path, "binary_matrix.csv")

    # Try lpca_binary_matrix.csv for supplement folders
    if not os.path.exists(matrix_file):
        matrix_file = os.path.join(path, "lpca_binary_matrix.csv")

    if not os.path.exists(cv_file) or not os.path.exists(matrix_file):
        print(f"Skipping {algo} {n_combos}: missing files")
        print(f"  cv_file: {cv_file} exists: {os.path.exists(cv_file)}")
        print(f"  matrix_file: {matrix_file} exists: {os.path.exists(matrix_file)}")
        continue

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
df.to_csv("results/summary_all_combos.csv", index=False)
print("\nSaved!")