import os
from pathlib import Path
import matplotlib
import pandas as pd
from src.supply_chain_dashboard.dashboard import mostrar_dashboard
matplotlib.use("Agg")
    

def test_dashboard_creates_figures(tmp_path):
    # Datos de ejemplo
    df_pedidos = pd.DataFrame({
        "fecha": ["2026-03-01","2026-03-02"],
        "cliente": ["A","B"],
        "estado": ["entregado","pendiente"],
        "cantidad": [10,5]
    })
    df_prod = pd.DataFrame({
        "producto": ["X","Y"],
        "fabricados": [100,200],
        "scrap": [5,10],
        "fecha": ["2026-03-01","2026-03-02"]
    })

    # Redefinir FIG_DIR para usar carpeta temporal
    from src.supply_chain_dashboard import dashboard
    dashboard.FIG_DIR = tmp_path

    # Ejecutar dashboard
    mostrar_dashboard(df_pedidos, df_prod)

    # Verificar que los tres archivos existen
    files = ["fabricados_vs_scrap_unidades.png",
             "tasa_scrap_por_producto.png",
             "estados_pedidos_pie.png"]
    for f in files:
        assert (tmp_path / f).exists(), f"Expected figure {f} to be created"
        remove_path = tmp_path / f
        if remove_path.exists():
            os.remove(remove_path)  
        else:
            print(f"File {remove_path} does not exist, cannot remove.")
