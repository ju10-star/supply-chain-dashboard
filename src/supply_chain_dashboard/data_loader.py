import sqlite3
import pandas as pd
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[2] / "data" / "supply_chain.db"

def cargar_datos():
    conn = sqlite3.connect(DB_PATH.as_posix())
    df_pedidos = pd.read_sql("SELECT * FROM pedidos", conn, parse_dates=["fecha"])
    df_prod = pd.read_sql("SELECT * FROM produccion", conn, parse_dates=["fecha"])
    conn.close()
    return df_pedidos, df_prod