# generate_cv_curves.py
# Generate CV reconstruction error curves for all datasets

import docker
import pandas as pd
import os
from pathlib import Path

DATASETS = [
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

def run_cv(input_file, output_file, k):
    client = docker.from_env()
    data_dir = str(Path(input_file).parent.absolute())
    command = [
        "Rscript", "/app/run_cv.R",
        f"/data/{Path(input_file).name}",
        f"/data/{Path(output_file).name}",
        str(k)
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

if __name__ == "__main__":
    for algo, n_combos, path in DATASETS:
        matrix_file = os.path.join(path, "binary_matrix.csv")
        cv_file = os.path.join(path, "cv_result.csv")
        cv_curve_file = os.path.join(path, "cv_result_curve.csv")

        if not os.path.exists(matrix_file):
            print(f"Skipping {algo} {n_combos}: missing matrix")
            continue

        if os.path.exists(cv_curve_file):
            print(f"{algo} {n_combos}: curve already exists, skipping")
            continue

        print(f"\nRunning CV for {algo} - {n_combos} combos...")
        out = run_cv(matrix_file, cv_file, k=2)
        print(out.strip())

    print("\nAll done!")