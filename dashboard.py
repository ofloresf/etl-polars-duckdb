import duckdb
import pandas as pd
import polars as pl
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="Climate Tech Renewable Dashboard",
    page_icon="⚡",
    layout="wide",
)

st.title("⚡ Climate Tech DataOps Pipeline")
st.markdown("Monitorización avanzada y analítica de recursos renovables desde **DuckDB**.")


# Función para cargar datos desde DuckDB usando Polars y Pandas
@st.cache_data
def load_data():
    conn = duckdb.connect("climate_warehouse.duckdb", read_only=True)
    query = "SELECT * FROM nasa_hourly_renewables"
    pdf = conn.execute(query).fetchdf()
    df = pl.from_pandas(pdf)
    conn.close()
    return df


try:
    df = load_data()

    if df.is_empty():
        st.warning(
            "La base de datos está vacía. Ejecuta el pipeline primero para cargar datos."
        )
    else:
        # Intentar detectar automáticamente la columna de tiempo/fecha
        time_col = None
        for col in ["timestamp", "datetime", "date", "time"]:
            if col in df.columns:
                time_col = col
                break

        if time_col is None:
            st.error(
                "No se encontró ninguna columna de fecha/tiempo reconocida (timestamp, datetime, date, time)."
            )
            st.stop()

        # Normalizar el formato de NASA POWER (ej. 2025010100 -> 202501010000 para incluir minutos)
        df = df.with_columns(
            pl.col(time_col)
            .cast(pl.Utf8)
            .str.pad_end(12, "0")  # Asegura 12 caracteres rellenando con ceros si falta
            .str.to_datetime(format="%Y%m%d%H%M", strict=False)
            .alias("timestamp")
        )

        min_val = df["timestamp"].min()
        max_val = df["timestamp"].max()

        if min_val is not None and max_val is not None:
            min_date = min_val.date()
            max_date = max_val.date()
        else:
            st.warning(
                f"La columna '{time_col}' no pudo convertirse a fechas válidas."
            )
            st.stop()

        # --- BARRA LATERAL: FILTROS ---
        st.sidebar.header("🔍 Filtros de Análisis")

        date_range = st.sidebar.date_input(
            "Selecciona el Rango de Fechas",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date,
        )

        if isinstance(date_range, tuple) and len(date_range) == 2:
            start_date, end_date = date_range
            df_filtered = df.filter(
                (pl.col("timestamp").dt.date() >= start_date)
                & (pl.col("timestamp").dt.date() <= end_date)
            )
        else:
            df_filtered = df

        # --- KPIs SUPERIORES ---
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Registros en Rango", value=f"{len(df_filtered):,}"
            )

        with col2:
            if "ALLSKY_SFC_SW_DWN" in df_filtered.columns and not df_filtered.is_empty():
                avg_solar = df_filtered["ALLSKY_SFC_SW_DWN"].mean()
                st.metric(
                    label="Radiación Solar Promedio",
                    value=f"{avg_solar:.2f} W/m²",
                )

        with col3:
            if "WS10M" in df_filtered.columns and not df_filtered.is_empty():
                avg_wind = df_filtered["WS10M"].mean()
                st.metric(
                    label="Velocidad de Viento Promedio (10m)",
                    value=f"{avg_wind:.2f} m/s",
                )

        st.divider()

        # Gráficas
        pdf_filtered = df_filtered.to_pandas()
        if not pdf_filtered.empty and "timestamp" in pdf_filtered.columns:
            pdf_filtered["timestamp"] = pd.to_datetime(
                pdf_filtered["timestamp"]
            )
            pdf_filtered = pdf_filtered.set_index("timestamp")

            st.subheader("☀️ Tendencia de Radiación Solar")
            if "ALLSKY_SFC_SW_DWN" in pdf_filtered.columns:
                st.line_chart(pdf_filtered[["ALLSKY_SFC_SW_DWN"]])

            st.subheader("💨 Tendencia de Velocidad del Viento (10m)")
            if "WS10M" in pdf_filtered.columns:
                st.line_chart(pdf_filtered[["WS10M"]])

            if (
                "ALLSKY_SFC_SW_DWN" in pdf_filtered.columns
                and "WS10M" in pdf_filtered.columns
            ):
                st.subheader(
                    "🔄 Correlación Temporal: Radiación Solar vs Viento"
                )
                st.line_chart(pdf_filtered[["ALLSKY_SFC_SW_DWN", "WS10M"]])

        with st.expander("📄 Ver tabla de datos filtrados"):
            st.dataframe(df_filtered, use_container_width=True)

except Exception as e:
    st.error(f"Error al conectar o consultar DuckDB: {e}")
