import streamlit as st
import pandas as pd
import plotly.express as px

# Configuración inicial de la página
st.set_page_config(
    page_title="Wildfire Peru Analytics",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CARGA DE DATOS ---
@st.cache_data
def load_data():
    df = pd.read_csv("data/processed/combined_clean.csv")
    # Asegurarnos de que acq_date sea datetime
    df["acq_date"] = pd.to_datetime(df["acq_date"], errors="coerce")
    return df

st.title("🔥 Panel de Control: Incendios Forestales en Perú")
st.markdown("Exploración interactiva de datos de incendios capturados por los sensores MODIS y VIIRS de la NASA.")

with st.spinner("Cargando base de datos (1.4M registros)..."):
    try:
        data = load_data()
    except FileNotFoundError:
        st.error("⚠️ No se encontró el archivo data/processed/combined_clean.csv. Asegúrate de haber ejecutado src/main.py")
        st.stop()

# --- BARRA LATERAL (FILTROS) ---
st.sidebar.header("Filtros de Búsqueda")

# Filtro de Año
years = sorted(data["year"].dropna().unique().astype(int).tolist())
selected_year = st.sidebar.selectbox("Selecciona el Año", ["Todos"] + years)

# Filtro de Mes
months = ["Todos"] + list(data["month_name"].dropna().unique())
selected_month = st.sidebar.selectbox("Selecciona el Mes", months)

# Filtro de Sensor
sensors = ["Todos", "MODIS", "VIIRS"]
selected_sensor = st.sidebar.selectbox("Selecciona el Sensor", sensors)

# Filtro de Gravedad
frp_levels = ["Todos"] + list(data["frp_level"].dropna().unique())
selected_frp = st.sidebar.selectbox("Nivel de Intensidad (FRP)", frp_levels)

# --- APLICAR FILTROS ---
filtered_data = data.copy()

if selected_year != "Todos":
    filtered_data = filtered_data[filtered_data["year"] == selected_year]
if selected_month != "Todos":
    filtered_data = filtered_data[filtered_data["month_name"] == selected_month]
if selected_sensor != "Todos":
    filtered_data = filtered_data[filtered_data["sensor"] == selected_sensor]
if selected_frp != "Todos":
    filtered_data = filtered_data[filtered_data["frp_level"] == selected_frp]

# --- KPIs ---
st.markdown("### Resumen Rápido")
col1, col2, col3, col4 = st.columns(4)

total_fires = len(filtered_data)
avg_frp = filtered_data["frp"].mean()
avg_bright = filtered_data["brightness"].mean()
max_frp = filtered_data["frp"].max()

col1.metric("🔥 Total Incendios", f"{total_fires:,.0f}")
col2.metric("🌡️ FRP Promedio (MW)", f"{avg_frp:,.1f}" if pd.notnull(avg_frp) else "0")
col3.metric("☀️ Brillo Promedio (K)", f"{avg_bright:,.1f}" if pd.notnull(avg_bright) else "0")
col4.metric("🚨 FRP Máximo Detectado", f"{max_frp:,.1f}" if pd.notnull(max_frp) else "0")

st.markdown("---")

# --- GRÁFICOS ---
col_chart1, col_chart2 = st.columns(2)

with col_chart1:
    st.subheader("Evolución Temporal (Tendencia)")
    if not filtered_data.empty:
        # Agrupar por mes/año para una línea más limpia
        temp_df = filtered_data.groupby(filtered_data["acq_date"].dt.to_period("M")).size().reset_index(name="counts")
        temp_df["acq_date"] = temp_df["acq_date"].dt.to_timestamp()
        
        fig1 = px.line(temp_df, x="acq_date", y="counts", template="plotly_dark", 
                       labels={"acq_date": "Mes/Año", "counts": "Cantidad de Incendios"},
                       line_shape="spline", color_discrete_sequence=["#F63366"])
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("No hay datos para mostrar.")

with col_chart2:
    st.subheader("Incendios por Nivel de Gravedad (FRP)")
    if not filtered_data.empty:
        frp_df = filtered_data.groupby("frp_level").size().reset_index(name="counts")
        fig2 = px.bar(frp_df, x="frp_level", y="counts", template="plotly_dark",
                      labels={"frp_level": "Nivel de FRP", "counts": "Cantidad de Incendios"},
                      color="frp_level", color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("No hay datos para mostrar.")

# --- MAPA GEOESPACIAL ---
st.markdown("### Mapa Geoespacial de Incendios")
if not filtered_data.empty:
    # Optimización: Streamlit st.map es rápido, pero con más de 100k puntos puede consumir mucha RAM del navegador.
    # Tomamos una muestra aleatoria solo para la visualización del mapa si excede los 50k puntos.
    map_data = filtered_data.dropna(subset=["latitude", "longitude"])
    if len(map_data) > 50000:
        st.caption(f"⚠️ *Se está mostrando una muestra aleatoria de 50,000 puntos en el mapa para mantener la fluidez web (el total filtrado es {len(map_data):,}). Los KPIs y gráficos de arriba sí contemplan el 100% de los datos.*")
        map_data = map_data.sample(n=50000, random_state=42)
    
    # Renderizamos un mapa muy rápido utilizando PyDeck integrado en st.map
    st.map(map_data, latitude="latitude", longitude="longitude", color="#F63366")
else:
    st.info("No hay datos geográficos para mostrar con los filtros actuales.")
