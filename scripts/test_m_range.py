# test_m_range.py
# For each dataset, test 6 fixed m values between 1 and 20, plus the CV best m

import docker
import pandas as pd
import os
from pathlib import Path

def get_m_range(best_m):
    fixed_values = [1, 4, 8, 12, 16, 20]
    m_values = sorted(set(fixed_values + [best_m]))
    return m_values

def run_lpca_fixed_m(input_file, output_file, k, m):
    client = docker.from_env()
    data_dir = str(Path(input_file).parent.absolute())
    command = [
        "Rscript", "/app/run_lpca.R",
        f"/data/{Path(input_file).name}",
        f"/data/{Path(output_file).name}",
        str(k),
        str(m)
    ]
    out = client.containers.run(
        "jeebjean/lpca",
        command,
        volumes=[f"{data_dir}:/data"],
        working_dir="/app",
        stderr=True
    )
    client.close()
    return out.decode("utf-8")

# All 12 datasets
datasets = [
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

for algo, n_combos, path in datasets:
    cv_file = os.path.join(path, "cv_result.csv")
    matrix_file = os.path.join(path, "binary_matrix.csv")

    if not os.path.exists(cv_file) or not os.path.exists(matrix_file):
        print(f"Skipping {algo} {n_combos}: missing files")
        continue

    best_m = int(pd.read_csv(cv_file)['best_m'][0])
    m_values = get_m_range(best_m)

    print(f"\n{'='*50}")
    print(f"{algo} - {n_combos} combos | CV best m={best_m} | Testing m={m_values}")
    print(f"{'='*50}")

    for m in m_values:
        output_file = os.path.join(path, f"lpca_scores_m{m}.csv")
        if os.path.exists(output_file):
            print(f"  m={m}: already exists, skipping")
            continue
        print(f"  Running m={m}...")
        out = run_lpca_fixed_m(matrix_file, output_file, k=2, m=m)
        print(f"  {out.strip()}")

print("\nAll done!")