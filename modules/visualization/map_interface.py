import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from typing import Dict

try:
    from modules.visualization.interactive_maps import EpicHealthMaps
    MAPS_AVAILABLE = True
except ImportError:
    try:
        from interactive_maps import EpicHealthMaps
        MAPS_AVAILABLE = True
    except ImportError:
        MAPS_AVAILABLE = False

class MapInterface:
    def __init__(self):
        if MAPS_AVAILABLE:
            self.epic_maps = EpicHealthMaps()
        else:
            self.epic_maps = None
    
    def render_epic_maps_dashboard(self, data: Dict, user_permissions: list = None):
        """Renderizar dashboard épico de mapas interactivos con permisos por rol"""
        
        if not MAPS_AVAILABLE:
            st.error("❌ Sistema de mapas no disponible. Instala: pip install folium streamlit-folium")
            return
        
        # Obtener mapas disponibles según permisos del usuario
        available_maps = self.get_maps_by_permissions(user_permissions or [])
        
        if not available_maps:
            st.warning("⚠️ No tienes permisos para acceder a mapas interactivos.")
            return
        
        st.markdown("""
        <div class="maps-dashboard-header">
            <h1>🗺️ MAPAS INTERACTIVOS ÉPICOS</h1>
            <h2>Sistema Sanitario de Málaga - Análisis Geoespacial</h2>
            <p>✨ Explora la red sanitaria con mapas adaptados a tu rol ✨</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Mostrar información sobre permisos
        self.show_permission_info(user_permissions)
        
        # Selector de tipo de mapa (filtrado por permisos)
        map_options = available_maps
        
        selected_map = st.selectbox("🎯 Selecciona el tipo de mapa:", map_options)
        
        # Configuraciones del mapa
        col1, col2, col3 = st.columns(3)
        
        with col1:
            map_style = st.selectbox("🎨 Estilo del Mapa:", 
                                   ["Dark Theme", "OpenStreetMap", "Satellite", "Terrain"])
        
        with col2:
            zoom_level = st.slider("🔍 Nivel de Zoom:", 8, 12, 9)
        
        with col3:
            show_legend = st.checkbox("📋 Mostrar Leyenda", value=True)
        
        # Inicializar estado del mapa si no existe
        if 'map_generated' not in st.session_state:
            st.session_state.map_generated = False
            st.session_state.current_map = None
            st.session_state.current_map_type = None
            st.session_state.filtered_data = None
        
        # Para administradores, ofrecer generar mapa automáticamente la primera vez
        if not st.session_state.map_generated and "mapas_todos" in user_permissions:
            if st.button("🚀 Generar Mapa Completo Automáticamente", type="primary"):
                with st.spinner("🎨 Creando mapa épico completo..."):
                    try:
                        filtered_data = self.filter_data_by_permissions(data, user_permissions)
                        epic_map = self.create_complete_epic_map(filtered_data, 9)
                        
                        st.session_state.map_generated = True
                        st.session_state.current_map = epic_map
                        st.session_state.current_map_type = "🌟 Mapa Completo Épico (Generado Automáticamente)"
                        st.session_state.filtered_data = filtered_data
                        
                        st.success("✅ Mapa completo épico generado automáticamente")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
            
            st.markdown("---")
        
        # Generar el mapa seleccionado
        if st.button("🚀 Generar Mapa Épico", type="primary"):
            with st.spinner("🎨 Creando mapa épico..."):
                try:
                    # Filtrar datos según permisos del usuario
                    filtered_data = self.filter_data_by_permissions(data, user_permissions)
                    
                    if "Completo" in selected_map:
                        epic_map = self.create_complete_epic_map(filtered_data, zoom_level)
                    elif "Hospitales" in selected_map or "Ubicaciones Básicas" in selected_map:
                        epic_map = self.create_hospitals_map(filtered_data, zoom_level)
                    elif "Municipios" in selected_map or "Análisis Demográfico" in selected_map:
                        epic_map = self.create_municipalities_map(filtered_data, zoom_level)
                    elif "Heatmap" in selected_map:
                        epic_map = self.create_accessibility_heatmap(filtered_data, zoom_level)
                    elif "Cobertura" in selected_map:
                        epic_map = self.create_coverage_map(filtered_data, zoom_level)
                    elif "Rutas" in selected_map:
                        epic_map = self.create_routes_map(filtered_data, zoom_level)
                    else:
                        epic_map = self.create_complete_epic_map(filtered_data, zoom_level)
                    
                    # Guardar el mapa en session_state
                    st.session_state.map_generated = True
                    st.session_state.current_map = epic_map
                    st.session_state.current_map_type = selected_map
                    st.session_state.filtered_data = filtered_data
                    
                    st.success(f"✅ Mapa '{selected_map}' generado correctamente")
                    
                except Exception as e:
                    st.error(f"❌ Error generando mapa: {str(e)}")
                    st.session_state.map_generated = False
        
        # Mostrar el mapa si ya está generado
        if st.session_state.map_generated and st.session_state.current_map is not None:
            st.markdown(f"### 🗺️ {st.session_state.current_map_type}")
            
            # Configurar el mapa para Streamlit con key única para evitar recargas
            map_key = f"epic_map_{hash(str(st.session_state.current_map_type))}"
            
            map_data = st_folium(
                st.session_state.current_map, 
                width=1200, 
                height=600,
                returned_objects=["last_clicked"],
                key=map_key
            )
            
            # Información del objeto clickeado (sin causar recarga)
            if map_data and map_data.get('last_clicked') is not None:
                with st.expander("📍 Información del Punto Seleccionado", expanded=False):
                    self.show_clicked_info(map_data['last_clicked'], st.session_state.filtered_data)
            
            # Estadísticas del mapa
            self.show_map_statistics(st.session_state.filtered_data)
            
            # Botón para limpiar el mapa
            if st.button("🗑️ Limpiar Mapa", type="secondary"):
                st.session_state.map_generated = False
                st.session_state.current_map = None
                st.session_state.current_map_type = None
                st.session_state.filtered_data = None
                st.rerun()
        
        # Panel de información
        self.render_map_info_panel(data)
    
    def create_complete_epic_map(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear mapa completo con todas las funcionalidades épicas"""
        
        try:
            # Verificar que tenemos todos los datos necesarios
            required_datasets = ['hospitales', 'demografia', 'servicios', 'accesibilidad']
            missing_datasets = [ds for ds in required_datasets if ds not in data or data[ds].empty]
            
            if missing_datasets:
                st.warning(f"⚠️ Datasets faltantes para mapa completo: {', '.join(missing_datasets)}")
                # Crear mapa básico solo con los datos disponibles
                epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
                
                if 'hospitales' in data and not data['hospitales'].empty:
                    epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
                
                if 'demografia' in data and not data['demografia'].empty:
                    epic_map = self.epic_maps.add_epic_municipalities(epic_map, data['demografia'])
                
                epic_map = self.epic_maps.create_epic_control_panel(epic_map)
                return epic_map
            
            # Crear mapa completo con todos los datos
            return self.epic_maps.create_epic_complete_map(
                hospitals_data=data['hospitales'],
                demographics_data=data['demografia'],
                services_data=data['servicios'],
                accessibility_data=data['accesibilidad']
            )
            
        except Exception as e:
            st.error(f"❌ Error creando mapa completo: {str(e)}")
            # Fallback: crear mapa básico
            epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
            if 'hospitales' in data and not data['hospitales'].empty:
                epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
            return epic_map
    
    def create_hospitals_map(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear mapa enfocado en hospitales"""
        
        epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
        epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
        epic_map = self.epic_maps.create_epic_control_panel(epic_map)
        
        # Título específico para hospitales
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #e74c3c, #c0392b); color: white; 
                    padding: 10px 20px; border-radius: 20px; z-index: 9999;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            <h3 style="margin: 0;">🏥 Red Hospitalaria de Málaga</h3>
            <p style="margin: 5px 0; opacity: 0.9;">Centros Sanitarios y Capacidad</p>
        </div>
        '''
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map
    
    def create_municipalities_map(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear mapa enfocado en municipios"""
        
        epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
        epic_map = self.epic_maps.add_epic_municipalities(epic_map, data['demografia'])
        epic_map = self.epic_maps.create_epic_control_panel(epic_map)
        
        # Título específico para municipios
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #27ae60, #229954); color: white; 
                    padding: 10px 20px; border-radius: 20px; z-index: 9999;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            <h3 style="margin: 0;">🏘️ Municipios de Málaga</h3>
            <p style="margin: 5px 0; opacity: 0.9;">Población y Crecimiento 2025</p>
        </div>
        '''
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map
    
    def create_accessibility_heatmap(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear heatmap de accesibilidad"""
        
        epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
        epic_map = self.epic_maps.create_accessibility_heatmap(epic_map, data['accesibilidad'])
        epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
        
        # Título específico para accesibilidad
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #f39c12, #e67e22); color: white; 
                    padding: 10px 20px; border-radius: 20px; z-index: 9999;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            <h3 style="margin: 0;">🔥 Heatmap de Accesibilidad</h3>
            <p style="margin: 5px 0; opacity: 0.9;">Tiempos de Acceso a Hospitales</p>
        </div>
        '''
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map
    
    def create_coverage_map(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear mapa de cobertura de especialidades"""
        
        epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
        epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
        epic_map = self.epic_maps.add_service_coverage_circles(epic_map, data['hospitales'], data['servicios'])
        epic_map = self.epic_maps.create_epic_control_panel(epic_map)
        
        # Título específico para cobertura
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #9b59b6, #8e44ad); color: white; 
                    padding: 10px 20px; border-radius: 20px; z-index: 9999;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            <h3 style="margin: 0;">💊 Cobertura de Especialidades</h3>
            <p style="margin: 5px 0; opacity: 0.9;">Áreas de Servicio Médico</p>
        </div>
        '''
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map
    
    def create_routes_map(self, data: Dict, zoom_level: int) -> folium.Map:
        """Crear mapa de rutas principales"""
        
        epic_map = self.epic_maps.create_epic_base_map(zoom_start=zoom_level)
        epic_map = self.epic_maps.add_epic_hospitals(epic_map, data['hospitales'])
        epic_map = self.epic_maps.add_epic_municipalities(epic_map, data['demografia'])
        epic_map = self.epic_maps.add_epic_routes(epic_map, data['accesibilidad'])
        epic_map = self.epic_maps.create_epic_control_panel(epic_map)
        
        # Título específico para rutas
        title_html = '''
        <div style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%);
                    background: linear-gradient(135deg, #34495e, #2c3e50); color: white; 
                    padding: 10px 20px; border-radius: 20px; z-index: 9999;
                    box-shadow: 0 4px 8px rgba(0,0,0,0.3);">
            <h3 style="margin: 0;">🛣️ Rutas de Acceso</h3>
            <p style="margin: 5px 0; opacity: 0.9;">Conexiones y Tiempos de Viaje</p>
        </div>
        '''
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map
    
    def show_clicked_info(self, clicked_data: Dict, data: Dict):
        """Mostrar información del objeto clickeado en el mapa"""
        
        if clicked_data and 'lat' in clicked_data and 'lng' in clicked_data:
            lat, lng = clicked_data['lat'], clicked_data['lng']
            
            st.markdown("### 📍 Información del Punto Seleccionado")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write(f"**Coordenadas:** {lat:.4f}, {lng:.4f}")
                
                # Buscar hospital más cercano
                closest_hospital = self.find_closest_hospital(lat, lng, data['hospitales'])
                if closest_hospital:
                    distance = self.calculate_distance(lat, lng, 
                                                     closest_hospital['latitud'], 
                                                     closest_hospital['longitud'])
                    st.write(f"**Hospital más cercano:** {closest_hospital['nombre']}")
                    st.write(f"**Distancia:** {distance:.1f} km")
            
            with col2:
                # Buscar municipio más cercano
                closest_municipality = self.find_closest_municipality(lat, lng, data['demografia'])
                if closest_municipality:
                    st.write(f"**Municipio:** {closest_municipality}")
                    
                    # Información demográfica
                    muni_data = data['demografia'][data['demografia']['municipio'] == closest_municipality]
                    if not muni_data.empty:
                        muni_info = muni_data.iloc[0]
                        st.write(f"**Población:** {muni_info['poblacion_2025']:,}")
                        st.write(f"**Crecimiento:** +{muni_info['crecimiento_2024_2025']:,}")
    
    def show_map_statistics(self, data: Dict):
        """Mostrar estadísticas épicas del sistema"""
        
        st.markdown("### 📊 Estadísticas Épicas del Sistema")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_hospitals = len(data['hospitales'])
            st.metric("🏥 Total Hospitales", total_hospitals)
            
            regional_hospitals = len(data['hospitales'][data['hospitales']['tipo_centro'] == 'Hospital Regional'])
            st.metric("🏥 Hospitales Regionales", regional_hospitals)
        
        with col2:
            total_population = data['demografia']['poblacion_2025'].sum()
            st.metric("👥 Población Total", f"{total_population/1000:.0f}K")
            
            total_beds = data['hospitales']['camas_funcionamiento_2025'].sum()
            st.metric("🛏️ Camas Totales", f"{total_beds:,}")
        
        with col3:
            avg_access_time = data['accesibilidad']['tiempo_coche_minutos'].mean()
            st.metric("⏱️ Tiempo Medio Acceso", f"{avg_access_time:.0f} min")
            
            max_access_time = data['accesibilidad']['tiempo_coche_minutos'].max()
            st.metric("⏱️ Tiempo Máximo", f"{max_access_time:.0f} min")
        
        with col4:
            bed_ratio = (total_beds / total_population) * 1000
            st.metric("📊 Camas/1000 hab", f"{bed_ratio:.1f}")
            
            growing_municipalities = len(data['demografia'][data['demografia']['crecimiento_2024_2025'] > 0])
            st.metric("📈 Municipios en Crecimiento", growing_municipalities)
        
        # Gráfico épico adicional
        self.create_epic_summary_chart(data)
    
    def create_epic_summary_chart(self, data: Dict):
        """Crear gráfico resumen épico"""
        
        import plotly.graph_objects as go
        from plotly.subplots import make_subplots
        
        # Crear subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('🏥 Hospitales por Tipo', '👥 Top 5 Municipios', 
                          '⏱️ Tiempos de Acceso', '🛏️ Capacidad vs Población'),
            specs=[[{"type": "pie"}, {"type": "bar"}],
                   [{"type": "histogram"}, {"type": "scatter"}]]
        )
        
        # Gráfico 1: Hospitales por tipo (Pie)
        hospital_types = data['hospitales']['tipo_centro'].value_counts()
        fig.add_trace(
            go.Pie(labels=hospital_types.index, values=hospital_types.values, 
                   name="Hospitales", hole=0.3),
            row=1, col=1
        )
        
        # Gráfico 2: Top 5 municipios (Bar)
        top_municipalities = data['demografia'].nlargest(5, 'poblacion_2025')
        fig.add_trace(
            go.Bar(x=top_municipalities['municipio'], 
                   y=top_municipalities['poblacion_2025'],
                   marker_color='lightblue'),
            row=1, col=2
        )
        
        # Gráfico 3: Histograma de tiempos de acceso
        fig.add_trace(
            go.Histogram(x=data['accesibilidad']['tiempo_coche_minutos'],
                        nbinsx=20, marker_color='orange'),
            row=2, col=1
        )
        
        # Gráfico 4: Scatter capacidad vs población
        fig.add_trace(
            go.Scatter(x=data['hospitales']['poblacion_referencia_2025'],
                      y=data['hospitales']['camas_funcionamiento_2025'],
                      mode='markers+text',
                      text=data['hospitales']['municipio'],
                      textposition='top center',
                      marker=dict(size=10, color='red')),
            row=2, col=2
        )
        
        # Actualizar layout
        fig.update_layout(
            height=600,
            showlegend=False,
            title_text="📊 Dashboard Geoespacial Épico - Sistema Sanitario Málaga",
            title_x=0.5
        )
        
        st.plotly_chart(fig, width="stretch")
    
    def render_map_info_panel(self, data: Dict):
        """Panel de información adicional sobre mapas"""
        
        st.markdown("---")
        st.markdown("### 💡 Guía de Mapas Interactivos")
        
        tab1, tab2, tab3 = st.tabs(["🎯 Funcionalidades", "📊 Interpretación", "🛠️ Controles"])
        
        with tab1:
            st.markdown("""
            #### 🌟 Funcionalidades Épicas Implementadas:
            
            **🏥 Marcadores Inteligentes:**
            - Tamaño proporcional a capacidad del hospital
            - Colores según tipo de centro sanitario
            - Popups con información completa y estadísticas
            
            **🗺️ Capas Interactivas:**
            - Hospitales con información detallada
            - Municipios con datos demográficos
            - Heatmap de accesibilidad sanitaria
            - Círculos de cobertura por especialidad
            - Rutas principales con tiempos de viaje
            
            **⚡ Controles Avanzados:**
            - Pantalla completa para análisis detallado
            - Medidor de distancias entre puntos
            - Minimapa con vista general
            - Coordenadas en tiempo real del cursor
            - Control de capas para análisis específicos
            """)
        
        with tab2:
            st.markdown("""
            #### 📊 Cómo Interpretar los Mapas:
            
            **🎨 Código de Colores:**
            - 🔴 **Rojo**: Hospitales Regionales (mayor capacidad)
            - 🔵 **Azul**: Hospitales Universitarios  
            - 🟠 **Naranja**: Hospitales Comarcales
            - 🟢 **Verde**: Centros de Alta Resolución
            
            **📏 Tamaños de Marcadores:**
            - **Grande**: >1000 camas (hospitales principales)
            - **Medio**: 500-1000 camas (hospitales comarcales)
            - **Pequeño**: <500 camas (centros locales)
            
            **🔥 Heatmap de Accesibilidad:**
            - **Verde**: Alta accesibilidad (<45 min)
            - **Amarillo**: Accesibilidad media (45-60 min)
            - **Rojo**: Baja accesibilidad (>60 min)
            
            **🛣️ Rutas:**
            - **Verde**: Rutas rápidas (<45 min)
            - **Naranja**: Rutas moderadas (45-60 min)
            - **Rojo**: Rutas lentas (>60 min)
            """)
        
        with tab3:
            st.markdown("""
            #### 🛠️ Controles del Mapa:
            
            **🖱️ Navegación:**
            - **Zoom**: Rueda del ratón o botones +/-
            - **Desplazar**: Clic y arrastrar
            - **Información**: Clic en cualquier marcador
            
            **📋 Panel de Capas:**
            - Activar/desactivar capas específicas
            - Ver solo hospitales o solo municipios
            - Combinar múltiples visualizaciones
            
            **📐 Herramientas:**
            - **Medir Distancias**: Herramienta en esquina inferior derecha
            - **Pantalla Completa**: Botón en esquina superior izquierda
            - **Coordenadas**: Mostradas en tiempo real
            
            **💡 Consejos:**
            - Usa diferentes niveles de zoom para análisis macro/micro
            - Combina capas para análisis multidimensional
            - Haz clic en marcadores para información detallada
            """)
    
    def find_closest_hospital(self, lat: float, lng: float, hospitals_data: pd.DataFrame):
        """Encontrar hospital más cercano a unas coordenadas"""
        
        min_distance = float('inf')
        closest_hospital = None
        
        for _, hospital in hospitals_data.iterrows():
            distance = self.calculate_distance(lat, lng, hospital['latitud'], hospital['longitud'])
            if distance < min_distance:
                min_distance = distance
                closest_hospital = hospital
        
        return closest_hospital
    
    def find_closest_municipality(self, lat: float, lng: float, demographics_data: pd.DataFrame):
        """Encontrar municipio más cercano"""
        
        municipality_coords = {
            'Málaga': [36.7213, -4.4214],
            'Marbella': [36.5108, -4.8856],
            'Vélez-Málaga': [36.7875, -4.1017],
            'Antequera': [37.0179, -4.5613],
            'Ronda': [36.7427, -5.1658]
        }
        
        min_distance = float('inf')
        closest_municipality = None
        
        for municipality, coords in municipality_coords.items():
            distance = self.calculate_distance(lat, lng, coords[0], coords[1])
            if distance < min_distance:
                min_distance = distance
                closest_municipality = municipality
        
        return closest_municipality
    
    def calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calcular distancia entre dos puntos en km"""
        
        from math import radians, sin, cos, sqrt, atan2
        
        # Convertir a radianes
        lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
        
        # Fórmula de Haversine
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))
        
        # Radio de la Tierra en km
        R = 6371
        
        return R * c
    
    def get_maps_by_permissions(self, user_permissions: list) -> list:
        """Obtener mapas disponibles según permisos del usuario"""
        
        # Definir mapas y sus permisos requeridos
        maps_permissions = {
            "🌟 Mapa Completo Épico (Todas las capas)": ["mapas_todos"],
            "🏥 Hospitales y Centros Sanitarios": ["mapas_operativos", "mapas_publicos", "mapas_todos"],
            "🏘️ Municipios y Demografía": ["mapas_demograficos", "mapas_analiticos", "mapas_publicos", "mapas_todos"],
            "🔥 Heatmap de Accesibilidad": ["mapas_analiticos", "mapas_gestion", "mapas_todos"],
            "💊 Cobertura de Especialidades": ["mapas_operativos", "mapas_gestion", "mapas_todos"],
            "🛣️ Rutas y Conexiones": ["mapas_gestion", "mapas_estrategicos", "mapas_todos"],
            "📊 Análisis Demográfico": ["mapas_demograficos", "mapas_analiticos", "mapas_todos"],
            "🏥 Ubicaciones Básicas": ["mapas_publicos", "mapas_todos"]
        }
        
        available_maps = []
        
        for map_name, required_permissions in maps_permissions.items():
            # Si el usuario tiene al menos uno de los permisos requeridos
            if any(perm in user_permissions for perm in required_permissions):
                available_maps.append(map_name)
        
        return available_maps
    
    def show_permission_info(self, user_permissions: list):
        """Mostrar información sobre permisos del usuario para mapas"""
        
        # Determinar tipo de acceso
        if "mapas_todos" in user_permissions:
            access_level = "🔓 **Acceso Completo** - Todos los mapas disponibles"
            color = "success"
        elif "mapas_estrategicos" in user_permissions:
            access_level = "🏛️ **Acceso Estratégico** - Mapas de planificación y gestión avanzada"
            color = "info"
        elif "mapas_operativos" in user_permissions:
            access_level = "⚙️ **Acceso Operativo** - Mapas de gestión sanitaria"
            color = "info"
        elif "mapas_analiticos" in user_permissions:
            access_level = "📊 **Acceso Analítico** - Mapas estadísticos y demográficos"
            color = "info"
        elif "mapas_publicos" in user_permissions:
            access_level = "👁️ **Acceso Público** - Mapas básicos de ubicación"
            color = "warning"
        else:
            access_level = "❌ **Sin Acceso** - No tienes permisos para mapas"
            color = "error"
        
        if color == "success":
            st.success(access_level)
        elif color == "info":
            st.info(access_level)
        elif color == "warning":
            st.warning(access_level)
        else:
            st.error(access_level)
    
    def filter_data_by_permissions(self, data: Dict, user_permissions: list) -> Dict:
        """Filtrar datos según permisos del usuario"""
        
        filtered_data = data.copy()
        
        # Si no tiene permisos sensibles, filtrar datos
        if "mapas_sensibles" not in user_permissions and "mapas_todos" not in user_permissions:
            # Filtrar información sensible de hospitales
            if 'hospitales' in filtered_data:
                hospitals = filtered_data['hospitales'].copy()
                if "mapas_operativos" not in user_permissions:
                    # Remover datos operativos sensibles
                    sensitive_columns = ['personal_sanitario_2025', 'presupuesto_anual', 'camas_uci']
                    for col in sensitive_columns:
                        if col in hospitals.columns:
                            hospitals = hospitals.drop(columns=[col])
                filtered_data['hospitales'] = hospitals
        
        # Si solo tiene acceso público, mostrar solo datos básicos
        if user_permissions == ["mapas_publicos"] or (len(user_permissions) == 2 and "ver_datos" in user_permissions):
            # Solo hospitales públicos básicos
            if 'hospitales' in filtered_data:
                public_hospitals = filtered_data['hospitales'][
                    filtered_data['hospitales']['tipo_centro'].isin(['Hospital Regional', 'Hospital Universitario'])
                ].copy()
                # Solo columnas básicas
                basic_columns = ['nombre', 'tipo_centro', 'municipio', 'latitud', 'longitud', 'urgencias_24h']
                available_columns = [col for col in basic_columns if col in public_hospitals.columns]
                filtered_data['hospitales'] = public_hospitals[available_columns]
        
        return filtered_data