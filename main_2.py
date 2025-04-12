#!python 3.13

import geopandas as gpd # Работа с геоданными
import pandas as pd
import numpy as np
import json
import h3  # Работа с H3-геоидами
import folium  # Визуализация на карте
import osmnx as ox # Загрузка данных OpenStreetMap
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon # Работа с геометрией

# Настройки OSMnx для кеширования запросов
ox.settings.use_cache = True
ox.settings.log_console = True

def get_city_boundary(city_name):
    """
    Получает административные границы города из OSM.
    
    Параметры:
        city_name (str): Название города на русском языке
    
    Возвращает:
        GeoDataFrame: Геоданные с границами города
    """
    try:   
        # Геокодирование
        return ox.geocode_to_gdf(f'{city_name}, Россия', which_result=1)
        
    except Exception as e:
        print(f'Ошибка загрузки данных: {e}')
        return gpd.GeoDataFrame()  # Возвращаем пустой DataFrame

def visualize_city_boundary(gdf):
    """
    Визуализирует границы города на карте.
    
    Параметры:
        gdf (GeoDataFrame): Геоданные с полигонами
    
    Возвращает:
        folium.Map: Карта с отрисованными границами
    """
    if gdf.empty:
        print("Нет данных для визуализации")
        return folium.Map(location=[55.751244, 37.618423], zoom_start=10)  # Москва по умолчанию
    
    # Создаем базовую карту
    centroid = gdf.union_all().centroid # Находим центр города
    
    m = folium.Map(
        location=[centroid.y, centroid.x], 
        zoom_start=12,
        tiles='cartodbpositron'
    )
    
    # Добавляем GeoJSON слой
    folium.GeoJson(
        gdf.__geo_interface__,
        name='Границы города',
        style_function=lambda x: {
            'fillColor': '#a1a1a1',  # Цвет заливки
            'color': 'red',         # Цвет границ
            'weight': 2              # Толщина границ
        },
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Город:'])
    ).add_to(m)
    
    return m

if __name__ == "__main__":
    try:
        # 1. Загружаем границы Краснодара
        krasnodar_gdf = get_city_boundary('Краснодар')
        
        # 2. Визуализируем границы города
        city_map = visualize_city_boundary(krasnodar_gdf)
        
        # 3. Генерируем H3-гексагон для центра города
        hex_id = h3.latlng_to_cell(
            lat=45.035470,  # Широта центра
            lng=38.975313,  # Долгота центра
            res=10 # Уровень детализации (9-15)
        )
        
        # 4. Добавляем гексагон на карту
        visualize_hexagons(
            hexagons=[hex_id],
            folium_map=city_map
        )
        
        # 5. Сохраняем комбинированную карту
        city_map.save('krasnodar_map.html')
        print("Карта успешно сохранена в файл krasnodar_map.html")
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        # Создаем карту с координатами по умолчанию
        fallback_map = folium.Map(location=[55.751244, 37.618423], zoom_start=5)
        fallback_map.save('fallback_map.html')