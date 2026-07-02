# run_lpca.py
# Standalone Python script to call the LPCA Docker container programmatically
# Reference: spras/containers.py#L343

import docker
import pandas as pd
from pathlib import Path, PurePath
from typing import Iterable, Union
from os import PathLike

# Import summarize_networks from SPRAS
import sys
sys.path.append("/Users/mdegbelo/spras")
from spras.analysis.ml import summarize_networks

def run_lpca(input_file: str, output_file: str, k: int, m: int):
    """
    Runs the LPCA Docker container on a binary data matrix.

    @param input_file: absolute path to the input CSV file (binary matrix)
    @param output_file: absolute path to the output CSV file (PC scores)
    @param k: number of principal components
    @param m: confidence parameter
    """

    # Initialize Docker client
    client = docker.from_env()

    # Define the data directory to mount
    data_dir = str(Path(input_file).parent)

    # Build the command to run inside the container
    command = [
        "Rscript", "/app/run_lpca.R",
        f"/data/{Path(input_file).name}",
        f"/data/{Path(output_file).name}",
        str(k),
        str(m)
    ]

    print(f"Running LPCA with k={k}, m={m}...")
    print(f"Input: {input_file}")
    print(f"Output: {output_file}")

    # Run the container
    out = client.containers.run(
        "jeebjean/lpca",
        command,
        volumes=[f"{data_dir}:/data"],
        working_dir="/app",
        stderr=True
    )

    print(out.decode("utf-8"))
    client.close()


def run_cv(input_file: str, output_file: str, k: int):
    
    client = docker.from_env()
    data_dir = str(Path(input_file).parent)

    command = [
        "Rscript", "/app/run_cv.R",
        f"/data/{Path(input_file).name}",
        f"/data/{Path(output_file).name}",
        str(k)
    ]

    print(f"Running cross-validation with k={k}...")

    out = client.containers.run(
        "jeebjean/lpca",
        command,
        volumes=[f"{data_dir}:/data"],
        working_dir="/app",
        stderr=True
    ).decode("utf-8")

    print(out)
    client.close()

    # Extract best_m from the output
    for line in out.splitlines():
        if "Best m:" in line:
            best_m = int(line.split("Best m:")[-1].strip())
            print(f"Best m found: {best_m}")
            return best_m

    raise ValueError("Could not find best m in cross-validation output")



def run_full_pipeline(
    algorithm_output_files: list,
    output_dir: str,
    k: int
):
    """
    Full pipeline:
    1. Summarize algorithm outputs into a binary edge x algorithm matrix
    2. Run cross-validation to find optimal m
    3. Run LPCA with the optimal m

    @param algorithm_output_files: list of file paths from SPRAS algorithm outputs
    @param output_dir: directory to write all intermediate and final files
    @param k: number of principal components
    """

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Step 1: Build binary matrix from algorithm outputs
    print("=" * 50)
    print("STEP 1: Building binary edge x algorithm matrix")
    print("=" * 50)
    matrix = summarize_networks(algorithm_output_files)
    print(f"Matrix shape: {matrix.shape}")
    print(f"Columns (algorithms): {list(matrix.columns)}")
    print(matrix.head())

    # Save matrix to CSV
    matrix_path = output_dir / "binary_matrix.csv"
    matrix.to_csv(matrix_path)
    print(f"Matrix saved to {matrix_path}")

    # Check minimum size before cross-validation
    if matrix.shape[0] < 20:
        print(f"Warning: matrix too small ({matrix.shape[0]} rows, {matrix.shape[1]} columns) for cross-validation and LPCA.")
        print("Need at least 20 rows (edges). Skipping LPCA.")
        return
    
    if matrix.shape[1] < 2:
        print(f"Warning: matrix too small ({matrix.shape[1]} columns) for LPCA.")
        print("Need at least 2 columns (algorithms). Skipping LPCA.")
        return

    # Step 2: Cross-validation to find optimal m
    print("=" * 50)
    print("STEP 2: Cross-validation to find optimal m")
    print("=" * 50)
    best_m = run_cv(
        input_file=str(matrix_path),
        output_file=str(output_dir / "cv_result.csv"),
        k=k
    )

    # Step 3: Run LPCA
    print("=" * 50)
    print("STEP 3: Running LPCA")
    print("=" * 50)
    run_lpca(
        input_file=str(matrix_path),
        output_file=str(output_dir / "lpca_scores.csv"),
        k=k,
        m=best_m
    )

    print("=" * 50)
    print("Pipeline complete!")
    print(f"Results saved in: {output_dir}")
    print("=" * 50)

if __name__ == "__main__":

   # Test: OmicsIntegrator1 - 10+ parameter combinations
    print("=" * 50)
    print("TEST CASE 3: OmicsIntegrator2 - 10 combinations")
    print("=" * 50)

    import glob
    algorithm_files = glob.glob(
        "/Users/mdegbelo/spras/output/egfr/tps_egfr-pathlinker-params-*/pathway.txt"
    )
    print(f"Found {len(algorithm_files)} algorithm output files")

    run_full_pipeline(
        algorithm_output_files=algorithm_files,
        output_dir="/Users/mdegbelo/lpca-docker/data/spras_output_egfr_pathlinker_5",
        k=2
    )