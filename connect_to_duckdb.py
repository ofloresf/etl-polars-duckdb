#import duckdb

import duckdb

# Conectar al warehouse analítico local
con = duckdb.connect("climate_warehouse.duckdb")

# Ver las tablas disponibles
print("Tablas en el almacén:")
print(con.execute("SHOW TABLES;").fetchall())

# Consultar una muestra de los datos diarios agregados
print("\nMuestra de datos diarios (Sevilla):")
print(con.execute("SELECT * FROM nasa_hourly_renewables LIMIT 5;").fetchall())

con.close()
