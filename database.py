import sqlite3

# ==========================================
# CONEXION
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

    capacidad_l REAL,

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
# TABLA STOCK SECO
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS stock_seco (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto TEXT,

    cantidad REAL,

    unidad TEXT

)

""")

# ==========================================
# TABLA PRODUCTOS ENOLOGICOS
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS enologicos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    producto TEXT,

    tipo TEXT,

    proveedor TEXT,

    lote_proveedor TEXT,

    cantidad REAL,

    unidad TEXT,

    coste REAL

)

""")

# ==========================================
# TABLA ELABORACION
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS elaboracion (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    deposito TEXT,

    fase TEXT,

    dato1 REAL,
    dato2 REAL,
    dato3 REAL,
    dato4 REAL,
    dato5 REAL,
    dato6 REAL,
    dato7 REAL,
    dato8 REAL,
    dato9 REAL,
    dato10 REAL,

    texto1 TEXT,
    texto2 TEXT

)

""")

# ==========================================
# TABLA CONSUMOS ENOLOGICOS
# ==========================================

cursor.execute("""

CREATE TABLE IF NOT EXISTS consumos_enologicos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    deposito TEXT,

    fase TEXT,

    producto TEXT,

    dosis REAL,

    unidad TEXT

)

""")

# ==========================================
# GUARDAR
# ==========================================

conn.commit()

conn.close()

print("✅ Base datos creada")
