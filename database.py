import sqlite3

# ==========================================
# CONECTAR BASE DATOS
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# TABLA DEPOSITOS
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS depositos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT,

    capacidad_l INTEGER,

    tipo TEXT,

    estado TEXT

)

""")

# ==========================================
# TABLA VENDIMIA
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS vendimia (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    parcela TEXT,

    variedad TEXT,

    kg REAL,

    deposito TEXT

)

""")

# ==========================================
# TABLA MOVIMIENTOS
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS movimientos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    tipo TEXT,

    origen TEXT,

    destino TEXT,

    litros REAL,

    observaciones TEXT

)

""")

# ==========================================
# GUARDAR
# ==========================================

conn.commit()

conn.close()

print("✅ Base de datos creada correctamente")
