library(ggplot2)
library(gridExtra)
library(yaml)

ML_DIR = "/Users/mdegbelo/spras/output/egfr/tps_egfr-ml"
LOG_DIR = "/Users/mdegbelo/spras/output/egfr/logs"
algo = "rwr"

# Charger PCA classique
pca = read.csv(file.path(ML_DIR, "rwr-pca-coordinates.txt"), header=TRUE, sep="\t")
pca = pca[!pca$datapoint_labels %in% c("centroid", "kde_peak"), ]
pca$hash = gsub("tps_egfr-rwr-params-", "", pca$datapoint_labels)

# Charger LPCA transposé
lpca = read.csv(file.path(ML_DIR, "rwr-lpca_scores_transposed.csv"), row.names=1)
lpca$hash = gsub("tps_egfr-rwr-params-", "", rownames(lpca))

# Merger
merged = merge(pca, lpca, by="hash")
cat(sprintf("Matched runs: %d\n", nrow(merged)))

# Charger paramètres pour coloration
param_files = list.files(LOG_DIR,
  pattern="parameters-rwr.*\\.yaml",
  full.names=TRUE)

params_list = lapply(param_files, function(f) {
  params = yaml.load_file(f)
  hash = gsub(".*parameters-rwr.*-(\\w+)\\.yaml", "\\1", basename(f))
  numeric_params = params[sapply(params, is.numeric)]
  if (length(numeric_params) > 0) {
    data.frame(hash=hash, param_val=numeric_params[[1]],
               param_name=names(numeric_params)[1])
  }
})
params_df = do.call(rbind, params_list)
merged2 = merge(merged, params_df, by="hash")

# Plot PCA classique
p1 = ggplot(merged2, aes(x=PC1, y=PC2, color=factor(round(param_val,3)))) +
  geom_point(size=3, alpha=0.8) +
  ggtitle("Standard PCA (SPRAS) - rwr") +
  xlab("PC1") + ylab("PC2") +
  theme_minimal() +
  labs(color=unique(merged2$param_name))

# Plot LPCA transposé
p2 = ggplot(merged2, aes(x=V1, y=V2, color=factor(round(param_val,3)))) +
  geom_point(size=3, alpha=0.8) +
  ggtitle("LPCA transposed - rwr") +
  xlab("PC1") + ylab("PC2") +
  theme_minimal() +
  labs(color=unique(merged2$param_name))

combined = arrangeGrob(p1, p2, ncol=2,
  top="Standard PCA vs LPCA transposed - rwr (14 runs)")

ggsave("data/viz_pca_vs_lpca_rwr.png", combined, width=16, height=8)
cat("Done!\n")