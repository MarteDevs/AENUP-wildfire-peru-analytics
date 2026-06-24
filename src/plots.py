import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Config de estilo para las gráficas
sns.set_theme(style="whitegrid", context="talk")


def plot_yearly_summary(df):
    # Incendios por año
    plt.figure(figsize=(12, 6))

    sns.lineplot(
        data=df,
        x="year",
        y="fires",
        hue="sensor",
        marker="o",
        linewidth=2.5
    )

    plt.title("Incendios forestales por año")
    plt.xlabel("Año")
    plt.ylabel("Número de incendios")
    plt.legend(title="Sensor")
    plt.tight_layout()
    plt.savefig("outputs/figures/yearly_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_monthly_summary(df):
    # Incendios por mes
    plt.figure(figsize=(12, 6))

    month_order = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]

    plot_df = df.copy()
    plot_df["month_name"] = pd.Categorical(
        plot_df["month_name"],
        categories=month_order,
        ordered=True
    )

    sns.barplot(
        data=plot_df,
        x="month_name",
        y="fires",
        hue="sensor"
    )

    plt.title("Incendios forestales por mes")
    plt.xlabel("Mes")
    plt.ylabel("Número de incendios")
    plt.xticks(rotation=45)
    plt.legend(title="Sensor")
    plt.tight_layout()
    plt.savefig("outputs/figures/monthly_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_sensor_summary(df):
    # Comparación total entre sensores
    plt.figure(figsize=(8, 5))

    sns.barplot(
        data=df,
        x="sensor",
        y="total_fires",
        palette="Blues"
    )

    plt.title("Comparación total de incendios por sensor")
    plt.xlabel("Sensor")
    plt.ylabel("Total de incendios")

    # Mostrar el valor en cada barra
    for i, value in enumerate(df["total_fires"]):
        plt.text(i, value, f"{value:,.0f}", ha="center", va="bottom")

    plt.tight_layout()
    plt.savefig("outputs/figures/sensor_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_daynight_summary(df):
    # Día/noche
    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=df,
        x="daynight",
        y="fires",
        hue="sensor",
        palette="Set2"
    )

    plt.title("Incendios detectados de día y de noche")
    plt.xlabel("Momento")
    plt.ylabel("Número de incendios")
    plt.legend(title="Sensor")
    plt.tight_layout()
    plt.savefig("outputs/figures/daynight_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_frp_summary(df):
    # FRP x nivel
    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=df,
        x="frp_level",
        y="fires",
        hue="sensor",
        palette="Oranges"
    )

    plt.title("Incendios por nivel de FRP")
    plt.xlabel("Nivel de FRP")
    plt.ylabel("Número de incendios")
    plt.legend(title="Sensor")
    plt.tight_layout()
    plt.savefig("outputs/figures/frp_summary.png", dpi=300, bbox_inches="tight")
    plt.close()


def plot_geo_scatter(df):
    # Distribución en superficie peruana
    plt.figure(figsize=(10, 8))

    sns.scatterplot(
        data=df,
        x="longitude",
        y="latitude",
        hue="sensor",
        alpha=0.4,
        s=20,
        palette="Set1"
    )

    plt.title("Distribución geográfica de los incendios")
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.legend(title="Sensor")
    plt.tight_layout()
    plt.savefig("outputs/figures/geo_scatter.png", dpi=300, bbox_inches="tight")
    plt.close()