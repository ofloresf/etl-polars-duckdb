# Lightweight ETL pipeline with Polars y DuckDB

Data Engineering project designed to be excuted effieciently in a limited resources environment (4 GB RAM) running on Linux Mint.

## Arquitecture and Technological Stack
* **Packet Manager:** `uv` (fast and low memory consumption)
*  **ETL Processing:** Polars + Apache Arrow
*  **Analytic Storage:** DuckDB (local coulmnar storage)

## Data Flow
`Raw Data (Python/CSV)` -> `Memory transformation (Polars)` -> `Load and SQL Queries (DuckDB)`

## How to replicate this project step by step
1. Clone the repo:
   ```bash
   git clone https://github.com
   cd etl-polars-duckdb
   ```
2. Automatically Install dependencies with `uv`:
   ```bash
   uv sync
   ```
3. Run the pipeline:
   ```bash
   uv run pipeline.py
   ```   
# etl-polars-duckdb
# etl-polars-duckdb
