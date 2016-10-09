"""
Defines the structures EarthMatrix and EarthPoint that model areas of earth
with a specific altitude. Also defines the algorithm
EarthMatrix::detect_borders that detects borders inside these areas.
"""


class EarthMatrix(object):
    """
    Represents an earth area made of earth points with a specific altitude.
    """
    def __init__(self, points):
        """
        :param points: matrix codified as a list of lists containing integers
        that represent an earth point's altitude.
        """
        self._points = EarthMatrix._parse_points(points)
        self._n_rows = len(self._points)
        self._n_cols = len(self._points[0])
        self._strata = []

    @staticmethod
    def _parse_points(points):
        points_parsed = []
        for x, row in enumerate(EarthMatrix._validate_points(points)):
            row_aux = []
            for y, altitude in enumerate(row):
                row_aux.append(EarthPoint(x, y, altitude))
            points_parsed.append(row_aux)
        return points_parsed

    @staticmethod
    def _validate_points(points):
        if type(points) is not list:
            raise EarthMatrixException("'points' must be a list of lists")
        if not len(points):
            raise EarthMatrixException("'points' must be a non empty list")
        if type(points[0]) is not list:
            raise EarthMatrixException("'points' must be a list of lists")
        dimension = len(points[0])
        for row in points[1:]:
            if type(row) is not list:
                raise EarthMatrixException("'points' must be a list of lists")
            if len(row) != dimension:
                raise EarthMatrixException(
                    "'points' lists must have same length")
        return points

    def detect_borders(self):
        """
        Determine whether an earth point in the matrix is a border, i. e., its
        altitude is less than the altitude of the strata it is surrounded by.
        :return: list of lists representing a matrix containing 1 if the point
        is a border and 0 otherwise.
        """
        self._compute_strata()
        for group in self._strata:
            is_border = all(self._is_minimum(point) for point in group)
            for point in group:
                point.is_border = is_border
        return self._get_border_matrix()

    def _compute_strata(self):
        """
        Compute the groups of points with same altitude.
        """
        for row in self._points:
            for point in row:
                if point.stratum is None:
                    self._init_stratum(point)
                    self._transmit_stratum_to_neighbors(point)

    def _init_stratum(self, point):
        point.stratum = len(self._strata)
        self._strata.append([point])

    def _transmit_stratum_to_neighbors(self, point):
        for neighbor in self._get_neighbors(point):
            if point.altitude == neighbor.altitude and neighbor.stratum is None:
                neighbor.stratum = point.stratum
                self._strata[point.stratum].append(neighbor)
                self._transmit_stratum_to_neighbors(neighbor)

    def _is_minimum(self, point):
        return all(
            point.altitude <= neighbor.altitude
            for neighbor in self._get_neighbors(point))

    def _get_neighbors(self, point):
        neighbors = []
        for coordinates in (point.delta(x, y)
                            for x, y in ((0, -1), (-1, 0), (0, 1), (1, 0))):
            if self._is_valid_coordinates(coordinates):
                neighbors.append(self[coordinates])
        return neighbors

    def _is_valid_coordinates(self, coordinates):
        return (0 <= coordinates[0] <= self._n_rows - 1 and
                0 <= coordinates[1] <= self._n_cols - 1)

    def _get_border_matrix(self):
        return [[1 if point.is_border else 0 for point in row]
                for row in self._points]

    def __str__(self):
        return '\n'.join(
            ['|'.join([str(element) for element in row])
             for row in self._points])

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        return self._points[index[0]][index[1]]


class EarthPoint(object):
    """
    Represents a piece of earth defined by its coordinates within a matrix,
    altitude and stratum (id of the set of matrix points with same altitude to
    which it belongs).
    """
    def __init__(self, x, y, altitude, stratum=None, is_border=False):
        self.x = x
        self.y = y
        self.altitude = altitude
        self.stratum = stratum
        self.is_border = is_border

    def delta(self, x, y):
        """
        Return a tuple of coordinates representing this point coordinates after
        applying a delta increase/decrease.
        """
        return self.x + x, self.y + y

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y and
                self.altitude == other.altitude and
                self.stratum == other.stratum and
                self.is_border == other.is_border)

    def __str__(self):
        return '{0:2} ({1:2}){2}'.format(
            self.altitude, self.stratum, '*' if self.is_border else ' ')


class EarthMatrixException(Exception):
    pass
