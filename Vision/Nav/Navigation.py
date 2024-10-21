import heapq
from collections import defaultdict

import cv2
import numpy as np
from math import sqrt, acos
from ultralytics import YOLO


class Graph:
    def __init__(self):
        self.COLOR = 'GREEN'
        self.top = YOLO('Vision/best_up.pt')
        self.main = YOLO('Vision/best-3.pt')
        self.BORDERS_INTERSECT = 1
        self.start = "START"
        self.end = "END"
        self.ball = "BALL"
        self.green_base = "GREEN_BASE"
        self.red_base = "RED_BASE"
        self.green_robot = "GREEN_ROBOT"
        self.red_robot = "RED_ROBOT"
        self.cube1 = "CUBE1"
        self.cube2 = "CUBE2"
        self.button1 = "BUTTON1"
        self.button2 = "BUTTON2"
        self.objects = [self.start, self.end, self.ball, self.cube1, self.cube2, self.button1, self.button2,
                        self.green_base, self.red_base, self.green_robot, self.red_robot]

        self.coords = {obj: [0, 0] for obj in self.objects}
        self.graph = {obj: [] for obj in self.objects}
        self.weights = {}

        self.width, self.height = 1010, 800
        self.ncols, self.nrows = 8, 6
        self.cell_width, self.cell_height = round(self.width / self.ncols), round(self.height / self.nrows)
        self.init_graph()

        frame = cv2.imread('Vision/outp.jpg')
        img = self.show_graph(frame)
        cv2.imshow('Graph', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def init_graph(self):
        self.coords[self.start] = [0, 0]
        self.coords[self.end] = [0, self.height]
        self.coords[self.ball] = [50, 50]
        self.coords[self.robot] = [60, 30]
        self.coords[self.base] = [30, 30]
        self.coords[self.enemy] = [240, 508]
        self.coords[self.cube1] = [809, 100]
        self.coords[self.cube2] = [50, 700]

        self.graph = {
            self.start: [self.end, self.ball],
            self.end: [self.ball, self.robot],
            self.ball: [self.cube1, self.cube2],
            self.robot: [self.cube1, self.cube2],
            self.cube1: [self.cube2],
            self.cube2: [self.cube2],
        }

    @staticmethod
    def getAngle(segment):
        a, b = segment
        dx = b.x - a.x
        dy = b.y - a.y
        return acos(dx / sqrt(dx ** 2 + dy ** 2))

    def astar(self, x0, y0, xf, yf, mapp):
        '''
        сочненький астар
        получает координаты точек начала и конца (0 0 в верхнем левом углу)
        возвращает координаты маршрута (только точки изменения траектории)
        '''
        x0, y0, xf, yf = x0 // 4, y0 // 4, xf // 4, yf // 4
        mapp = cv2.resize(mapp, (mapp.shape[1] // 4, mapp.shape[0] // 4))
        m, n = mapp.shape
        visited = np.zeros((m, n), dtype=int)
        dist = np.full((m, n), np.inf)
        deque = []
        argue = []

        visited[y0, x0] = 1
        dist[y0, x0] = 0
        deque.append((y0, x0))
        argue.append(0)
        flag = False

        while deque and not flag:
            temp = np.argmin(argue)
            y, x = deque[temp]
            visited[y, x] = 1
            deque.pop(temp)
            argue.pop(temp)

            for t in [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                dy, dx = t
                nx = x + dx
                ny = y + dy

                if 0 <= nx < n and 0 <= ny < m and mapp[ny][nx] != 0:  ###########'1'
                    if visited[ny, nx] != 1:
                        distance = dist[y, x] + (1.41421356 if (dx * dx + dy * dy) == 2 else 1)
                        if (ny, nx) not in deque:
                            dist[ny, nx] = min(distance, dist[ny, nx])
                            deque.append((ny, nx))
                            yy = abs(ny - yf)
                            xx = abs(nx - xf)
                            argue.append(distance + (abs(xx - yy) + 1.41421356 * min(xx, yy)))
                        else:
                            if dist[ny, nx] > distance:
                                index = deque.index((ny, nx))
                                argue[index] -= dist[ny, nx] - distance
                                dist[ny, nx] = distance
                        if ny == yf and nx == xf:
                            flag = True
                            break
        ycur, xcur = yf, xf
        ansans = []
        while ycur != y0 or xcur != x0:
            minx, miny = -1, -1
            minarg = 99999999
            for t in [(1, 0), (0, 1), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]:
                dy, dx = t
                nx = xcur + dx
                ny = ycur + dy
                if 0 <= nx < n and 0 <= ny < m and mapp[ny][nx] != 0 and dist[ny][nx] < minarg:  ###########'1'
                    minarg = dist[ny][nx]
                    minx = nx
                    miny = ny
            ycur, xcur = miny, minx
            ansans.append((xcur, ycur))
        ansansans = []
        if len(ansans) != 0:
            ansansans.append((xf * 4, yf * 4))
            for i in range(1, len(ansans) - 1):
                if ((ansans[i][0] - ansans[i - 1][0]) != (ansans[i + 1][0] - ansans[i][0])) or (
                        (ansans[i][1] - ansans[i - 1][1]) != (ansans[i + 1][1] - ansans[i][1])):
                    ansansans.append((ansans[i][0] * 4, ansans[i][1] * 4))
        return list(reversed(ansansans))

    @staticmethod
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

    def show_graph(self, frame):
        img = frame.copy()
        for vertex in self.coords.keys():
            cv2.circle(img, self.coords[vertex], 10, (0, 255, 0), -1)

        for a in self.graph.keys():
            for b in self.graph[a]:
                cv2.line(img, self.coords[a], self.coords[b], (0, 255, 0), 2)

        return img

    def get_from_yolo(self, frame, camera='Top'):
        if camera == 'Top':
            boxes = self.top.predict(frame)[0].boxes
        else:
            boxes = self.main.predict(frame)[0].boxes
        ans = defaultdict(list)
        for box in boxes:
            left, top, right, bottom = box.xyxy[0]
            ans[box.cls].append((int(left), int(top), int(right), int(bottom)))

        for cls in ans:
            ans[cls] = sorted(ans[cls], key=lambda x: ((x[0] + x[2]) // 2, (x[1] + x[3]) // 2))
        return ans

    def update_graph(self, frame):
        roi = self.get_from_yolo(frame)
        for obj in roi.keys():
            cls = obj
            left, top, right, bottom = roi[cls]
            c_x, c_y = (left + right) // 2, (top + bottom) // 2


    def get_from_mouse(self):

        pass


g = Graph()
