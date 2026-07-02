# run_full_test.py
# Full LPCA test pipeline across multiple algorithms and parameter combination levels

import pandas as pd
import glob
from pathlib import Path

from run_lpca import run_full_pipeline

ALGO_PATTERNS = {
    "PathLinker": "tps_egfr-pathlinker-*",
    "OI1": "tps_egfr-omicsintegrator1-*",
    "OI2": "tps_egfr-omicsintegrator2-*",
}

if __name__ == "__main__":
    summary_results = []

    for algo, pattern in ALGO_PATTERNS.items():
        algorithm_files = glob.glob(
            f"/Users/mdegbelo/spras/output/egfr/{pattern}/pathway.txt"
        )
        n_files = len(algorithm_files)

        if n_files == 0:
            print(f"No files found for {algo}, skipping")
            continue

        print(f"\n{'='*60}")
        print(f"{algo}: found {n_files} parameter combination files")
        print(f"{'='*60}")

        output_dir = f"/Users/mdegbelo/lpca-docker/data/spras_output_egfr_{algo.lower()}_{n_files}"
        run_full_pipeline(algorithm_files, output_dir, k=2)

        matrix = pd.read_csv(f"{output_dir}/binary_matrix.csv", index_col=0)
        cv_file = f"{output_dir}/cv_result.csv"
        best_m = pd.read_csv(cv_file)['best_m'][0] if Path(cv_file).exists() else None

        summary_results.append({
            "Algorithm": algo,
            "Combinations": n_files,
            "Matrix rows (edges)": matrix.shape[0],
            "Matrix cols (runs)": matrix.shape[1],
            "Best m": best_m
        })

    df = pd.DataFrame(summary_results)
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(df.to_string(index=False))
    df.to_csv("/Users/mdegbelo/lpca-docker/data/summary_all_combos.csv", index=False)