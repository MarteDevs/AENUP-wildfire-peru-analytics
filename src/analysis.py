import pandas as pd


def yearly_summary(df):
    # Resumen por año/sensor
    yearly = (
        df.groupby(["sensor", "year"])
        .agg(
            fires=("year", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean"),
            avg_confidence=("confidence_level", lambda x: x.notna().mean())
        )
        .reset_index()
        .sort_values(["sensor", "year"])
    )

    return yearly


def monthly_summary(df):
    # Resumen x mes
    monthly = (
        df.groupby(["sensor", "month", "month_name"])
        .agg(
            fires=("month", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "month"])
    )

    return monthly


def sensor_summary(df):
    # Comparación general (MODIS y VIIRS)
    summary = (
        df.groupby("sensor")
        .agg(
            total_fires=("sensor", "size"),
            min_year=("year", "min"),
            max_year=("year", "max"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
    )

    return summary


def daynight_summary(df):
    # Día/noche
    dn = (
        df.groupby(["sensor", "daynight"])
        .agg(
            fires=("daynight", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "daynight"])
    )

    return dn


def frp_level_summary(df):
    # Resumen x nivel de FRP
    frp = (
        df.groupby(["sensor", "frp_level"])
        .agg(
            fires=("frp_level", "size"),
            avg_frp=("frp", "mean"),
            avg_brightness=("brightness", "mean")
        )
        .reset_index()
        .sort_values(["sensor", "fires"], ascending=[True, False])
    )

    return frp