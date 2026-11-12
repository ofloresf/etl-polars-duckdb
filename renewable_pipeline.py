import logging
import urllib.request
import json
from datetime import datetime, timedelta
import polars as pl
import duckdb

# Configure structured logging (Green Software: zero heavy external logging dependencies)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ClimatePipeline")

# Configuration Constants (Seville coordinates)
LAT = 37.3891
LON = -5.9845

# Use a fully consolidated historical window (previous year) to ensure data availability
START_DATE = "20250101"
END_DATE = "20250131"

NASA_API_URL = (
    f"https://power.larc.nasa.gov/api/temporal/hourly/point?"
    f"parameters=ALLSKY_SFC_SW_DWN,WS10M&community=RE&"
    f"longitude={LON}&latitude={LAT}&start={START_DATE}&end={END_DATE}&format=JSON"
)

def fetch_nasa_data() -> dict:
    logger.info(f"Fetching NASA POWER weather metrics for Seville (lat: {LAT}, lon: {LON})...")
    logger.info(f"Date range: {START_DATE} to {END_DATE}")
    
    req = urllib.request.Request(
        NASA_API_URL,
        headers={"User-Agent": "ClimateTechDataOpsPipeline/1.0"}
    )
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode("utf-8"))
    
    logger.info("Successfully retrieved raw JSON payload from NASA POWER API.")
    return data

def transform_and_validate_data(raw_data: dict) -> pl.DataFrame:
    logger.info("Parsing and transforming hourly meteorological streams...")
    
    properties = raw_data.get("properties", {}).get("parameter", {})
    solar_rad = properties.get("ALLSKY_SFC_SW_DWN", {})
    wind_speed = properties.get("WS10M", {})
    
    # Align timestamps securely
    timestamps = list(solar_rad.keys())
    solar_values = [solar_rad.get(ts) for ts in timestamps]
    wind_values = [wind_speed.get(ts) for ts in timestamps]
    
    df = pl.DataFrame({
        "timestamp": timestamps,
        "ALLSKY_SFC_SW_DWN": solar_values,
        "WS10M": wind_values
    })
    
    # Clean NASA missing value indicator (-999) and parse dates (NASA hourly format is YYYYMMDDHH -> append '00' for minutes)
    df = df.with_columns([
        (pl.col("timestamp") + "00").str.strptime(pl.Datetime, "%Y%m%d%H%M").alias("datetime"),
        pl.col("ALLSKY_SFC_SW_DWN").cast(pl.Float64),
        pl.col("WS10M").cast(pl.Float64)
    ]).filter(
        (pl.col("ALLSKY_SFC_SW_DWN") != -999) & 
        (pl.col("WS10M") != -999)
    )
    
    initial_rows = len(df)
    logger.info(f"Cleaned dataset rows (excluding API nulls): {initial_rows}")
    
    # Data Quality: Physical boundary checks
    logger.info("Running Data Quality physical boundary validations...")
    valid_df = df.filter(
        (pl.col("ALLSKY_SFC_SW_DWN") >= 0.0) &
        (pl.col("WS10M") >= 0.0) &
        (pl.col("WS10M") < 100.0)
    )
    
    dropped_rows = initial_rows - len(valid_df)
    if dropped_rows > 0:
        logger.warning(f"Data Quality Alert: Dropped {dropped_rows} records violating physical boundaries.")
    else:
        logger.info("Data Quality check passed: All records within valid physical parameters.")
        
    return valid_df

def persist_to_duckdb(df: pl.DataFrame):
    db_path = "climate_warehouse.duckdb"
    logger.info(f"Persisting processed telemetry into DuckDB warehouse: {db_path}")
    
    con = duckdb.connect(db_path)
    con.register("df_view", df)
    
    # Drop and recreate cleanly to avoid schema mismatch from previous test runs
    con.execute("DROP TABLE IF EXISTS nasa_hourly_renewables;")
    con.execute("""
        CREATE TABLE nasa_hourly_renewables AS 
        SELECT * FROM df_view;
    """)
    
    row_count = con.execute("SELECT COUNT(*) FROM nasa_hourly_renewables;").fetchone()[0]
    logger.info(f"Persistence complete. Total rows in warehouse table 'nasa_hourly_renewables': {row_count}")
    
    con.close()

def main():
    try:
        raw_json = fetch_nasa_data()
        processed_df = transform_and_validate_data(raw_json)
        persist_to_duckdb(processed_df)
        logger.info("Pipeline execution completed successfully.")
    except Exception as e:
        logger.error(f"Pipeline execution failed: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
