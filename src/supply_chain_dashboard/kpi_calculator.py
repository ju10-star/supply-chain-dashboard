import numpy as np 

def scrap_calculate(df_prod):
    """taza de scrap = scrap / fabricados
       Si fabricados es 0, devuelve 0 para evitar división por cero.
       Recibe: DataFrame con columnas 'fabricados' y 'scrap'.
       Devuelve: float (0.0 si no hay fabricados)."""
    fabricados = df_prod['fabricados'].to_numpy(dtype=float)
    scrap = df_prod['scrap'].to_numpy(dtype=float)
    total_fabricados = fabricados.sum()
    if total_fabricados == 0:
        return 0.0
    return scrap.sum() / total_fabricados

def scrap_per_product_calculate(df_prod):
    """Devuelve array (producto, tasa_scrap)
       Recibe: DataFrame con columnas 'producto', 'fabricados', 'scrap'.
       Devuelve: lista de tuplas (producto, tasa_scrap) en el mismo orden que groupby."""
    #Agrupar por producto
    grouped = df_prod.groupby("producto")[["fabricados", "scrap"]].sum().reset_index()
    #Calcular tasa de scrap por producto
    #Pasa a NumPy Calcula vextorizada de tasas usando np.where para evitar división por cero
    fabricados = grouped["fabricados"].to_numpy(dtype=float)
    scrap = grouped["scrap"].to_numpy(dtype=float)
    tasas = np.where(fabricados > 0, scrap / fabricados, 0.0)
    productos = grouped["producto"].tolist()
    return list(zip(grouped["producto"].tolist(), tasas.tolist()))

    ##"""taza de scrap por producto = scrap / fabricados"""
    ###fabricados = df_prod['fabricados'].to_numpy(dtype=float)
    ####scrap = df_prod['scrap'].to_numpy(dtype=float)
   ### with np.errstate(divide='ignore', invalid='ignore'):
        ####scrap_per_product = np.where(fabricados != 0, scrap / fabricados, 0.0)
   ### return dict(zip(df_prod['producto'], scrap_per_product))##
def calcular_nivel_servicio(df_pedidos):
    """Nivel de servicio = pedidos entregados / total pedidos."""
    total = len(df_pedidos)
    if total == 0:
        return 0.0
    entregados = (df_pedidos["estado"] == "entregado").sum()
    return entregados / total

def promedio_cantidad_entregada(df_pedidos):
    """Promedio de cantidad por pedido entregado."""
    entregados = df_pedidos[df_pedidos["estado"] == "entregado"]
    if len(entregados) == 0:
        return 0.0
    return entregados["cantidad"].mean()
