class PointMapException(Exception):
    pass


class Point(object):
    def __init__(self, x, y, value, stratum=None, is_border=False):
        self.x = x
        self.y = y
        self.value = value
        self.stratum = stratum
        self.is_border = is_border

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and
                self.value == other.value and self.stratum == other.stratum)

    def __str__(self):
        return '{0:2} ({1:2}){2}'.format(
            self.value, self.stratum, '*' if self.is_border else ' ')


class PointMap(object):
    def __init__(self, points):
        self._points = PointMap._parse_points(points)
        self._n_rows = len(self._points)
        self._n_cols = len(self._points[0])
        self._strata = []

    def __str__(self):
        return '\n'.join(
            ['|'.join([str(element) for element in row])
             for row in self._points])

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        return self._points[index[0]][index[1]]

    @staticmethod
    def _parse_points(points):
        points_parsed = []
        for x, row in enumerate(PointMap._validate_points(points)):
            row_aux = []
            for y, value in enumerate(row):
                row_aux.append(Point(x, y, value))
            points_parsed.append(row_aux)
        return points_parsed

    @staticmethod
    def _validate_points(points):
        if type(points) is not list:
            raise PointMapException("'points' must be a list of lists")
        if not len(points):
            raise PointMapException("'points' must be a non empty list")
        if type(points[0]) is not list:
            raise PointMapException("'points' must be a list of lists")
        dimension = len(points[0])
        for row in points[1:]:
            if type(row) is not list:
                raise PointMapException("'points' must be a list of lists")
            if len(row) != dimension:
                raise PointMapException(
                    "'points' must represent a valid matrix")
        return points

    def compute_borders(self):
        self._compute_strata()
        for group in self._strata:
            is_border = False
            if all(self._is_minimum(point) for point in group):
                is_border = True
            for point in group:
                point.is_border = is_border

    def _compute_strata(self):
        for row in self._points:
            for point in row:
                if point.stratum is None:
                    self._init_stratum(point)
                    self._transmit_stratum(point)

    def _init_stratum(self, point):
        point.stratum = len(self._strata)
        self._strata.append([point])

    def _transmit_stratum(self, point):
        for neighbor in self._get_neighbors(point):
            if point.value == neighbor.value and neighbor.stratum is None:
                neighbor.stratum = point.stratum
                self._strata[point.stratum].append(neighbor)
                self._transmit_stratum(neighbor)

    def _is_minimum(self, point):
        return all(
            point.value <= neighbor.value
            for neighbor in self._get_neighbors(point))

    def _get_neighbors(self, point):
        neighbors = []
        for neighbor_i, neighbor_j in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            if self._is_valid_point(point.x, point.y, neighbor_i, neighbor_j):
                neighbors.append(
                    self[point.x + neighbor_i, point.y + neighbor_j])
        return neighbors

    def _is_valid_point(self, i, j, i_rel, j_rel):
        return (0 <= i + i_rel <= self._n_rows - 1
                and 0 <= j + j_rel <= self._n_cols - 1)
