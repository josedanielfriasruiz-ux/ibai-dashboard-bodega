import sqlite3

# ==========================================
# CONEXION
# ==========================================

conn = sqlite3.connect("bodega.db")

cursor = conn.cursor()

# ==========================================
# BORRAR TABLAS ANTIGUAS
# ==========================================

cursor.execute("DROP TABLE IF EXISTS depositos")
cursor.execute("DROP TABLE IF EXISTS lotes")
cursor.execute("DROP TABLE IF EXISTS vendimia")
cursor.execute("DROP TABLE IF EXISTS movimientos")
cursor.execute("DROP TABLE IF EXISTS stock_seco")
cursor.execute("DROP TABLE IF EXISTS enologicos")
cursor.execute("DROP TABLE IF EXISTS elaboracion")
cursor.execute("DROP TABLE IF EXISTS consumos_enologicos")

# ==========================================
# TABLA DEPOSITOS
# ==========================================

cursor.execute("""

CREATE TABLE depositos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    nombre TEXT,

    capacidad_l REAL,

    tipo TEXT,

    estado TEXT

)

""")

# ==========================================
# TABLA LOTES
# ==========================================

cursor.execute("""

CREATE TABLE lotes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    lote TEXT,

    vino TEXT,

    anada INTEGER,

    parcela TEXT,

    estado TEXT,

    litros REAL

)

""")

# ==========================================
# TABLA VENDIMIA
# ==========================================

cursor.execute("""

CREATE TABLE vendimia (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    lote TEXT,

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

CREATE TABLE movimientos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    lote TEXT,

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

CREATE TABLE stock_seco (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    producto TEXT,

    cantidad REAL,

    unidad TEXT

)

""")

# ==========================================
# TABLA ENOLOGICOS
# ==========================================

cursor.execute("""

CREATE TABLE enologicos (

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

CREATE TABLE elaboracion (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    lote TEXT,

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

CREATE TABLE consumos_enologicos (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    fecha TEXT,

    lote TEXT,

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

print("✅ Base de datos recreada")
