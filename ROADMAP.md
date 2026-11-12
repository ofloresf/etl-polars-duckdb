# Project Roadmap: Climate Tech DataOps Pipeline
This document outlines the evolutionary phases of our lightweight, green-engineered data pipeline.

## Vision & Career Focus
Building a hybrid **DataOps** portfolio tailored for the **European Climate Tech & Clean Energy** sector, combining prior experience in **Technical Support, Cloud, DevOps, and Data** under **Green Software** principles (high efficiency, low hardware/energy footprint).

# ✅ Phase 1: Core ETL & Analytical Storage (Completed)

[x] Integrate NASA POWER API for real-time solar and wind metrics (Seville coordinates).

[x] Implement robust cleaning logic to filter out missing/null values (-999).

[x] Process and transform data streams efficiently using Polars and Apache Arrow.

[x] Persist and query daily aggregated metrics inside an embedded DuckDB warehouse (climate_warehouse.duckdb).


# ✅ Phase 2: Multi-Platform Portability & Environment Validation (Completed)

[x] Establish dependency management via uv.

[x] Validate zero-code-change portability across Linux Mint (4GB RAM edge setup), Ubuntu (WSL2), and Native Windows.

[x] Standardize cross-platform installation procedures (winget for Windows, shell scripts for Unix).


#  Phase 3: DataOps Maturity & Cloud Automation (In Progress)

[x] Documentation sync: Publish professional English README and ROADMAP.

## [ ] Step 3.1: Observability & Data Quality:

Replace basic print() statements with structured logging (logging module).

Implement physical range boundary assertions (e.g., solar radiation >= 0, wind speed >= 0) before DuckDB insertion.

## [ ] Step 3.2: Code Quality with Ruff:

Integrate Ruff for ultra-fast linting and code formatting.

## [ ] Step 3.3: Cloud Automation:

Set up GitHub Actions workflow (.github/workflows/daily_etl.yml) for scheduled daily pipeline execution.


#  Phase 4: Advanced Green Analytics & Reporting (Planned)

[ ] Build lightweight visualization endpoints or local dashboard metrics.

[ ] Carbon footprint / energy optimization tracking for pipeline execution.
