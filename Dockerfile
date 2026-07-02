FROM rocker/r-base

RUN Rscript -e "install.packages('logisticPCA', repos='https://cran.r-project.org')"

COPY run_lpca.R /app/run_lpca.R
COPY run_cv.R /app/run_cv.R

WORKDIR /app