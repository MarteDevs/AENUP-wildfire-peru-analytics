import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
import os

def create_base_map():
    # Centro aproximado de Perú
    return folium.Map(location=[-9.19, -75.015], zoom_start=5, tiles="CartoDB positron")

def generate_heatmap(df):
    m = create_base_map()
    
    # Extraer latitud y longitud
    heat_data = df[['latitude', 'longitude']].dropna().values.tolist()
    
    # Agregar el mapa de calor
    HeatMap(heat_data, radius=10, blur=15, max_zoom=10).add_to(m)
    
    # Asegurar que exista el directorio
    os.makedirs("outputs/maps", exist_ok=True)
    m.save("outputs/maps/heatmap.html")
    print("Heatmap interactivo guardado en outputs/maps/heatmap.html")

def generate_cluster_map(df):
    m = create_base_map()
    marker_cluster = MarkerCluster().add_to(m)
    
    # Si el dataset es muy grande, tomamos una muestra para no colapsar el navegador con el HTML
    plot_df = df.dropna(subset=['latitude', 'longitude'])
    if len(plot_df) > 50000:
        plot_df = plot_df.sample(n=50000, random_state=42)
        
    for idx, row in plot_df.iterrows():
        # Manejo de la fecha si es NaT
        fecha = row['acq_date'].strftime('%Y-%m-%d') if pd.notnull(row['acq_date']) else 'N/A'
        
        popup_info = (
            f"<b>Fecha:</b> {fecha}<br>"
            f"<b>FRP:</b> {row['frp']}<br>"
            f"<b>Sensor:</b> {row['sensor']}<br>"
            f"<b>Intensidad (Nivel):</b> {row.get('frp_level', 'N/A')}"
        )
        
        folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_info, max_width=300),
            icon=folium.Icon(color='red', icon='fire', prefix='fa')
        ).add_to(marker_cluster)
        
    os.makedirs("outputs/maps", exist_ok=True)
    m.save("outputs/maps/cluster_map.html")
    print("Cluster map interactivo guardado en outputs/maps/cluster_map.html")
