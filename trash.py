# # Импортируем необходимые библиотеки
# import osmnx as ox
# import geopandas as gpd
# from shapely.geometry import Polygon
# import matplotlib.pyplot as plt
# from descartes import PolygonPatch
# import numpy as np
# import math

# # Задаем название города
# city = 'Москва'

# # Загружаем данные карты города из OpenStreetMap (OSM)
# graph = ox.graph_from_place(city, network_type='all')

# # Преобразуем граф в GeoDataFrame для работы с геометрическими данными
# nodes, edges = ox.graph_to_gdfs(graph)

# # Получаем границы города в виде выпуклой оболочки (convex hull)
# boundaries = nodes.unary_union.convex_hull

# # Визуализируем границы города
# fig, ax = plt.subplots(figsize=(10, 10))  # Создаем фигуру и ось для графика
# gpd.GeoSeries(boundaries).plot(ax=ax, color='blue', alpha=0.5)  # Отображаем границу
# plt.axis('off')  # Скрываем оси
# plt.title(f'Границы {city}')  # Заголовок графика
# plt.show()  # Показываем график

# # Функция для генерации гексагональной сетки внутри заданного полигона
# def generate_hex_grid(boundary_polygon, cell_size=1000):
#     """
#     Генерирует гексагональную сетку внутри заданного полигона.
#     :param boundary_polygon: Полигон границ города
#     :param cell_size: Размер стороны гексагона в метрах
#     :return: Список гексагонов
#     """
    
#     # Рассчитываем границы полигона
#     min_x, min_y, max_x, max_y = boundary_polygon.bounds
#     width = max_x - min_x
#     height = max_y - min_y
    
#     # Определяем количество гексагонов по осям X и Y
#     n_cols = int(math.ceil(width / (cell_size * 3**0.5)))
#     n_rows = int(math.ceil(height / (cell_size * 1.5)))

#     # Создаем список для хранения гексагонов
#     grid = []
    
#     # Циклы для генерации гексагонов
#     for i in range(n_rows):
#         for j in range(n_cols):
#             x = min_x + j * cell_size * 3**0.5  # Расчет координаты x
#             y = min_y + i * cell_size * 1.5  # Расчет координаты y
            
#             # Смещение для нечетных рядов
#             if i % 2 == 1:
#                 x += cell_size * 3**0.5 / 2
            
#             # Создание координат для одного гексагона
#             hexagon = Polygon([
#                 (x, y),
#                 (x + cell_size * 3**0.5 / 2, y + cell_size * 0.75),
#                 (x + cell_size * 3**0.5, y + cell_size * 0.75),
#                 (x + cell_size * 3**0.5, y - cell_size * 0.75),
#                 (x + cell_size * 3**0.5 / 2, y - cell_size * 0.75),
#                 (x, y)
#             ])

#             # Проверка пересечения гексагона с границей города
#             if hexagon.intersects(boundary_polygon):
#                 grid.append(hexagon)  # Добавляем гексагон в сетку

#     return grid  # Возвращаем список гексагонов

# # Генерируем гексагональную сетку с размером 500 метров
# hexagons = generate_hex_grid(boundaries, cell_size=500)

# # Функция для вычисления оценки гексагона на подходящесть для кофейни
# def calculate_coffee_shop_score(hexagon, population_density, pois):
#     """
#     Вычисляет оценку пригодности гексагона для размещения кофейни.
#     :param hexagon: Гексагон для анализа
#     :param population_density: Плотность населения в районе
#     :param pois: Точки интереса (POI), такие как магазины, офисы и т.д.
#     :return: Оценка от 0 до 1
#     """
#     score = 0
#     # Расчет оценки на основе плотности населения и близости POI
#     # Здесь вставьте вашу логику расчета оценки
    
#     return score  # Возвращаем рассчитанную оценку

# # Список для хранения лучших гексагонов
# best_hexagons = []

# # Вычисляем оценки для каждого гексагона
# for hexagon in hexagons:
#     score = calculate_coffee_shop_score(hexagon, population_density, pois)
#     best_hexagons.append((score, hexagon))  # Добавляем кортеж (оценка, гексагон)

# # Сортируем гексагоны по оценкам
# best_hexagons.sort(key=lambda x: x[0], reverse=True)

# # Визуализируем лучшие гексагоны
# plt.figure(figsize=(10, 10))  # Создаем новую фигуру
# ax = plt.axes()

# # Отображаем границы города
# gpd.GeoSeries(boundaries).plot(ax=ax, facecolor="none", edgecolor="black")

# # Отображаем гексагоны с лучшими оценками
# for score, hexagon in best_hexagons[:10]:  # Берем лучшие 10 гексагонов
#     patch = PolygonPatch(hexagon, fc="green", ec="black", alpha=0.5, zorder=2)  # Создаем патч гексагона
#     ax.add_patch(patch)  # Добавляем патч на график

# plt.show()  # Показываем график

# Импортируем необходимые библиотеки
import osmnx as ox
import geopandas as gpd
from shapely.geometry import Polygon
import matplotlib.pyplot as plt
from descartes import PolygonPatch
import numpy as np
import math

