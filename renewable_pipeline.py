import requests
import polars as pl
import duckdb

# 1. EXTRACT: Fetch hourly solar radiation & wind speed from NASA POWER API (Seville, Spain)
host = "power.larc.nasa.gov"
path = "/api/temporal/hourly/point"
url = f"https://{host}{path}"

params = {
    "parameters": "ALLSKY_SFC_SW_DWN,WS10M",
    "community": "RE",
    "longitude": -5.98,
    "latitude": 37.38,
    "start": "20261025",
    "end": "20261031",
    "format": "JSON",
}

print("Fetching NASA POWER satellite renewable energy metrics...")
response = requests.get(url, params=params, timeout=20)
response.raise_for_status()

payload = response.json()
solar_dict = payload["properties"]["parameter"]["ALLSKY_SFC_SW_DWN"]
wind_dict = payload["properties"]["parameter"]["WS10M"]

# 2. TRANSFORM: Clean NASA missing values (-999) and enrich using Polars
df = pl.DataFrame({
    "timestamp_str": list(solar_dict.keys()),
    "solar_radiation_wm2": list(solar_dict.values()),
    "wind_speed_ms": list(wind_dict.values()),
})

df_clean = (
    df.filter(
        (pl.col("solar_radiation_wm2") >= 0) & (pl.col("wind_speed_ms") >= 0)
    )
    .with_columns([
        (pl.col("timestamp_str") + "00").str.to_datetime("%Y%m%d%H%M").alias("timestamp"),
        (pl.col("wind_speed_ms") * 3.6).round(2).alias("wind_speed_kmh"),
    ])
    .with_columns([
        pl.col("timestamp").dt.date().alias("date"),
        (pl.col("solar_radiation_wm2") > 400).alias("is_high_solar"),
        (pl.col("wind_speed_kmh") > 15).alias("is_high_wind"),
    ])
    .select(["timestamp", "date", "solar_radiation_wm2", "wind_speed_kmh", "is_high_solar", "is_high_wind"])
)

# 3. LOAD & ANALYZE: Persist into local DuckDB analytical warehouse
con = duckdb.connect("climate_warehouse.duckdb")
con.execute("CREATE OR REPLACE TABLE nasa_hourly_renewables AS SELECT * FROM df_clean")

daily_summary = con.sql("""
    SELECT 
        date,
        ROUND(AVG(solar_radiation_wm2), 1) AS avg_solar_wm2,
        ROUND(MAX(wind_speed_kmh), 1) AS max_wind_kmh,
        SUM(CASE WHEN is_high_solar OR is_high_wind THEN 1 ELSE 0 END) AS optimal_renewable_hours
    FROM nasa_hourly_renewables
    GROUP BY date
    ORDER BY date ASC
""").pl()

print("\nNASA Satellite Renewable Potential Summary (Seville):")
print(daily_summary)
