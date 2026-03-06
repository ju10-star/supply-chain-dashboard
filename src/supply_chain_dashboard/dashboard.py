import matplotlib.pyplot as plt
from pathlib import Path

FIG_DIR = Path(__file__).resolve().parents[2] / "reports" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

def mostrar_dashboard(df_pedidos, df_prod):
    # 1 fabricados vs scrap por producto (unidades)
    agg = df_prod.groupby("producto")[["fabricados", "scrap"]].sum()
    ax = agg.plot(kind="bar", figsize=(9,5), color=["#4C72B0", "#C44E52"])
    ax.set_title("Fabricados y Scrap por Producto (unidades)")
    ax.set_ylabel("Unidades")
    for p in ax.patches:
        ax.annotate(int(p.get_height()), (p.get_x() + p.get_width()/2, p.get_height()),
                    ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "fabricados_vs_scrap_unidades.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()

    # 2 tasa de scrap por producto (%)
    grouped = agg.copy()
    grouped["tasa_scrap"] = grouped["scrap"] / grouped["fabricados"]
    grouped = grouped.reset_index().sort_values("tasa_scrap", ascending=False)

    fig, ax2 = plt.subplots(figsize=(7,4))
    ax2.bar(grouped["producto"], grouped["tasa_scrap"] * 100, color="#C44E52")
    ax2.set_title("Tasa de Scrap por Producto (%)")
    ax2.set_ylabel("Tasa (%)")
    for i, v in enumerate(grouped["tasa_scrap"] * 100):
        ax2.text(i, v + 0.5, f"{v:.1f}%", ha='center', va='bottom', fontsize=9)
    plt.tight_layout()
    plt.savefig(FIG_DIR / "tasa_scrap_por_producto.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()

    #  distribución de estados de pedidos
    counts = df_pedidos["estado"].value_counts()
    ax3 = counts.plot(kind="pie", autopct="%1.1f%%", figsize=(6,6), startangle=90,
                      colors=["#4C72B0","#55A868","#C44E52","#8172B3"])
    ax3.set_ylabel("")  # quitar etiqueta vertical
    ax3.set_title("Distribución de Estados de Pedidos")
    plt.tight_layout()
    plt.savefig(FIG_DIR / "estados_pedidos_pie.png", dpi=150, bbox_inches="tight")
    plt.show()
    plt.close()