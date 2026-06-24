import pandas as pd
import numpy as np


def create_features(df):
    """
    Crea variables nuevas a partir de la fecha, hora e intensidad.
    Esto nos sirve para el análisis y las visualizaciones.
    """

    # Realizamos una copia para trabajar
    df = df.copy()

    # Fecha en formato datetime
    df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")

    # Variables de tiempo (año, mes, trimestre, día)
    df["year"] = df["acq_date"].dt.year
    df["month"] = df["acq_date"].dt.month
    df["quarter"] = df["acq_date"].dt.quarter
    df["day_of_year"] = df["acq_date"].dt.dayofyear
    df["month_name"] = df["acq_date"].dt.month_name()

    # Hora de registro en formato HHMM
    df["hour"] = pd.to_numeric(df["acq_time"], errors="coerce") // 100

    # Clasificamos la hora en límites simples
    df["time_slot"] = pd.cut(
        df["hour"],
        bins=[-1, 5, 11, 17, 23],
        labels=["night", "morning", "afternoon", "evening"]
    )

    # Clasificación simple de FRP
    df["frp_level"] = np.where(
        df["frp"] < 5, "Low",
        np.where(df["frp"] < 20, "Medium", "High")
    )

    # Clasificación simple de brightness
    df["brightness_level"] = np.where(
        df["brightness"] < 320, "Low",
        np.where(df["brightness"] < 340, "Medium", "High")
    )

    return df