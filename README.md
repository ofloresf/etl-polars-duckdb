# Pipeline ETL Ligero con Polars y DuckDB

Proyecto de Ingeniería de Datos diseñado para ejecutarse de forma eficiente en entornos con recursos limitados (4 GB RAM) sobre Linux Mint.

## Arquitectura y Stack Tecnológico
* **Gestor de paquetes:** `uv` (rápido y bajo consumo de memoria)
* **Procesamiento (ETL):** Polars + Apache Arrow
* **Almacenamiento Analítico:** DuckDB (almacenamiento columnar local)

## Flujo de Datos
`Datos Crudos (Python/CSV)` -> `Transformación en memoria (Polars)` -> `Carga y consulta SQL (DuckDB)`

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
