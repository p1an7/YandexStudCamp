import heapq

def dijkstra(graph, start):
    # Инициализация расстояний до всех вершин
    distances = {vertex: float('infinity') for vertex in graph}
    distances[start] = 0  # Расстояние до стартовой вершины равно 0

    # Используем приоритетную очередь для хранения вершин
    priority_queue = [(0, start)]  # (расстояние, вершина)

    while priority_queue:
        current_distance, current_vertex = heapq.heappop(priority_queue)

        # Если текущее расстояние больше, чем уже найденное, пропускаем
        if current_distance > distances[current_vertex]:
            continue

        # Обходим соседние вершины
        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            # Если найдено более короткое расстояние
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances

# Пример графа в виде словаря
graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1}
}

# Запуск алгоритма Дейкстры
start_vertex = 'D'
distances = dijkstra(graph, start_vertex)

# Вывод результатов
print(f"Кратчайшие расстояния от вершины '{start_vertex}':")
for vertex, distance in distances.items():
    print(f"До {vertex}: {distance}")
