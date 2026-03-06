import sqlite3
import logging
from pathlib import Path
from typing import Optional

logger = logging.getLogger(__name__)

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "supply_chain.db"

def create_data(db_path: Optional[Path] = None) -> None:
    """
    Crea la base de datos SQLite y carga datos de ejemplo si las tablas están vacías.

    Parámetros
    db_path: Path opcional para la base de datos. Si no se provee, se usa DB_PATH.
    """
    path = db_path or DB_PATH
    path.parent.mkdir(parents=True, exist_ok=True)

    try:
        # Usar contexto para asegurar commit/close automáticos
        with sqlite3.connect(path.as_posix()) as conn:
            cursor = conn.cursor()

            # Tablas
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS pedidos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT,
                cliente TEXT,
                estado TEXT,
                cantidad INTEGER
            )
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS produccion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                producto TEXT,
                fabricados INTEGER,
                scrap INTEGER,
                fecha TEXT
            )
            """)

            # Índices para consultas por fecha y producto
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pedidos_fecha ON pedidos(fecha)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produccion_producto ON produccion(producto)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_produccion_fecha ON produccion(fecha)")

            # Insertar datos de ejemplo en pedidos si está vacío
            cursor.execute("SELECT COUNT(1) FROM pedidos")
            row = cursor.fetchone()
            count = row[0] if row is not None else 0

            if count == 0:
                cursor.executemany(
                    "INSERT INTO pedidos (fecha, cliente, estado, cantidad) VALUES (?,?,?,?)",
                    [
                        ('2026-03-01','Cliente A','entregado',10),
                        ('2026-03-02','Cliente B','pendiente',5),
                        ('2026-03-02','Cliente C','entregado',7),
                        ('2026-03-03','Cliente D','cancelado',3),
                        ('2026-03-03','Cliente E','entregado',12),
                    ]
                )

            # Insertar datos de ejemplo en produccion si está vacío
            cursor.execute("SELECT COUNT(1) FROM produccion")
            row = cursor.fetchone()
            count = row[0] if row is not None else 0

            if count == 0:
                cursor.executemany(
                    "INSERT INTO produccion (producto, fabricados, scrap, fecha) VALUES (?,?,?,?)",
                    [
                        ('Producto X',100,5,'2026-03-01'),
                        ('Producto Y',200,10,'2026-03-02'),
                        ('Producto Z',150,15,'2026-03-03'),
                    ]
                )

    except sqlite3.DatabaseError as e:
        logger.exception("Error al crear o poblar la base de datos: %s", e)
        raise