# Задаем название города
city = 'Калининград'

# Загружаем данные карты города из OpenStreetMap (OSM)
graph = ox.graph_from_place(city, network_type='all')

# Преобразуем граф в GeoDataFrame для работы с геометрическими данными
nodes, edges = ox.graph_to_gdfs(graph)

# Получаем границы города в виде выпуклой оболочки (convex hull)
boundaries = nodes.unary_union.convex_hull

# Визуализируем границы города
fig, ax = plt.subplots(figsize=(10, 10))  # Создаем фигуру и ось для графика
gpd.GeoSeries(boundaries).plot(ax=ax, color='blue', alpha=0.5)  # Отображаем границу
plt.axis('off')  # Скрываем оси
plt.title(f'Границы {city}')  # Заголовок графика
plt.show()  # Показываем график

# Функция для генерации гексагональной сетки внутри заданного полигона
def generate_hex_grid(boundary_polygon, cell_size=1000):
    """
    Генерирует гексагональную сетку внутри заданного полигона.
    :param boundary_polygon: Полигон границ города
    :param cell_size: Размер стороны гексагона в метрах
    :return: Список гексагонов
    """
    # Рассчитываем границы полигона
    min_x, min_y, max_x, max_y = boundary_polygon.bounds
    width = max_x - min_x
    height = max_y - min_y

    # Определяем количество гексагонов по осям X и Y
    n_cols = int(math.ceil(width / (cell_size * 3**0.5)))
    n_rows = int(math.ceil(height / (cell_size * 1.5)))

    # Создаем список для хранения гексагонов
    grid = []

    # Циклы для генерации гексагонов
    for i in range(n_rows):
        for j in range(n_cols):
            x = min_x + j * cell_size * 3**0.5  # Расчет координаты x
            y = min_y + i * cell_size * 1.5  # Расчет координаты y

            # Смещение для нечетных рядов
            if i % 2 == 1:
                x += cell_size * 3**0.5 / 2

            # Создание координат для одного гексагона
            hexagon = Polygon([
                (x, y),
                (x + cell_size * 3**0.5 / 2, y + cell_size * 0.75),
                (x + cell_size * 3**0.5, y + cell_size * 0.75),
                (x + cell_size * 3**0.5, y - cell_size * 0.75),
                (x + cell_size * 3**0.5 / 2, y - cell_size * 0.75),
                (x, y)
            ])

            # Проверка пересечения гексагона с границей города
            if hexagon.intersects(boundary_polygon):
                grid.append(hexagon)  # Добавляем гексагон в сетку

    return grid  # Возвращаем список гексагонов

# Генерируем гексагональную сетку с размером 500 метров
hexagons = generate_hex_grid(boundaries, cell_size=500)

# Функция для вычисления оценки гексагона на подходящесть для кофейни
def calculate_coffee_shop_score(hexagon, population_density, pois):
    """
    Вычисляет оценку пригодности гексагона для размещения кофейни.
    :param hexagon: Гексагон для анализа
    :param population_density: Плотность населения в районе
    :param pois: Точки интереса (POI), такие как магазины, офисы и т.д.
    :return: Оценка от 0 до 1
    """
    score = 0
    # Простой расчет: учитываем количество POI внутри гексагона
    pois_within_hexagon = pois[pois.within(hexagon)].shape[0]
    population_score = population_density  # Предположим, у нас есть плотность населения
    
    # Логика расчета оценки
    score = (pois_within_hexagon * 0.5 + population_score * 0.5) / (population_density + 1)  # Нормализуем оценку

    return score  # Возвращаем рассчитанную оценку

# Пример данных плотности населения и точек интереса (POI)
# Следует заменить на реальные данные
population_density = 1500  # Пример плотности населения (человек на квадратный км)
pois = gpd.GeoDataFrame({'geometry': [Polygon(np.random.rand(4, 2)) for _ in range(20)]})  # Случайные POI

# Список для хранения лучших гексагонов
best_hexagons = []

# Вычисляем оценки для каждого гексагона
for hexagon in hexagons:
    score = calculate_coffee_shop_score(hexagon, population_density, pois)
    best_hexagons.append((score, hexagon))  # Добавляем кортеж (оценка, гексагон)

# Сортируем гексагоны по оценкам
best_hexagons.sort(key=lambda x: x[0], reverse=True)

# Визуализируем лучшие гексагоны
plt.figure(figsize=(10, 10))  # Создаем новую фигуру
ax = plt.axes()

# Отображаем границы города
gpd.GeoSeries(boundaries).plot(ax=ax, facecolor="none", edgecolor="black")

# Отображаем гексагоны с лучшими оценками
for score, hexagon in best_hexagons[:10]:  # Берем лучшие 10 гексагонов
    patch = PolygonPatch(hexagon, fc="green", ec="black", alpha=0.5, zorder=2)  # Создаем патч гексагона
    ax.add_patch(patch)  # Добавляем патч на график

plt.show()  # Показываем график

