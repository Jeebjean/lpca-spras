# test_k_values.py
# Test different k values on OI2 datasets (5, 10, 25, 50 combos)
# and collect deviance explained for each k

import docker
import pandas as pd
import os
from pathlib import Path

K_VALUES = [2, 3, 4, 5, 10]

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

def run_lpca_fixed_km(input_file, output_file, k, m):
    # Check k is not larger than number of columns
    matrix = pd.read_csv(input_file, index_col=0)
    if k >= matrix.shape[1]:
        print(f"  k={k}: skipping, k must be less than number of columns ({matrix.shape[1]})")
        return None

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

def get_deviance(output_file):
    deviance_file = output_file.replace(".csv", "_deviance.txt")
    if os.path.exists(deviance_file):
        with open(deviance_file) as f:
            return float(f.read().strip())
    return None

if __name__ == "__main__":
    summary = []

    for algo, n_combos, path in DATASETS:
        cv_file = os.path.join(path, "cv_result.csv")
        matrix_file = os.path.join(path, "binary_matrix.csv")

        if not os.path.exists(cv_file) or not os.path.exists(matrix_file):
            print(f"Skipping {algo} {n_combos}: missing files")
            continue

        best_m = int(pd.read_csv(cv_file)['best_m'][0])
        print(f"\n{'='*50}")
        print(f"{algo} - {n_combos} combos | CV best m={best_m}")
        print(f"{'='*50}")

        for k in K_VALUES:
            output_file = os.path.join(path, f"lpca_scores_k{k}_m{best_m}.csv")

            if os.path.exists(output_file):
                print(f"  k={k}: already exists, skipping")
                deviance = get_deviance(output_file)
            else:
                out = run_lpca_fixed_km(matrix_file, output_file, k=k, m=best_m)
                if out is None:
                    summary.append({
                        "Algorithm": algo,
                        "Combos": n_combos,
                        "k": k,
                        "m (CV best)": best_m,
                        "Prop. deviance explained": None
                    })
                    continue
                print(f"  {out.strip()}")
                deviance = get_deviance(output_file)

            summary.append({
                "Algorithm": algo,
                "Combos": n_combos,
                "k": k,
                "m (CV best)": best_m,
                "Prop. deviance explained": round(deviance, 4) if deviance else None
            })

    df = pd.DataFrame(summary)
    print("\n" + "="*60)
    print("SUMMARY - Deviance explained by k and combo level")
    print("="*60)
    print(df.to_string(index=False))
    df.to_csv("data/summary_k_deviance.csv", index=False)
    print("\nSaved to data/summary_k_deviance.csv")