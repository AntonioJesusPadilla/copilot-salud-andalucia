import folium
from folium import plugins
import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
import json
import streamlit as st
import plotly.express as px

# Importación opcional de geopy
try:
    from geopy.distance import geodesic
    GEOPY_AVAILABLE = True
except ImportError:
    GEOPY_AVAILABLE = False
    st.warning("⚠️ geopy no disponible - algunas funciones de mapas estarán limitadas")

class EpicHealthMaps:
    def __init__(self):
        # Coordenadas centrales de Málaga
        self.malaga_center = [36.7213, -4.4214]
        
        # Colores épicos para diferentes tipos de centros
        self.hospital_colors = {
            'Hospital Regional': '#e74c3c',      # Rojo intenso
            'Hospital Universitario': '#3498db',  # Azul brillante
            'Hospital Comarcal': '#f39c12',      # Naranja vibrante
            'Centro Alta Resolución': '#27ae60'   # Verde esmeralda
        }
        
        # Colores para especialidades médicas
        self.specialty_colors = {
            'cardiologia': '#e74c3c',
            'neurologia': '#9b59b6', 
            'oncologia_medica': '#34495e',
            'pediatria': '#f1c40f',
            'ginecologia': '#e91e63',
            'traumatologia': '#ff5722',
            'urgencias_generales': '#f44336'
        }
    
    def create_epic_base_map(self, style: str = 'OpenStreetMap', zoom_start: int = 9) -> folium.Map:
        """Crear mapa base épico de Málaga"""
        
        # Crear mapa con configuración premium
        m = folium.Map(
            location=self.malaga_center,
            zoom_start=zoom_start,
            tiles='CartoDB dark_matter',
            prefer_canvas=True,
            control_scale=True
        )
        
        # ⭐ FUNCIONALIDADES ÉPICAS
        
        # 1. Pantalla completa
        folium.plugins.Fullscreen(
            position='topleft',
            title='🖥️ Pantalla Completa',
            title_cancel='❌ Salir',
            force_separate_button=True
        ).add_to(m)
        
        # 2. Medidor de distancias
        folium.plugins.MeasureControl(
            position='bottomright',
            primary_length_unit='kilometers',
            secondary_length_unit='meters',
            primary_area_unit='hectares'
        ).add_to(m)
        
        # 3. Minimapa épico
        minimap = plugins.MiniMap(
            tile_layer='CartoDB positron',
            position='bottomleft',
            width=150,
            height=150,
            collapsed=False
        )
        m.add_child(minimap)
        
        # 4. Coordenadas del cursor
        folium.plugins.MousePosition(
            position='topright',
            separator=' | ',
            empty_string='Coordenadas: N/A',
            lng_first=True,
            num_digits=4,
            prefix='📍 '
        ).add_to(m)
        
        return m
    
    def add_epic_hospitals(self, map_obj: folium.Map, hospitals_data: pd.DataFrame) -> folium.Map:
        """Añadir hospitales con marcadores épicos y popups interactivos"""
        
        # Crear grupo de capas para hospitales
        hospital_layer = folium.FeatureGroup(name="🏥 Hospitales")
        
        for idx, hospital in hospitals_data.iterrows():
            # Determinar color y tamaño según tipo
            color = self.hospital_colors.get(hospital.get('tipo_centro', 'Desconocido'), '#95a5a6')
            
            # Tamaño basado en número de camas
            camas_raw = hospital.get('camas_funcionamiento_2025', 0)
            camas = int(camas_raw) if isinstance(camas_raw, (int, float)) and camas_raw is not None else 0
            if camas > 1000:
                radius = 25
                icon_size = 'large'
            elif camas > 500:
                radius = 20
                icon_size = 'medium'
            else:
                radius = 15
                icon_size = 'small'
            
            # 🎨 POPUP ÉPICO CON INFORMACIÓN COMPLETA
            popup_html = f"""
            <div style="width: 300px; font-family: Arial;">
                <div style="background: linear-gradient(135deg, {color}, {color}cc); color: white; padding: 10px; border-radius: 10px 10px 0 0;">
                    <h3 style="margin: 0; font-size: 16px;">🏥 {hospital.get('nombre', 'N/A')}</h3>
                    <p style="margin: 5px 0; opacity: 0.9;">{hospital.get('tipo_centro', 'N/A')}</p>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 0 0 10px 10px; border: 2px solid {color};">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <strong>📍 Ubicación:</strong><br>
                            {hospital.get('municipio', 'N/A')}<br>
                            <small>{hospital.get('distrito_sanitario', 'N/A')}</small>
                        </div>
                        <div>
                            <strong>🛏️ Capacidad:</strong><br>
                            {hospital.get('camas_funcionamiento_2025', 'N/A')} camas<br>
                            <small>{hospital.get('personal_sanitario_2025', 'N/A')} profesionales</small>
                        </div>
                    </div>
                    
                    <hr style="border: 1px solid {color}; margin: 10px 0;">
                    
                    <div>
                        <strong>👥 Población Referencia:</strong><br>
                        {f"{hospital.get('poblacion_referencia_2025', 0):,}" if isinstance(hospital.get('poblacion_referencia_2025'), (int, float)) and hospital.get('poblacion_referencia_2025') != 'N/A' else 'N/A'} habitantes
                    </div>
                    
                    <div style="margin-top: 10px;">
                        <strong>🚨 Urgencias 24h:</strong> 
                        {'✅ SÍ' if hospital.get('urgencias_24h', False) else '❌ NO'}
                    </div>
                    
                    <div style="margin-top: 10px;">
                        <strong>🏥 UCI:</strong> 
                        {hospital.get('uci_camas', 0)} camas
                    </div>
                </div>
            </div>
            """
            
            # 🎯 MARCADOR ÉPICO
            folium.CircleMarker(
                location=[hospital.get('latitud', 0), hospital.get('longitud', 0)],
                radius=radius,
                popup=folium.Popup(popup_html, max_width=320),
                color='white',
                weight=3,
                fillColor=color,
                fillOpacity=0.9,
                tooltip=f"🏥 {hospital.get('nombre', 'N/A')} | 🛏️ {hospital.get('camas_funcionamiento_2025', 'N/A')} camas"
            ).add_to(hospital_layer)
            
            # ⭐ ICONO ADICIONAL PARA HOSPITALES GRANDES
            if camas > 800:
                folium.Marker(
                    location=[hospital.get('latitud', 0), hospital.get('longitud', 0)],
                    icon=folium.Icon(color='red', icon='plus-sign', prefix='fa'),
                    tooltip="🏥 Hospital Principal"
                ).add_to(hospital_layer)
        
        map_obj.add_child(hospital_layer)
        return map_obj
    
    def add_epic_municipalities(self, map_obj: folium.Map, demographics_data: pd.DataFrame) -> folium.Map:
        """Añadir municipios con círculos proporcionales a población"""
        
        municipalities_layer = folium.FeatureGroup(name="🏘️ Municipios")
        
        for idx, muni in demographics_data.iterrows():
            población = muni['poblacion_2025']
            crecimiento = muni['crecimiento_2024_2025']
            
            # Coordenadas aproximadas de municipios principales
            coords = self.get_municipality_coords(muni['municipio'])
            if not coords:
                continue
            
            # Tamaño proporcional a población
            radius = max(5, min(30, población / 10000))
            
            # Color basado en crecimiento
            if crecimiento > 1000:
                color = '#27ae60'  # Verde para alto crecimiento
                opacity = 0.8
            elif crecimiento > 0:
                color = '#f39c12'  # Naranja para crecimiento moderado
                opacity = 0.6
            else:
                color = '#e74c3c'  # Rojo para decrecimiento
                opacity = 0.4
            
            # 🎨 POPUP MUNICIPAL ÉPICO
            popup_municipal = f"""
            <div style="width: 280px; font-family: Arial;">
                <div style="background: linear-gradient(135deg, {color}, {color}aa); color: white; padding: 10px; border-radius: 10px 10px 0 0;">
                    <h3 style="margin: 0;">🏘️ {muni['municipio']}</h3>
                    <p style="margin: 5px 0; opacity: 0.9;">Provincia de Málaga</p>
                </div>
                
                <div style="background: white; padding: 15px; border-radius: 0 0 10px 10px; border: 2px solid {color};">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <strong>👥 Población 2025:</strong><br>
                            {f"{población:,}" if isinstance(población, (int, float)) else población} habitantes
                        </div>
                        <div>
                            <strong>📈 Crecimiento:</strong><br>
                            {'+' if crecimiento >= 0 else ''}{crecimiento:,}
                        </div>
                    </div>
                    
                    <hr style="border: 1px solid {color}; margin: 10px 0;">
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px;">
                        <div>
                            <strong>📊 Densidad:</strong><br>
                            {muni['densidad_hab_km2_2025']:.1f} hab/km²
                        </div>
                        <div>
                            <strong>💰 Renta:</strong><br>
                            {muni['renta_per_capita_2024']:,}€/año
                        </div>
                    </div>
                    
                    <div style="margin-top: 10px;">
                        <strong>👴 Índice Envejecimiento:</strong> {muni['indice_envejecimiento_2025']:.1f}
                    </div>
                </div>
            </div>
            """
            
            # Círculo proporcional épico
            folium.CircleMarker(
                location=coords,
                radius=radius,
                popup=folium.Popup(popup_municipal, max_width=300),
                color='white',
                weight=2,
                fillColor=color,
                fillOpacity=opacity,
                tooltip=f"🏘️ {muni['municipio']} | 👥 {población:,} hab"
            ).add_to(municipalities_layer)
        
        map_obj.add_child(municipalities_layer)
        return map_obj
    
    def create_accessibility_heatmap(self, map_obj: folium.Map, accessibility_data: pd.DataFrame) -> folium.Map:
        """Crear heatmap épico de accesibilidad"""
        
        # Procesar datos de accesibilidad
        heat_data = []
        
        for idx, row in accessibility_data.iterrows():
            municipio = row['municipio_origen']
            tiempo = row['tiempo_coche_minutos']
            
            coords = self.get_municipality_coords(municipio)
            if coords:
                # Intensidad inversa al tiempo (menor tiempo = mayor intensidad)
                intensity = max(0.1, 1 - (tiempo / 120))  # Normalizar a 0-1
                heat_data.append([coords[0], coords[1], intensity])
        
        # Crear heatmap
        if heat_data:
            heatmap_layer = folium.FeatureGroup(name="🔥 Heatmap Accesibilidad")
            
            folium.plugins.HeatMap(
                heat_data,
                name="Accesibilidad Sanitaria",
                min_opacity=0.3,
                max_zoom=18,
                radius=25,
                blur=15,
                gradient={
                    0.0: '#e74c3c',    # Rojo (baja accesibilidad)
                    0.3: '#f39c12',    # Naranja
                    0.6: '#f1c40f',    # Amarillo
                    1.0: '#27ae60'     # Verde (alta accesibilidad)
                }
            ).add_to(heatmap_layer)
            
            map_obj.add_child(heatmap_layer)
        
        return map_obj
    
    def add_service_coverage_circles(self, map_obj: folium.Map, hospitals_data: pd.DataFrame, services_data: pd.DataFrame) -> folium.Map:
        """Añadir círculos de cobertura de servicios especializados"""
        
        # Crear capas para cada especialidad
        for specialty in ['cardiologia', 'neurologia', 'oncologia_medica', 'pediatria']:
            if specialty not in services_data.columns:
                continue
            
            specialty_layer = folium.FeatureGroup(name=f"💊 {specialty.replace('_', ' ').title()}")
            
            # Hospitales con esta especialidad
            hospitals_with_specialty = services_data[services_data[specialty] == True]
            
            for idx, service_row in hospitals_with_specialty.iterrows():
                # Encontrar hospital correspondiente
                hospital_row = hospitals_data[hospitals_data['nombre'].str.contains(
                    service_row['centro_sanitario'].replace('Hospital ', '').replace('CAR ', ''), na=False
                )]
                
                if not hospital_row.empty:
                    hospital = hospital_row.iloc[0]
                    color = self.specialty_colors.get(specialty, '#95a5a6')
                    
                    # Círculo de cobertura (radio de 30km aproximadamente)
                    folium.Circle(
                        location=[hospital.get('latitud', 0), hospital.get('longitud', 0)],
                        radius=30000,  # 30km en metros
                        popup=f"💊 Cobertura {specialty.replace('_', ' ').title()}<br>🏥 {service_row['centro_sanitario']}",
                        color=color,
                        weight=2,
                        fillColor=color,
                        fillOpacity=0.1,
                        tooltip=f"💊 {specialty.replace('_', ' ').title()}"
                    ).add_to(specialty_layer)
            
            map_obj.add_child(specialty_layer)
        
        return map_obj
    
    def add_epic_routes(self, map_obj: folium.Map, accessibility_data: pd.DataFrame) -> folium.Map:
        """Añadir rutas épicas entre municipios y hospitales"""
        
        routes_layer = folium.FeatureGroup(name="🛣️ Rutas Principales")
        
        # Seleccionar algunas rutas importantes para mostrar
        important_routes = accessibility_data[
            (accessibility_data['tiempo_coche_minutos'] > 45) |
            (accessibility_data['municipio_origen'].isin(['Marbella', 'Vélez-Málaga', 'Antequera', 'Ronda']))
        ]
        
        for idx, route in important_routes.iterrows():
            municipio_coords = self.get_municipality_coords(route['municipio_origen'])
            hospital_coords = self.get_hospital_coords(route['hospital_destino'])
            
            if municipio_coords and hospital_coords:
                tiempo = route['tiempo_coche_minutos']
                
                # Color de ruta según tiempo
                if tiempo > 60:
                    color = '#e74c3c'  # Rojo para rutas largas
                    weight = 4
                elif tiempo > 45:
                    color = '#f39c12'  # Naranja para rutas medias
                    weight = 3
                else:
                    color = '#27ae60'  # Verde para rutas cortas
                    weight = 2
                
                # Crear línea de ruta
                folium.PolyLine(
                    locations=[municipio_coords, hospital_coords],
                    weight=weight,
                    color=color,
                    opacity=0.7,
                    popup=f"🛣️ {route['municipio_origen']} → {route['hospital_destino']}<br>⏱️ {tiempo} min<br>💰 {route['coste_transporte_euros']:.2f}€",
                    tooltip=f"⏱️ {tiempo} min"
                ).add_to(routes_layer)
        
        map_obj.add_child(routes_layer)
        return map_obj
    
    def get_municipality_coords(self, municipio: str) -> Tuple[float, float]:
        """Obtener coordenadas aproximadas de municipios principales"""
        coords_map = {
            'Málaga': [36.7213, -4.4214],
            'Marbella': [36.5108, -4.8856],
            'Vélez-Málaga': [36.7875, -4.1017],
            'Fuengirola': [36.5297, -4.6262],
            'Mijas': [36.5908, -4.6386],
            'Torremolinos': [36.6201, -4.4996],
            'Benalmádena': [36.5988, -4.6219],
            'Antequera': [37.0179, -4.5613],
            'Ronda': [36.7427, -5.1658],
            'Estepona': [36.4270, -5.1448],
            'Nerja': [36.7576, -3.8739],
            'Rincón de la Victoria': [36.7175, -4.2717],
            'Coín': [36.6598, -4.7539],
            'Alhaurín de la Torre': [36.6583, -4.5611]
        }
        return coords_map.get(municipio, None)
    
    def get_hospital_coords(self, hospital_name: str) -> Tuple[float, float]:
        """Obtener coordenadas de hospitales"""
        hospital_coords = {
            'Hospital Regional Málaga': [36.7213, -4.4192],
            'Hospital Costa del Sol': [36.5108, -4.8856],
            'Hospital Axarquía': [36.7875, -4.1017],
            'Hospital Antequera': [37.0179, -4.5613],
            'Hospital Ronda': [36.7427, -5.1658]
        }
        
        # Buscar coincidencias parciales
        for key, coords in hospital_coords.items():
            if any(word in hospital_name for word in key.split()):
                return coords
        
        return None
    
    def create_epic_control_panel(self, map_obj: folium.Map) -> folium.Map:
        """Añadir panel de control épico con leyenda"""
        
        # Control de capas personalizado
        folium.LayerControl(
            position='topright',
            collapsed=False,
            autoZIndex=True
        ).add_to(map_obj)
        
        # Leyenda épica con clases CSS
        legend_html = '''
        <div class="map-legend">
            <div class="map-legend-header">
                <h4>🗺️ Leyenda Sanitaria</h4>
            </div>
            
            <div class="map-legend-content">
                <p><b>🏥 Tipos de Centros:</b></p>
                <p><span style="color: #e74c3c;">●</span> Hospital Regional</p>
                <p><span style="color: #3498db;">●</span> Hospital Universitario</p>
                <p><span style="color: #f39c12;">●</span> Hospital Comarcal</p>
                <p><span style="color: #27ae60;">●</span> Centro Alta Resolución</p>
                
                <hr>
                
                <p><b>🏘️ Municipios:</b></p>
                <p><span style="color: #27ae60;">●</span> Crecimiento Alto</p>
                <p><span style="color: #f39c12;">●</span> Crecimiento Medio</p>
                <p><span style="color: #e74c3c;">●</span> Decrecimiento</p>
                
                <hr>
                
                <p><b>🛣️ Rutas:</b></p>
                <p><span style="color: #27ae60;">━</span> < 45 min</p>
                <p><span style="color: #f39c12;">━</span> 45-60 min</p>
                <p><span style="color: #e74c3c;">━</span> > 60 min</p>
            </div>
        </div>
        '''
        
        map_obj.get_root().html.add_child(folium.Element(legend_html))
        
        return map_obj
    
    def create_epic_complete_map(self, hospitals_data: pd.DataFrame, demographics_data: pd.DataFrame, 
                               services_data: pd.DataFrame, accessibility_data: pd.DataFrame) -> folium.Map:
        """Crear mapa épico completo con todas las funcionalidades"""
        
        # 1. Crear mapa base épico
        epic_map = self.create_epic_base_map()
        
        # 2. Añadir todas las capas épicas
        epic_map = self.add_epic_hospitals(epic_map, hospitals_data)
        epic_map = self.add_epic_municipalities(epic_map, demographics_data)
        epic_map = self.create_accessibility_heatmap(epic_map, accessibility_data)
        epic_map = self.add_service_coverage_circles(epic_map, hospitals_data, services_data)
        epic_map = self.add_epic_routes(epic_map, accessibility_data)
        
        # 3. Añadir controles épicos
        epic_map = self.create_epic_control_panel(epic_map)
        
        # 4. Añadir título épico
        title_html = '''
        <div class="map-epic-title">
            <h3>🏥 Mapa Interactivo - Sistema Sanitario Málaga</h3>
            <p>Análisis Geoespacial Avanzado | 2025</p>
        </div>
        '''
        
        epic_map.get_root().html.add_child(folium.Element(title_html))
        
        return epic_map