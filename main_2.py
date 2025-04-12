# #!python 3.13

# # import geopandas as gpd # Работа с геоданными
# # import pandas as pd
# # import numpy as np
# # import json
# # import h3  # Работа с H3-геоидами
# # import folium  # Визуализация на карте
# # import osmnx as ox # Загрузка данных OpenStreetMap
# # from shapely import wkt
# # from folium.plugins import HeatMap
# # from shapely.geometry import Polygon # Работа с геометрией

# # # Настройки OSMnx для кеширования запросов
# # ox.settings.use_cache = True
# # ox.settings.log_console = True

# # def visualize_hexagons(hexagons, color="grey", folium_map=None):
# #     """
# #     Визуализирует H3-гексагоны на карте Folium.
    
# #     Параметры:
# #         hexagons (list): Список H3-идентификаторов
# #         color (str): Цвет границ гексагонов
# #         folium_map (folium.Map): Существующая карта для добавления слоя
    
# #     Возвращает:
# #         folium.Map: Объект карты с отрисованными гексагонами
# #     """
# #     polylines = []  # Список для хранения полигонов
# #     lat_coords = []  # Широты для расчета центра
# #     lng_coords = []  # Долготы для расчета центра

# #     # Обрабатываем каждый гексагон
# #     for hex_id in hexagons:
# #         # Получаем границы гексагона
# #         boundary = h3.cell_to_boundary(hex_id)
        
# #         # Преобразуем кортежи в списки
# #         boundary_coords = [list(coord) for coord in boundary]
        
# #         # Замыкаем полигон, добавляя первую точку в конец
# #         closed_polygon = boundary_coords + [boundary_coords[0]]
        
# #         # Собираем координаты для центра карты
# #         for coord in closed_polygon:
# #             lat_coords.append(coord[0])
# #             lng_coords.append(coord[1])
        
# #         polylines.append(closed_polygon)

# #     # Создаем новую карту если не передана существующая
# #     if folium_map is None:
# #         # Рассчитываем центр как среднее координат или используем значения по умолчанию
# #         map_center = (
# #             [sum(lat_coords)/len(lat_coords), sum(lng_coords)/len(lng_coords)] 
# #             if lat_coords and lng_coords 
# #             else [45.035470, 38.975313]  # Координаты Краснодара
# #         )
        
# #         folium_map = folium.Map(
# #             location=map_center,
# #             zoom_start=14,
# #             tiles='cartodbpositron'  # Стиль карты
# #         )

# #     # Добавляем полигоны на карту
# #     for polygon in polylines:
# #         folium.PolyLine(
# #             locations=polygon,
# #             weight=3,  # Толщина линии
# #             color=color,
# #             opacity=0.8,
# #             tooltip=f"H3-гексагон: {hex_id}"  # Всплывающая подсказка
# #         ).add_to(folium_map)

# #     return folium_map

# # def get_city_boundary(city_name):
# #     """
# #     Получает административные границы города из OSM.
    
# #     Параметры:
# #         city_name (str): Название города на русском языке
    
# #     Возвращает:
# #         GeoDataFrame: Геоданные с границами города
# #     """
# #     try:
# #         # Загружаем данные административных границ
# #         gdf = ox.features_from_place(
# #             f'{city_name}, Россия', 
# #             tags={'boundary': 'administrative'}
# #         )
        
# #         # Фильтруем городской округ
# #         filtered = gdf[
# #             (gdf['name'].str.contains(city_name, na=False)) &
# #             (gdf['admin_level'] == '6')  # Уровень для городов федерального значения
# #         ]
        
# #         if not filtered.empty:
# #             return filtered.reset_index()
            
# #         # Геокодирование
# #         return ox.geocode_to_gdf(f'{city_name}, Россия', which_result=1)
        
# #     except Exception as e:
# #         print(f'Ошибка загрузки данных: {e}')
# #         return gpd.GeoDataFrame()  # Возвращаем пустой DataFrame

# # def visualize_city_boundary(gdf):
# #     """
# #     Визуализирует границы города на карте.
    
# #     Параметры:
# #         gdf (GeoDataFrame): Геоданные с полигонами
    
# #     Возвращает:
# #         folium.Map: Карта с отрисованными границами
# #     """
# #     if gdf.empty:
# #         print("Нет данных для визуализации")
# #         return folium.Map(location=[55.751244, 37.618423], zoom_start=10)  # Москва по умолчанию
    
