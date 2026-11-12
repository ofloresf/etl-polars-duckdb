# Climate Tech DataOps Pipeline 🌍⚡

A lightweight, high-performance DataOps pipeline designed for Climate Tech applications. It extracts real-time renewable energy weather metrics (solar radiation and wind speed) from the NASA POWER API, processes them using memory-efficient columnar formats, and stores them locally in an analytical warehouse.

Built with a **Green Software** engineering mindset: optimized to run seamlessly on resource-constrained edge environments (such as Linux Mint with 4GB RAM) as well as robust development workstations, utilizing zero heavy containerization overhead.

---

## 🚀 Key Features

- **High-Performance Extract**: Pulls hourly solar irradiance (`ALLSKY_SFC_SW_DWN`) and 10m wind speed (`WS10M`) metrics using the NASA POWER API.
- **Modern Data Stack**: Powered by `uv` for lightning-fast dependency management, `Polars` + Apache Arrow for blazing-fast, low-memory data transformations, and `DuckDB` as an embedded analytical data warehouse.
- **Multi-Platform Portability**: Runs identically across Linux Mint, Ubuntu (WSL2), and native Windows without modifying a single line of code.
- **Data Quality & Observability** *(Phase 3)*: Structured logging and strict physical boundary validation rules prior to warehouse ingestion.
- **Automated CI/CD** *(Phase 3)*: Daily scheduled execution via GitHub Actions.

---

## 🛠️ Tech Stack

- **Language**: Python 3.10+
- **Dependency & Environment Manager**: [uv](https://github.com/astral-sh/uv)
- **Data Processing**: Polars, Apache Arrow
- **Storage / Warehouse**: DuckDB (`climate_warehouse.duckdb`)
- **API Source**: NASA POWER API (Prediction of Worldwide Energy Resources)

---

## 📦 Installation & Setup

Ensure you have `uv` installed on your system.

### 1. Clone the Repository
```bash
git clone [https://github.com/ofloresf/etl-polars-duckdb.git](https://github.com/ofloresf/etl-polars-duckdb.git)
cd etl-polars-duckdb
