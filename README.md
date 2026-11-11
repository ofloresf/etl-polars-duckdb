# Lightweight ETL pipeline with Polars y DuckDB

Data Engineering project designed to be excuted effieciently in a limited resoources environment (4 GB RAM) running on Linux Mint.

Proyecto de Ingeniería de Datos diseñado para ejecutarse de forma eficiente en entornos con recursos limitados (4 GB RAM) sobre Linux Mint.
## Arquitecture and Technological Stack
* **Packet Manager:** `uv` (fast and low memory consumption)
*  **ETL Processing:** Polars + Apache Arrow
*  **Analytic Storage:** DuckDB (local coulmnar storage)


## Arquitectura y Stack Tecnológico
* **Gestor de paquetes:** `uv` (rápido y bajo consumo de memoria)
* **Procesamiento (ETL):** Polars + Apache Arrow
* **Almacenamiento Analítico:** DuckDB (almacenamiento columnar local)

## Data Flow
`Raw Data (Python/CSV)` -> `Memory transformation (Polars)` -> `Load and SQL Queries (DuckDB)`


## Flujo de Datos
`Datos Crudos (Python/CSV)` -> `Transformación en memoria (Polars)` -> `Carga y consulta SQL (DuckDB)`

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
## Cómo replicar este proyecto paso a paso

1. Clonar el repositorio:
   ```bash
   git clone https://github.com
   cd etl-polars-duckdb
   ```

2. Instalar dependencias automáticamente con `uv`:
   ```bash
   uv sync
   ```

3. Ejecutar el pipeline:
   ```bash
   uv run pipeline.py
   ```
# etl-polars-duckdb
# etl-polars-duckdb
