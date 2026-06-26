# AENUP Wildfire Peru Analytics 🔥🇵🇪

Un pipeline integral de análisis de datos geoespaciales y temporales diseñado para procesar, limpiar y visualizar información satelital sobre incendios forestales en Perú.

---

## 📖 Marco Teórico

### El Problema de los Incendios Forestales en Perú
En Perú, los incendios forestales son un problema recurrente, especialmente durante la temporada seca (entre agosto y noviembre). La mayoría de estos incendios son de origen antrópico (causados por humanos), vinculados a prácticas agrícolas tradicionales como el "roza y quema" para limpiar terrenos agrícolas, los cuales muchas veces se salen de control y terminan afectando bosques amazónicos, ecosistemas andinos y áreas naturales protegidas.

### NASA FIRMS (Fire Information for Resource Management System)
El sistema FIRMS de la NASA distribuye datos de incendios activos en tiempo casi real (NRT - Near Real-Time). Provee las coordenadas, la hora y características físicas de las anomalías térmicas detectadas por satélites espaciales. Este proyecto utiliza los datos históricos generados por dos de los sensores más importantes del FIRMS:

#### 1. Sensor MODIS
El *Moderate Resolution Imaging Spectroradiometer* (MODIS) vuela a bordo de los satélites Terra y Aqua. Detecta anomalías térmicas con una resolución espacial de 1 km por píxel. Es un sensor clásico y altamente confiable que lleva décadas monitoreando el planeta, aunque su menor resolución puede hacer que se pierdan incendios muy pequeños.

#### 2. Sensor VIIRS
El *Visible Infrared Imaging Radiometer Suite* (VIIRS) vuela a bordo de los satélites Suomi NPP y NOAA-20. Ofrece una resolución espacial superior de 375 metros por píxel. Esto le permite detectar incendios mucho más pequeños y mapear perímetros de grandes incendios con mayor precisión, y a menudo detecta entre 3 y 4 veces más focos de calor que MODIS.

### Fire Radiative Power (FRP)
El FRP (Poder Radiativo del Fuego) es una variable crucial en nuestros datos. Se mide en Megavatios (MW) y cuantifica la energía calórica irradiada por el incendio. Un FRP alto indica un incendio muy intenso, que consume mucha biomasa de manera rápida, lo que lo correlaciona directamente con la cantidad de gases de efecto invernadero (humo, CO2) que se están emitiendo a la atmósfera.

---

## ⚙️ Documentación del Proyecto

El código está estructurado de manera modular para transformar datos satelitales crudos en información lista para toma de decisiones y reportes.

### Estructura de Directorios

```text
AENUP-wildfire-peru-analytics/
│
├── data/
│   ├── raw/                 # Archivos originales de la NASA (modis_archive.csv, viirs_archive.csv)
│   └── processed/           # Datasets limpios y resúmenes estadísticos (generados automáticamente)
│
├── outputs/
│   ├── figures/             # Gráficos estáticos PNG (tendencias, estacionalidad, distribuciones)
│   └── maps/                # Mapas interactivos HTML generados con Folium
│
├── src/                     # Código fuente del pipeline
│   ├── main.py              # Script principal que orquesta el pipeline
│   ├── cleaning.py          # Lógica de estandarización y limpieza
│   ├── features.py          # Ingeniería de características (momentos del día, niveles de severidad)
│   ├── analysis.py          # Agregaciones estadísticas
│   ├── plots.py             # Generación de gráficos estáticos con Matplotlib y Seaborn
│   └── maps.py              # Generación de mapas geoespaciales interactivos
│
└── requirements.txt         # Lista de dependencias del entorno
```

### Funcionalidades del Pipeline
1. **Limpieza Uniforme:** Homologa la confianza (Confidence) de MODIS (numérica) y VIIRS (letras) en una única escala (`Low`, `Medium`, `High`), eliminando anomalías sin coordenadas.
2. **Feature Engineering:** Deriva variables de temporalidad (año, mes, momento del día) y categoriza el nivel de gravedad basándose en el FRP y el Brightness (Brillo).
3. **Análisis Estadístico:** Genera reportes por año, mes y nivel de severidad.
4. **Visualización Estática:** Exporta gráficas en PNG útiles para reportes técnicos.
5. **Análisis Geoespacial:** Exporta mapas web de calor (Heatmaps) y mapas de clústeres dinámicos.
6. **Dashboard Interactivo:** Proveemos una aplicación web construida con Streamlit que te permite filtrar e interactuar con los datos visualmente.

### Instalación y Ejecución

1. Asegúrate de tener Python instalado (probado en Python 3.10+).
2. Se recomienda crear un entorno virtual:
   ```bash
   python -m venv .venv
   ```
3. Activar el entorno virtual:
   - En Windows: `.\.venv\Scripts\Activate.ps1`
   - En Mac/Linux: `source .venv/bin/activate`
4. Instalar las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
5. Ejecutar el pipeline completo:
   ```bash
   python src/main.py
   ```

Una vez que el script finaliza ("Proceso terminado sin errores"), puedes encontrar los CSV limpios en `data/processed/`, las gráficas en `outputs/figures/`, y abrir los mapas interactivos ubicados en `outputs/maps/` usando cualquier navegador web.

### 📊 Despliegue del Dashboard Interactivo

Hemos construido una aplicación web de alto rendimiento utilizando **Streamlit** y **Plotly** para reemplazar los gráficos estáticos por interactivos. El dashboard incluye:
- **Filtros Laterales:** Permite segmentar 1.4 millones de registros por Año, Mes, Sensor y Gravedad.
- **KPIs en Tiempo Real:** Métricas que se actualizan dinámicamente según tus filtros.
- **Visualizaciones Interactivas:** Gráficos de tendencias temporales y distribución por nivel de FRP.
- **Mapa Geoespacial Integrado:** Para evitar que el navegador se congele, el mapa aplica automáticamente un límite inteligente: si los filtros seleccionados agrupan más de 50,000 puntos, renderizará un muestreo aleatorio uniforme para mantener la web fluida (mientras que los KPIs sí calculan el 100% de la data).
- **Tema Oscuro Persistente:** Interfaz diseñada con colores y fondos optimizados.

#### ¿Cómo ejecutarlo?

Si deseas explorar los datos, ejecuta el siguiente comando teniendo tu entorno virtual activado:

```bash
streamlit run src/dashboard.py
```

> **Nota sobre el primer inicio:** 
> La primera vez que ejecutes Streamlit en tu computadora, es posible que la terminal te muestre el siguiente mensaje:
> `If you'd like to receive helpful onboarding emails... Please enter your email address below.`
> **No es necesario ingresar ningún correo**. Simplemente deja el espacio en blanco, presiona la tecla **Enter** (Intro) y la aplicación continuará cargando.

Tu navegador se abrirá automáticamente (usualmente en `http://localhost:8501`) mostrando el panel de control interactivo.