# #     # Создаем базовую карту
# #     centroid = gdf.union_all().centroid # Находим центр города
    
# #     m = folium.Map(
# #         location=[centroid.y, centroid.x], 
# #         zoom_start=12,
# #         tiles='cartodbpositron'
# #     )
    
# #     # Добавляем GeoJSON слой
# #     folium.GeoJson(
# #         gdf.__geo_interface__,
# #         name='Границы города',
# #         style_function=lambda x: {
# #             'fillColor': '#a1a1a1',  # Цвет заливки
# #             'color': 'red',         # Цвет границ
# #             'weight': 2              # Толщина границ
# #         },
# #         tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Город:'])
# #     ).add_to(m)
    
# #     return m

# # if __name__ == "__main__":
# #     try:
# #         # 1. Загружаем границы Краснодара
# #         krasnodar_gdf = get_city_boundary('Краснодар')
        
# #         # 2. Визуализируем границы города
# #         city_map = visualize_city_boundary(krasnodar_gdf)
        
# #         # 3. Генерируем H3-гексагон для центра города
# #         hex_id = h3.latlng_to_cell(
# #             lat=45.035470,  # Широта центра
# #             lng=38.975313,  # Долгота центра
# #             res=10 # Уровень детализации (9-15)
# #         )
        
# #         # 4. Добавляем гексагон на карту
# #         visualize_hexagons(
# #             hexagons=[hex_id],
# #             folium_map=city_map
# #         )
        
# #         # 5. Сохраняем комбинированную карту
# #         city_map.save('krasnodar_map.html')
# #         print("Карта успешно сохранена в файл krasnodar_map.html")
            
# #     except Exception as e:
# #         print(f"Критическая ошибка: {e}")
# #         # Создаем карту с координатами по умолчанию
# #         fallback_map = folium.Map(location=[55.751244, 37.618423], zoom_start=5)
# #         fallback_map.save('fallback_map.html')


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
ox.settings.use_cache = True
ox.settings.log_console = True


def visualize_hexagons(hexagons, color="grey", folium_map=None):
    """
    Визуализирует H3-гексагоны на карте Folium.

    Параметры:
        hexagons (list): Список H3-идентификаторов
        color (str): Цвет границ гексагонов
        folium_map (folium.Map): Существующая карта для добавления слоя

    Возвращает:
        folium.Map: Объект карты с отрисованными гексагонами
    """
    polylines = []  # Список для хранения полигонов
    lat_coords = []  # Широты для расчета центра
    lng_coords = []  # Долготы для расчета центра

    # Обрабатываем каждый гексагон
    for hex_id in hexagons:
        # Получаем границы гексагона
        boundary = h3.cell_to_boundary(hex_id)

        # Преобразуем кортежи в списки
        boundary_coords = [list(coord) for coord in boundary]

        # Замыкаем полигон, добавляя первую точку в конец
        closed_polygon = boundary_coords + [boundary_coords[0]]

        # Собираем координаты для центра карты
        for coord in closed_polygon:
            lat_coords.append(coord[0])
            lng_coords.append(coord[1])

        polylines.append(closed_polygon)

    # Создаем новую карту если не передана существующая
    if folium_map is None:
        # Рассчитываем центр как среднее координат или используем значения по умолчанию
        map_center = (
            [sum(lat_coords) / len(lat_coords), sum(lng_coords) / len(lng_coords)]
            if lat_coords and lng_coords
            else [45.035470, 38.975313]  # Координаты Краснодара
        )

        folium_map = folium.Map(
            location=map_center,
            zoom_start=14,
            tiles='cartodbpositron'  # Стиль карты
        )

    # Добавляем полигоны на карту
    for polygon in polylines:
        folium.PolyLine(
            locations=polygon,
            weight=3,  # Толщина линии
            color=color,
            opacity=0.8,
            tooltip=f"H3-гексагон: {hex_id}"  # Всплывающая подсказка
        ).add_to(folium_map)

    return folium_map


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
    centroid = gdf.union_all().centroid  # Находим центр города

    map_city = folium.Map(
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
            'color': 'red',  # Цвет границ
            'weight': 2  # Толщина границ
        },
        tooltip=folium.GeoJsonTooltip(fields=['name'], aliases=['Город:'])
    ).add_to(map_city)

    return map_city




