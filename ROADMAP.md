# Project Roadmap & DataOps Strategy

## Vision & Career Focus
Building a hybrid **DataOps** portfolio tailored for the **European Climate Tech & Clean Energy** sector, combining prior experience in **Technical Support, Cloud, DevOps, and Data** under **Green Software** principles (high efficiency, low hardware/energy footprint).

## Phased Execution Plan

### Phase 1: Lightweight Local Core (Completed ✅)
* **Environment:** Linux Mint (4 GB RAM constraint).
* **Stack:** `uv`, Polars, Apache Arrow, DuckDB, Git/GitHub.
* **Pipeline:** Ingestion of hourly satellite solar radiation and wind speed from **NASA POWER API**, unit conversion, anomaly filtering (`-999`), and SQL aggregation in DuckDB.

### Phase 2: Cross-Platform Validation (In Progress 🔄)
* Clone and execute the pipeline on **Windows** (high-spec machine) and **Ubuntu** using `uv sync`.
* Verify zero-code-change portability and document any OS-specific nuances in `README.md`.

### Phase 3: DataOps & Automation Layer (Upcoming ⏳)
* **CI/CD:** Automate daily pipeline execution and code linting (`Ruff`) via **GitHub Actions**.
* **Observability:** Replace `print()` statements with structured Python `logging` (execution time, row counts, memory usage).
* **Data Quality:** Implement automated schema and value range validations before loading to DuckDB.

### Phase 4: Scalable Cloud & Analytics Layer (Future ⏳)
* Export clean datasets to partitioned **Parquet** files and sync with object storage (S3 / Cloudflare R2).
* Integrate **dbt-duckdb** for modular SQL modeling and automated data tests.
