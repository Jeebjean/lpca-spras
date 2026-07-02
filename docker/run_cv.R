# run_cv.R
# Finds the optimal m for a given k using cross-validation

args = commandArgs(trailingOnly = TRUE)
input_file = args[1]
output_file = args[2]
k = as.integer(args[3])

set.seed(42)

# Load data
library(logisticPCA)
data = read.csv(input_file, row.names = NULL)
data = data[, -1]
data_matrix = as.matrix(data)
data_matrix[is.na(data_matrix)] = 0

# Cross-validation over m, fixed k
cv_result = cv.lpca(data_matrix, ks = k, ms = 1:20)
best_m = which.min(cv_result)

cat("Cross-validation done for k =", k, "\n")
cat("Best m:", best_m, "\n")

write.csv(data.frame(k = k, best_m = best_m), output_file, row.names = FALSE)