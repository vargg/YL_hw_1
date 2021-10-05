from itertools import permutations
from typing import List, Tuple


class Point:
    def __init__(self, x: int, y: int, address: str) -> None:
        self.x = x
        self.y = y
        self.address = address

    def __repr__(self) -> str:
        return (
            f'{self.__class__.__name__}(x={self.x}, y={self.y}, '
            f'address={self.address})'
        )

    def __str__(self) -> str:
        return self.address


class Navigation:
    def __init__(self, base_point: Point) -> None:
        self._base_point: Point = base_point
        self._other_points: List[Point] = list()

    def add_point(self, point: Point) -> None:
        self._other_points.append(point)

    def get_points_qty(self) -> int:
        return len(self._other_points)

    def get_full_route(self, bruteforce: bool = False) -> str:
        if bruteforce:
            route, distances = self._iterating_all_options()
        else:
            route, distances = self._greedy_search()
        result: List[str] = [str((route[0].x, route[0].y)), '->']
        for i in range(1, len(route)):
            result.append(str((route[i].x, route[i].y)))
            result.append(str([round(sum(distances[:i]), 3)]))
            result.append('->')
        result.pop()
        result.extend(['=', str(round(sum(distances), 3))])
        return ' '.join(result)

    def _greedy_search(self) -> Tuple[List[Point], List[float]]:
        route = [self._base_point]
        route_distances = list()
        unused_points = self._other_points.copy()
        while len(unused_points) > 0:
            distances = [
                self._calc_distance(route[-1], pnt) for pnt in unused_points
            ]
            min_dist_index = self._find_min_dist(distances)
            route.append(unused_points.pop(min_dist_index))
            route_distances.append(distances[min_dist_index])
        route_distances.append(
            self._calc_distance(route[-1], self._base_point)
        )
        route.append(self._base_point)
        return route, route_distances

    def _iterating_all_options(self) -> Tuple[List[Point], List[float]]:
        all_routes = self._generate_routes()
        routes_distances = list()
        for route in all_routes:
            distance = list()
            for i in range(len(route) - 1):
                distance.append(self._calc_distance(route[i], route[i + 1]))
            routes_distances.append(distance)
        min_dist_index = self._find_min_dist(routes_distances, many=True)
        return all_routes[min_dist_index], routes_distances[min_dist_index]

    def _find_min_dist(
        self, distances: List[List[int]], many: bool = False
    ) -> int:

        min_index = 0
        if many:
            min_dist = sum(distances[min_index])
        else:
            min_dist = distances[min_index]
        for i in range(len(distances)):
            if many:
                route_distance = sum(distances[i])
            else:
                route_distance = distances[i]
            if route_distance < min_dist:
                min_index = i
                min_dist = route_distance
        return min_index

    def _generate_routes(self) -> List[List[Point]]:
        sequences = permutations(
            [x for x in range(self.get_points_qty())]
        )
        all_routes = list()
        for seq in sequences:
            route = [self._base_point]
            for i in seq:
                route.append(self._other_points[i])
            route.append(self._base_point)
            all_routes.append(route)
        return all_routes

    def _calc_distance(self, first_point: Point, second_point: Point) -> float:
        dx = first_point.x - second_point.x
        dy = first_point.y - second_point.y
        return (dx**2 + dy**2)**0.5


if __name__ == '__main__':
    base = (0, 2, 'Почтовое отделение')
    points = (
        (2, 5, 'ул. Грибоедова, 104/25'),
        (5, 2, 'ул. Бейкер-стрит, 221б'),
        (6, 6, 'ул. Большая садовая, 302-бис'),
        (8, 3, 'ул. Вечнозелёная аллея, 742'),
    )
    nvg = Navigation(Point(base[0], base[1], base[2]))
    for pnt in points:
        nvg.add_point(Point(pnt[0], pnt[1], pnt[2]))
    print(nvg.get_full_route())
    print(nvg.get_full_route(True))
