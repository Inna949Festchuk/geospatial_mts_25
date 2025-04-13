#!python 3.13

import geopandas as gpd  # Работа с геоданными
import pandas as pd
import numpy as np
import json
import h3  # Работа с H3-геоидами
import folium  # Визуализация на карте
import osmnx as ox  # Загрузка данных OpenStreetMap
from shapely import wkt
from folium.plugins import HeatMap
from shapely.geometry import Polygon  # Работа с геометрией

# Настройки OSMnx для кеширования запросов
# ox.settings.use_cache = True
# ox.settings.log_console = True

def get_city_boundary(city_name):
    """
    Получает административные границы города из OSM.
    Параметры:
        city_name (str): Название города на русском языке
    Возвращает:
        GeoDataFrame: Геоданные с границами города
    """
    try:
        # Загружаем данные административных границ
        gdf = ox.features_from_place(
            f'{city_name}, Россия',
            tags={'boundary': 'administrative'}
        )

        # Фильтруем городской округ
        filtered = gdf[
            (gdf['name'].str.contains(city_name, na=False)) &
            (gdf['admin_level'] == '6')  # Уровень для городов федерального значения
        ]

        if not filtered.empty:
            return filtered.reset_index()

        # Геокодирование
        # return ox.geocode_to_gdf(f'{city_name}, Россия', which_result=1) 
        return gpd.GeoDataFrame()

    except Exception as e:
        print(f'Ошибка загрузки данных: {e}')
        return gpd.GeoDataFrame()  # Возвращаем пустой DataFrame


def visualize_city_boundary(city_gpf):
    """
    Визуализирует границы города на карте.
    Параметры:
        gdf (GeoDataFrame): Геоданные с полигонами
    Возвращает:
        folium.Map: Карта с отрисованными границами
    """
    if city_gpf.empty:
        print("Нет данных для визуализации")
        return folium.Map(location=[55.751244, 37.618423], zoom_start=10)  # Москва по умолчанию

    # Создаем базовую карту
    centroid = city_gpf.union_all().centroid  # Находим центр города

    map_city = folium.Map(
        location=[centroid.y, centroid.x],
        zoom_start=12,
        tiles='CartoDB positron', # Плитки карты остаются такими же
        name='Базовая карта', # Имя для панели слоев
        control=True
    )
    
    # Добавляем слой границ города
    city_layer = folium.FeatureGroup(name='Границы города', show=True)
    city_layer.add_to(map_city)

    # Добавляем GeoJSON в слой city_layer
    folium.GeoJson(
        city_gpf.__geo_interface__, # — это специальный интерфейс в Python, \
        # который используется для стандартизации работы с географическими \
        # данными различных геобиблиотек
        name='Границы города',  # Здесь задаете имя слоя для границ города
        style_function=lambda x: {
            'fillColor': '#a1a1a1',  # Цвет заливки
            'color': 'red',  # Цвет границ
            'weight': 5  # Толщина границ
        },
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Город:']) # Всплывающее окно
    ).add_to(city_layer)

    return map_city


def create_hexagons(geoJson, base_map):
    """
    Генерация H3-гексагона внутри заданного полигона и визуализация их на карте.
    Параметры:
        geoJson (dict): GeoJSON с полигоном
    Возвращает:
        folium.Map: Карта с визуализированными гексагонами
        hexagons (list): Список H3 идентификаторов
    """
    # Проверяем, является ли geoJson корректным полигоном
    if geoJson['type'] != 'Polygon':
        raise ValueError("GeoJSON must be of type 'Polygon'")

    # Извлекаем координаты полигона
    coordinates = geoJson['coordinates'][0]

    # Убедимся, что полигон замкнут
    if coordinates[0] != coordinates[-1]:
        coordinates.append(coordinates[0])

    # Создаем объект LatLngPoly
    lat_lng_poly = h3.LatLngPoly(coordinates)

    # Генерация H3-гексагона
    hexagons = h3.h3shape_to_cells(lat_lng_poly, res=8)  # Уровень детализации 10

    # Визуализируем гексагоны

    # Создаем слой гексагонов
    layer_hexagon = folium.FeatureGroup(name=f'Гексагоны', show=True)
    layer_hexagon.add_to(base_map)

    for hex_id in hexagons:
        # Получаем LatLngPoly для данного H3 идентификатора
        polygon = h3.cells_to_h3shape([hex_id], tight=True)

        # Извлекаем координаты из объекта LatLngPoly
        outlines = polygon.outer if hasattr(polygon, 'outer') else []

        # Закрываем полигон добавлением первой координаты в конец
        polyline = list(outlines) + [outlines[0]]  # Замыкаем полигон

        # Добавляем на карту
        map_hexagon = folium.PolyLine(locations=polyline, weight=3, color='grey').add_to(layer_hexagon)

    
    return hexagons, map_hexagon

if __name__ == "__main__":
    try:
        # 1. Загружаем границы Краснодара
        krasnodar_gdf = get_city_boundary('Краснодар')

        # 2. Визуализируем границы города
        city_map = visualize_city_boundary(krasnodar_gdf)

        # 5. Генерируем гексагоны внутри полигона Краснодара
        geoJson = json.loads(gpd.GeoSeries(krasnodar_gdf['geometry']).to_json())
        geoJson = geoJson['features'][0]['geometry']
        geoJson = {
            'type': 'Polygon',
            'coordinates': [
                np.column_stack((
                    np.array(geoJson['coordinates'][0])[:, 1],
                    np.array(geoJson['coordinates'][0])[:, 0]
                )).tolist()
            ]
        }

        # Вызов функции для создания гексагонов
        create_hexagons(geoJson, city_map)
        
        # Кнопка управления слоями
        folium.LayerControl().add_to(city_map)
        
        city_map.save("output_map.html")

        print("Карта успешно сохранена")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


