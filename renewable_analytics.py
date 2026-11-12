import logging
import duckdb

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("ClimateAnalytics")

def run_analytics():
    db_path = "climate_warehouse.duckdb"
    logger.info(f"Connecting to DuckDB warehouse in read-only mode: {db_path}")
    
    con = duckdb.connect(db_path, read_only=True)
    
    # 1. Daily Aggregations using fetchall()
    logger.info("Computing daily meteorological summaries for Seville...")
    daily_query = """
        SELECT 
            SUBSTR(timestamp, 1, 8) AS date_str,
            ROUND(AVG(ALLSKY_SFC_SW_DWN), 2) AS avg_solar_irradiance,
            ROUND(MAX(WS10M), 2) AS max_wind_speed,
            ROUND(AVG(WS10M), 2) AS avg_wind_speed
        FROM nasa_hourly_renewables
        GROUP BY date_str
        ORDER BY date_str ASC;
    """
    daily_rows = con.execute(daily_query).fetchall()
    logger.info(f"Generated daily aggregates successfully for {len(daily_rows)} days.")
    
    print("\n--- Daily Aggregates Sample (First 5 Days of January 2025) ---")
    print(f"{'Date':<12} | {'Avg Solar (kW-hr/m²)'} | {'Max Wind (m/s)'} | {'Avg Wind (m/s)'}")
    print("-" * 65)
    for row in daily_rows[:5]:
        date_str, avg_solar, max_wind, avg_wind = row
        print(f"{date_str:<12} | {avg_solar:<22} | {max_wind:<16} | {avg_wind}")
    
    # 2. Peak Generation Highlights
    logger.info("Identifying peak renewable generation windows...")
    peak_solar = con.execute("""
        SELECT timestamp, ALLSKY_SFC_SW_DWN 
        FROM nasa_hourly_renewables 
        ORDER BY ALLSKY_SFC_SW_DWN DESC 
        LIMIT 3;
    """).fetchall()
    
    print("\n--- Top 3 Peak Solar Radiation Hours ---")
    for row in peak_solar:
        print(f"Timestamp: {row[0]} -> Solar Irradiance: {row[1]} kW-hr/m²")
        
    peak_wind = con.execute("""
        SELECT timestamp, WS10M 
        FROM nasa_hourly_renewables 
        ORDER BY WS10M DESC 
        LIMIT 3;
    """).fetchall()
    
    print("\n--- Top 3 Peak Wind Speed Hours ---")
    for row in peak_wind:
        print(f"Timestamp: {row[0]} -> Wind Speed (10m): {row[1]} m/s")
        
    con.close()
    logger.info("Analytics execution completed successfully.")

if __name__ == "__main__":
    run_analytics()
