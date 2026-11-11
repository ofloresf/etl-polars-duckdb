# Lightweight Satellite Renewable Energy Pipeline (NASA POWER + Polars + DuckDB)

An energy-efficient Data Engineering ETL pipeline built on Linux Mint that ingests hourly satellite solar radiation and wind speed metrics from the **NASA POWER API**, cleans and transforms them in-memory using **Polars**, and stores analytical aggregations in **DuckDB**.

## Why This Stack? (Green Software & Low-Resource Engineering)
Designed to run smoothly on constrained hardware (**4 GB RAM**), minimizing CPU cycles, memory overhead, and energy footprint compared to heavy JVM-based or multi-container stacks:
* **Package & Environment Management:** `uv` (ultra-fast Rust-based Python tooling)
* **Data Processing & Cleaning:** Polars + Apache Arrow (zero-copy columnar transformations, handling missing satellite telemetry `-999` values, and feature engineering)
* **Analytical Warehouse:** DuckDB (embedded OLAP SQL database)

## Data Pipeline Architecture
`NASA POWER REST API (Satellite Telemetry)` ➔ `Polars (Data Cleaning & Feature Engineering)` ➔ `DuckDB (Analytical SQL Aggregations)`

## Quickstart Guide

1. Clone the repository:
   ```bash
   git clone https://github.com/ofloresf/etl-polars-duckdb.git
   cd etl-polars-duckdb
   ```

2. Install dependencies automatically via `uv`:
   ```bash
   uv sync
   ```

3. Run the ETL pipeline:
   ```bash
   uv run renewable_pipeline.py
   ```
