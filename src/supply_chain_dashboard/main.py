from .db_setup import *
from .data_loader import cargar_datos
from .kpi_calculator import (
    scrap_calculate,
    scrap_per_product_calculate,
    calcular_nivel_servicio,
    promedio_cantidad_entregada
)
from .dashboard import mostrar_dashboard

def main():
    create_data()
    df_pedidos, df_prod = cargar_datos()

    # Calcular KPIs
    tasa_scrap = scrap_calculate(df_prod)
    tasas_por_producto = scrap_per_product_calculate(df_prod)
    nivel_servicio = calcular_nivel_servicio(df_pedidos)
    promedio_entregado = promedio_cantidad_entregada(df_pedidos)

    # Mostrar resultados en consola
    print(f"Tasa de scrap global: {tasa_scrap:.4f}")
    print("Tasa de scrap por producto:")
    for producto, tasa in tasas_por_producto:
        print(f"  - {producto}: {tasa:.4f}")
    print(f"Nivel de servicio: {nivel_servicio:.4f}")
    print(f"Promedio cantidad entregada: {promedio_entregado:.2f}")

    # Mostrar dashboard gráfico
    mostrar_dashboard(df_pedidos, df_prod)

if __name__ == "__main__":
    main()