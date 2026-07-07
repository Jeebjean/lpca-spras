# compare_pca_lpca.py
# Transpose binary matrix and run LPCA for comparison with SPRAS PCA

import docker
import pandas as pd
from pathlib import Path

ML_DIR = "/Users/mdegbelo/spras/output/egfr/tps_egfr-ml"
ALGOS = ["pathlinker", "omicsintegrator1", "omicsintegrator2"]

def run_lpca(input_file, output_file, k, m):
    client = docker.from_env()
    data_dir = str(Path(input_file).parent.absolute())
    command = [
        "Rscript", "/app/run_lpca.R",
        f"/data/{Path(input_file).name}",
        f"/data/{Path(output_file).name}",
        str(k), str(m)
    ]
    out = client.containers.run(
        "jeebjean/lpca", command,
        volumes=[f"{data_dir}:/data"],
        working_dir="/app", stderr=True
    )
    client.close()
    return out.decode("utf-8")

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
        "jeebjean/lpca", command,
        volumes=[f"{data_dir}:/data"],
        working_dir="/app", stderr=True
    )
    client.close()
    return out.decode("utf-8")

for algo in ALGOS:
    print(f"\n{'='*50}")
    print(f"Processing {algo}")
    print(f"{'='*50}")

    matrix_file = f"{ML_DIR}/{algo}-lpca_binary_matrix.csv"
    transposed_file = f"{ML_DIR}/{algo}-lpca_binary_matrix_transposed.csv"
    cv_file = f"{ML_DIR}/{algo}-lpca_cv_transposed_result.csv"
    scores_file = f"{ML_DIR}/{algo}-lpca_scores_transposed.csv"

    # Step 1: Transpose matrix
    matrix = pd.read_csv(matrix_file, index_col=0)
    print(f"Original matrix: {matrix.shape}")
    matrix_T = matrix.T
    print(f"Transposed matrix: {matrix_T.shape}")
    matrix_T.to_csv(transposed_file)

    if matrix_T.shape[0] < 2 or matrix_T.shape[1] < 2:
        print(f"Matrix too small, skipping")
        continue

   # Step 2: Read best_m from original CV result
    original_cv_file = f"{ML_DIR}/{algo}-lpca_cv_result.csv"
    best_m = int(pd.read_csv(original_cv_file)['best_m'][0])
    print(f"Using m={best_m} from original matrix CV")

    # Step 3: Run LPCA on transposed matrix with this m
    print(f"Running LPCA on transposed matrix with k=2, m={best_m}...")
    out = run_lpca(transposed_file, scores_file, k=2, m=best_m)
    print(out.strip())

print("\nAll done!")
