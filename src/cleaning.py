import pandas as pd


def clean_firms_data(df, sensor_name):
    """
    Limpieza básica de los datos de FIRMS.
    La cosa es dejar MODIS y VIIRS con la misma estructura
    antes de empezar el análisis.
    """

    # Copia para no modificar el original
    df = df.copy()

    # Normaliza nombres de columnas (-espacios + minus)
    df.columns = df.columns.str.strip().str.lower()

    # Convierte fecha -> datetime
    df["acq_date"] = pd.to_datetime(
        df["acq_date"],
        errors="coerce"
    )

    # Estandariza valores de día/noche (-espacios + minus)
    df["daynight"] = (
        df["daynight"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    # Nueva columna para identificar el sensor
    df["sensor"] = sensor_name

    # Confidence original se guarda por si luego se hacen análisis de comparación
    df["confidence_original"] = df["confidence"]

    # MODIS usa confidence numérico (0-100)
    if pd.api.types.is_numeric_dtype(df["confidence"]):

        df["confidence_level"] = pd.cut(
            df["confidence"],
            bins=[0, 33, 66, 100],
            labels=["Low", "Medium", "High"],
            include_lowest=True
        )

    # VIIRS usa l, n, h
    else:

        confidence_map = {
            "l": "Low",
            "n": "Medium",
            "h": "High"
        }

        df["confidence_level"] = (
            df["confidence"]
            .astype(str)
            .str.lower()
            .map(confidence_map)
        )

    # Elimina duplicados
    df = df.drop_duplicates()

    # Elimina filas sin información necesaria
    df = df.dropna(
        subset=[
            "latitude",
            "longitude",
            "acq_date"
        ]
    )

    print(f"{sensor_name}: {len(df):,} registros luego de limpieza")

    return df