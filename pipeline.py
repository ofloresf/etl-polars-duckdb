
import polars as pl
import duckdb

# 1. Crear datos simulados con Polars
df = pl.DataFrame({
    "producto": ["Laptop", "Teclado", "Monitor", "Ratón", "Laptop"],
    "precio": [10,20,30,40,50],
    "cantidad": [2, 10, 5, 20, 1]
})

# 2. Transformar: calcular el total por venta
df_transformado = df.with_columns(
    (pl.col("precio") * pl.col("cantidad")).alias("total_venta")
)

# 3. Guardar y consultar con DuckDB en un archivo local
con = duckdb.connect("almacen.duckdb")
con.execute("CREATE OR REPLACE TABLE ventas AS SELECT * FROM df_transformado")

resultado = con.sql("""
    SELECT producto, SUM(total_venta) as ingresos_totales
    FROM ventas
    GROUP BY producto
    ORDER BY ingresos_totales DESC
""").pl()

print(resultado)
EOF


