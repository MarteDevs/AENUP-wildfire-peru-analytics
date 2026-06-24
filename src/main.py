import pandas as pd

from cleaning import clean_firms_data
from features import create_features
from analysis import (
    yearly_summary,
    monthly_summary,
    sensor_summary,
    daynight_summary,
    frp_level_summary
)
from plots import (
    plot_yearly_summary,
    plot_monthly_summary,
    plot_sensor_summary,
    plot_daynight_summary,
    plot_frp_summary,
    plot_geo_scatter
)


# Carga los datos crudos
modis = pd.read_csv("data/raw/modis_archive.csv")
viirs = pd.read_csv("data/raw/viirs_archive.csv")

# Limpia ambos datasets
modis = clean_firms_data(modis, "MODIS")
viirs = clean_firms_data(viirs, "VIIRS")

# Crea variables nuevas
modis = create_features(modis)
viirs = create_features(viirs)

# Unimos MODIS y VIIRS
combined = pd.concat([modis, viirs], ignore_index=True)

# Guarda el dataset combinado
combined.to_csv("data/processed/combined_clean.csv", index=False)

# Genera resúmenes
yearly = yearly_summary(combined)
monthly = monthly_summary(combined)
sensor_sum = sensor_summary(combined)
daynight = daynight_summary(combined)
frp_sum = frp_level_summary(combined)

# Guarda resúmenes
yearly.to_csv("data/processed/yearly_summary.csv", index=False)
monthly.to_csv("data/processed/monthly_summary.csv", index=False)
sensor_sum.to_csv("data/processed/sensor_summary.csv", index=False)
daynight.to_csv("data/processed/daynight_summary.csv", index=False)
frp_sum.to_csv("data/processed/frp_summary.csv", index=False)

# Genera visualizaciones
plot_yearly_summary(yearly)
plot_monthly_summary(monthly)
plot_sensor_summary(sensor_sum)
plot_daynight_summary(daynight)
plot_frp_summary(frp_sum)
plot_geo_scatter(combined)

print("Proceso terminado sin errores:")
print("MODIS:", modis.shape)
print("VIIRS:", viirs.shape)
print("COMBINED:", combined.shape)