def create_hexagons(geoJson):
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
    hexagons = h3.h3shape_to_cells(lat_lng_poly, res=10)  # Уровень детализации 10

    # Создаем карту
    m = folium.Map(location=[np.mean([coord[1] for coord in coordinates]), np.mean([coord[0] for coord in coordinates])],
                      zoom_start=13, tiles='cartodbpositron')

    # Визуализируем каждый гексагон
    for hex_id in hexagons:
        # Получаем LatLngPoly для данного H3 идентификатора
        polygon = h3.cells_to_h3shape([hex_id], tight=True)

        # Извлекаем координаты из объекта LatLngPoly
        outlines = polygon.outer if hasattr(polygon, 'outer') else []

        # if outlines:  # Если контуры существуют
        #     # Конвертируем кортеж в список
        #     if isinstance(outlines, tuple):
        #         outlines = list(outlines)

        # Закрываем полигон добавлением первой координаты в конец
        polyline = list(outlines) + [outlines[0]]  # Замыкаем полигон

        # Добавляем на карту
        folium.PolyLine(locations=polyline, weight=3, color='red').add_to(m)

    return m, hexagons




if __name__ == "__main__":
    try:
        # 1. Загружаем границы Краснодара
        krasnodar_gdf = get_city_boundary('Краснодар')

        # 2. Визуализируем границы города
        city_map = visualize_city_boundary(krasnodar_gdf)

        # # 3. Генерируем H3-гексагон для центра города
        # hex_id = h3.latlng_to_cell(
        #     lat=45.035470,  # Широта центра
        #     lng=38.975313,  # Долгота центра
        #     res=10  # Уровень детализации (9-15)
        # )

        # # 4. Добавляем гексагон на карту
        # visualize_hexagons(
        #     hexagons=[hex_id],
        #     folium_map=city_map
        # )

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
        m, hexagons = create_hexagons(geoJson)
        m.save("city_map.html")
        
        city_map.save("output_map.html")

        print("Карта успешно сохранена")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


# if __name__ == "__main__":
#     # 1. Загружаем границы Краснодара
#     krasnodar_gdf = get_city_boundary('Краснодар')
    
#     # 2. Создаем базовую карту
#     map_center = [45.035470, 38.975313]  # Координаты Краснодара
#     city_map = folium.Map(location=map_center, zoom_start=14, tiles='cartodbpositron')
    
#     # 3. Визуализируем границы города
#     city_map = visualize_city_boundary(krasnodar_gdf, city_map)
    
#     # 4. Генерируем GeoJSON и создаем гексагоны
#     geoJson = json.loads(krasnodar_gdf['geometry'].to_json())
#     geoJson = geoJson['features'][0]['geometry']
    
#     hexagons = create_hexagons(geoJson)
#     hex_polylines = visualize_hexagons(hexagons)

#     # 5. Добавляем гексагоны на карту
#     for polygon in hex_polylines:
#         folium.PolyLine(locations=polygon, weight=3, color='blue', opacity=0.8).add_to(city_map)

#     # 6. Сохраняем комбинированную карту
#     city_map.save('krasnodar_combined_map.html')
#     print("Карта успешно сохранена как krasnodar_combined_map.html")











# import geopandas as gpd  # Работа с геоданными
# import pandas as pd
# import numpy as np
# import json
# import h3  # Работа с H3-геоидами
# import folium  # Визуализация на карте
# import osmnx as ox  # Загрузка данных OpenStreetMap
# from shapely import wkt

# # Настройки OSMnx для кеширования запросов
# ox.settings.use_cache = True
# ox.settings.log_console = True

# # def visualize_hexagons(hexagons, color="grey"):
# #     """
# #     Визуализирует H3-гексагоны на карте Folium.
# #     Параметры:
# #         hexagons (list): Список H3-идентификаторов
# #         color (str): Цвет границ гексагонов
# #     Возвращает:
# #         list: Список полигонов для добавления на карту
# #     """
# #     polylines = []  # Список для хранения полигонов
# #     for hex_id in hexagons:
# #         # Получаем границы гексагона
# #         boundary = h3.cell_to_boundary(hex_id)
# #         boundary_coords = [list(coord) for coord in boundary]
# #         closed_polygon = boundary_coords + [boundary_coords[0]]  # Замыкаем полигон
# #         polylines.append(closed_polygon)
# #     return polylines

