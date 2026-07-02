library(ggplot2)
library(gridExtra)

datasets = list(
  list(algo="PathLinker", combos=5,  path="data/spras_output_egfr_pathlinker_5"),
  list(algo="PathLinker", combos=10, path="data/spras_output_egfr_pathlinker_10"),
  list(algo="PathLinker", combos=25, path="data/spras_output_egfr_pathlinker_25"),
  list(algo="PathLinker", combos=50, path="data/spras_output_egfr_pathlinker_50"),
  list(algo="OI1",        combos=5,  path="data/spras_output_egfr_oi1_5"),
  list(algo="OI1",        combos=10, path="data/spras_output_egfr_oi1_10"),
  list(algo="OI1",        combos=25, path="data/spras_output_egfr_oi1_25"),
  list(algo="OI1",        combos=54, path="data/spras_output_egfr_oi1_54"),
  list(algo="OI2",        combos=5,  path="data/spras_output_egfr_oi2_5"),
  list(algo="OI2",        combos=10, path="data/spras_output_egfr_oi2_10"),
  list(algo="OI2",        combos=25, path="data/spras_output_egfr_oi2_25"),
  list(algo="OI2",        combos=50, path="data/spras_output_egfr_oi2_50")
)

for (ds in datasets) {
  cv_file = file.path(ds$path, "cv_result.csv")
  matrix_file = file.path(ds$path, "binary_matrix.csv")

  if (!file.exists(cv_file) || !file.exists(matrix_file)) {
    cat("Skipping", ds$algo, ds$combos, ": missing files\n")
    next
  }

  best_m = as.integer(read.csv(cv_file)$best_m[1])
  fixed_values = c(1, 4, 8, 12, 16, 20)
  m_values = sort(unique(c(fixed_values, best_m)))

  matrix_data = read.csv(matrix_file, row.names=1)
  n_present = rowSums(matrix_data)

  cat(sprintf("\n%s - %d combos | CV best m=%d | Testing m=%s\n",
              ds$algo, ds$combos, best_m, paste(m_values, collapse=", ")))

  plots = list()
  for (m in m_values) {
    score_file = file.path(ds$path, paste0("lpca_scores_m", m, ".csv"))
    if (!file.exists(score_file)) {
      cat(sprintf("  m=%d: file not found, skipping\n", m))
      next
    }

    results = read.csv(score_file, row.names=1)
    results$robustness = n_present

    title = if (m == best_m) paste0("m=", m, " * CV best") else paste0("m=", m)

    p = ggplot(results, aes(x=V1, y=V2, color=robustness)) +
      geom_point(alpha=0.4, size=0.8) +
      scale_color_gradient(low="blue", high="red", name="# runs") +
      ggtitle(title) +
      xlab("PC1") + ylab("PC2") +
      theme_minimal() +
      theme(plot.title=element_text(
        size=10,
        face=ifelse(m==best_m, "bold", "plain")
      ))
    plots[[as.character(m)]] = p
  }

  if (length(plots) == 0) next

  combined = arrangeGrob(
    grobs=plots, ncol=4,
    top=paste0(ds$algo, " - ", ds$combos, " combos | CV best m=", best_m,
               " | Color = edge robustness (# runs present)")
  )

  out_file = file.path(ds$path, "viz_m_comparison.png")
  ggsave(out_file, combined, width=16, height=8)
  cat(sprintf("  Saved: %s\n", out_file))
}

cat("\nAll done!\n")