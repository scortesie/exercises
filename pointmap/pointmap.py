class PointMapException(Exception):
    pass


class PointMap(object):
    MINIMUM_LOCAL = 0
    MINIMUM_GLOBAL = 1
    MINIMUM_OTHER = 2

    def __init__(self, points):
        self._points = PointMap.validate_points(points)
        self._n_rows = len(self._points)
        self._n_cols = len(self._points[0])
        self._minima = []
        self._strata = []
        self._strata_groups = []

    def __str__(self):
        points = '\n'.join(
            ['|'.join(['{:2}'.format(element) for element in row])
             for row in self._points])
        strata = '\n'.join(
            ['|'.join(['{:2}'.format(element) for element in row])
             for row in self._strata])
        return points + '\n---\n' + strata

    def __repr__(self):
        return str(self)

    def __getitem__(self, index):
        return self._points[index[0]][index[1]]

    @staticmethod
    def validate_points(points):
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

    def compute_minima(self):
        self._minima = []
        for i, row in enumerate(self._points):
            self._minima.append([])
            for j, point in enumerate(row):
                self._minima[i].append(self._classify_minimum(i, j))

    def _classify_minimum(self, i, j):
        if all(self[i, j] < value for value in self._get_neighbor_values(i, j)):
            return PointMap.MINIMUM_GLOBAL
        if any(self[i, j] > value for value in self._get_neighbor_values(i, j)):
            return PointMap.MINIMUM_OTHER
        return PointMap.MINIMUM_LOCAL

    def _get_neighbor_values(self, i, j):
        neighbor_up_value = self._get_neighbor_value(i, j, -1, 0)
        neighbor_right_value = self._get_neighbor_value(i, j, 0, 1)
        neighbor_down_value = self._get_neighbor_value(i, j, 1, 0)
        neighbor_left_value = self._get_neighbor_value(i, j, 0, -1)
        return [neighbor_value for neighbor_value in [
            neighbor_up_value, neighbor_right_value,
            neighbor_down_value, neighbor_left_value]
            if neighbor_value is not None]

    def _get_neighbor_value(self, i, j, i_rel, j_rel):
        if self._is_valid_point(i, j, i_rel, j_rel):
            return self[i + i_rel, j + j_rel]
        return None

    def _is_valid_point(self, i, j, i_rel, j_rel):
        return (0 <= i + i_rel <= self._n_rows - 1
                and 0 <= j + j_rel <= self._n_cols - 1)

    def compute_strata(self):
        self._strata = [
            [None for _ in range(self._n_cols)] for _ in range(self._n_rows)]
        for i, row in enumerate(self._points):
            for j, point in enumerate(row):
                self._classify_stratum(i, j)

    def _classify_stratum(self, i, j):
        if self._strata[i][j] is None:
            self._create_stratum(i, j)
            self._transmit_stratum(i, j)

    def _create_stratum(self, i, j):
        self._strata[i][j] = len(self._strata_groups)
        self._strata_groups.append([(i, j)])

    def _transmit_stratum(self, i, j):
        for neighbor_i, neighbor_j in ((0, -1), (-1, 0), (0, 1), (1, 0)):
            if self._is_valid_point(i, j, neighbor_i, neighbor_j):
                if (self[i, j] == self._get_neighbor_value(
                        i, j, neighbor_i, neighbor_j) and
                        self._strata[i + neighbor_i][j + neighbor_j] is None):
                    self._strata[i + neighbor_i][j + neighbor_j] = \
                        self._strata[i][j]
                    self._strata_groups[self._strata[i][j]].append(
                        (i + neighbor_i, j + neighbor_j))
                    self._transmit_stratum(i + neighbor_i, j + neighbor_j)