# def visualize_hexagons(hexagons, color="grey"):
#     """
#     Визуализирует H3-гексагоны на карте Folium.
    
#     Параметры:
#         hexagons (list): Список H3-идентификаторов
#         color (str): Цвет границ гексагонов
        
#     Возвращает:
#         list: Список полигонов для добавления на карту
#     """
#     polylines = []  # Список для хранения полигонов
    
#     for hex_id in hexagons:
#         # Получаем границы гексагона
#         boundary = h3.cell_to_boundary(hex_id)
        
#         # Подготовка координат без изменения порядка
#         boundary_coords = [(coord[1], coord[0]) for coord in boundary]  # (долгота, широта)
        
#         closed_polygon = boundary_coords + [boundary_coords[0]]  # Замыкаем полигон
#         polylines.append(closed_polygon)
        
#     return polylines



# def get_city_boundary(city_name):
#     """
#     Получает административные границы города из OSM.
#     Параметры:
#         city_name (str): Название города на русском языке
#     Возвращает:
#         GeoDataFrame: Геоданные с границами города
#     """
#     try:
#         gdf = ox.features_from_place(f'{city_name}, Россия', tags={'boundary': 'administrative'})
#         filtered = gdf[(gdf['name'].str.contains(city_name, na=False)) & (gdf['admin_level'] == '6')]
#         return filtered.reset_index() if not filtered.empty else gdf
#     except Exception as e:
#         print(f'Ошибка загрузки данных: {e}')
#         return gpd.GeoDataFrame()  # Возвращаем пустой DataFrame

# def visualize_city_boundary(gdf, folium_map):
#     """
#     Визуализирует границы города на карте.
#     Параметры:
#         gdf (GeoDataFrame): Геоданные с полигонами
#         folium_map (folium.Map): Объект карты для отрисовки границ
#     Возвращает:
#         folium.Map: Карта с отрисованными границами
#     """
#     if gdf.empty:
#         print("Нет данных для визуализации")
#         return folium_map
#     centroid = gdf.geometry.union_all().centroid  # Находим центр города
#     folium.GeoJson(
#         gdf.__geo_interface__,
#         name='Границы города',
#         style_function=lambda x: {
#             'fillColor': '#a1a1a1',  # Цвет заливки
#             'color': 'red',          # Цвет границ
#             'weight': 2              # Толщина границ
#         }
#     ).add_to(folium_map)
#     return folium_map

# def create_hexagons(geoJson):
#     """
#     Генерация H3-гексагона внутри заданного полигона.
#     Параметры:
#         geoJson (dict): GeoJSON с полигоном
#     Возвращает:
#         list: Список H3 идентификаторов
#     """
#     if geoJson['type'] != 'Polygon':
#         raise ValueError("GeoJSON must be of type 'Polygon'")
    
#     coordinates = geoJson['coordinates'][0]
#     if coordinates[0] != coordinates[-1]:
#         coordinates.append(coordinates[0])  # Замкнуть полигон
#     lat_lng_poly = h3.LatLngPoly(coordinates)
#     hexagons = h3.h3shape_to_cells(lat_lng_poly, res=10)  # Уровень детализации 10
#     return hexagons

# if __name__ == "__main__":
#     # 1. Загружаем границы Краснодара
#     krasnodar_gdf = get_city_boundary('Краснодар')
    
#     # 2. Создаем базовую карту
#     map_center = [45.035470, 38.975313]  # Координаты Краснодара
#     city_map = folium.Map(location=map_center, zoom_start=14, tiles='cartodbpositron')
    
#     # 3. Визуализируем границы города
#     city_map = visualize_city_boundary(krasnodar_gdf, city_map)
    
#     # 4. Генерируем GeoJSON и создаем гексагоны
#     geoJson = json.loads(krasnodar_gdf['geometry'].to_json())
#     geoJson = geoJson['features'][0]['geometry']
    
#     hexagons = create_hexagons(geoJson)
#     hex_polylines = visualize_hexagons(hexagons)

#     # 5. Добавляем гексагоны на карту
#     for polygon in hex_polylines:
#         folium.PolyLine(locations=polygon, weight=3, color='blue', opacity=0.8).add_to(city_map)

#     # 6. Сохраняем комбинированную карту
#     city_map.save('krasnodar_combined_map.html')
#     print("Карта успешно сохранена как krasnodar_combined_map.html")
