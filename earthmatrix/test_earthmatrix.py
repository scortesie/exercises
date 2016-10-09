import unittest
import mock

from earthmatrix import EarthPoint, EarthMatrix, EarthMatrixException


class TestEarthMatrix(unittest.TestCase):
    def test_parse_points_should_codify_altitudes_using_points(self):
        points = EarthMatrix._parse_points([
            [5, 4, 3],
            [1, 2, 6],
            [7, 9, 0],
        ])
        self.assertEqual(3, len(points))
        self.assertEqual(3, len(points[0]))
        self.assertEqual(3, len(points[1]))
        self.assertEqual(3, len(points[2]))
        self.assertEqual(EarthPoint(0, 0, 5), points[0][0])
        self.assertEqual(EarthPoint(0, 1, 4), points[0][1])
        self.assertEqual(EarthPoint(0, 2, 3), points[0][2])
        self.assertEqual(EarthPoint(1, 0, 1), points[1][0])
        self.assertEqual(EarthPoint(1, 1, 2), points[1][1])
        self.assertEqual(EarthPoint(1, 2, 6), points[1][2])
        self.assertEqual(EarthPoint(2, 0, 7), points[2][0])
        self.assertEqual(EarthPoint(2, 1, 9), points[2][1])
        self.assertEqual(EarthPoint(2, 2, 0), points[2][2])

    def test_parse_points_should_return_empty_matrix_if_points_are_empty(self):
        points = EarthMatrix._parse_points([[]])
        self.assertEqual(1, len(points))
        self.assertEqual(0, len(points[0]))

    @mock.patch(
        'earthmatrix.EarthMatrix._validate_points',
        side_effect=EarthMatrixException('Something wrong happened'))
    def test_parse_points_should_raise_if_validation_raises(self, mock_validate):
        with self.assertRaises(EarthMatrixException) as context:
            EarthMatrix._parse_points([[]])
        self.assertEqual('Something wrong happened', context.exception.message)

    def test_validate_points_should_raise_if_points_are_not_list(self):
        with self.assertRaises(EarthMatrixException) as context:
            EarthMatrix._validate_points(None)
        self.assertEqual(
            "'points' must be a list of lists", context.exception.message)

    def test_validate_points_should_raise_if_points_are_empty_list(self):
        with self.assertRaises(EarthMatrixException) as context:
            EarthMatrix._validate_points([])
        self.assertEqual(
            "'points' must be a non empty list", context.exception.message)

    def test_validate_points_should_raise_if_points_are_not_list_of_lists(self):
        with self.assertRaises(EarthMatrixException) as context:
            EarthMatrix._validate_points([
                [1, 2, 3],
                [4, 5, 6],
                (7, 8, 9)])
        self.assertEqual(
            "'points' must be a list of lists", context.exception.message)

    def test_validate_point_should_raise_if_lists_have_not_same_length(self):
        with self.assertRaises(EarthMatrixException) as context:
            EarthMatrix._validate_points([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8]])
        self.assertEqual(
            "'points' lists must have same length", context.exception.message)

    def test_validate_points_should_return_points_if_no_exceptions(self):
        points = [
            [1, 2, 3],
            [4, 5, 6]]
        self.assertEqual(points, EarthMatrix._validate_points(points))

    def test_detect_borders_should_set_true_for_strata_with_all_minimum_points(self):
        pmap = EarthMatrix([
            [9, 2, 2, 2, 3, 5],
            [9, 8, 3, 2, 4, 5],
            [9, 7, 2, 2, 4, 3],
            [9, 9, 2, 4, 4, 3],
            [9, 2, 3, 4, 3, 5]])
        self.assertEqual([
            [0, 1, 1, 1, 0, 0],
            [0, 0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0, 1],
            [0, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 1, 0]], pmap.detect_borders())

    def test_detect_borders_should_set_true_for_strata_with_all_minimum_points_for_single_point_map(self):
        pmap = EarthMatrix([[9]])
        self.assertEqual([
            [1]], pmap.detect_borders())

    def test_detect_borders_should_set_true_for_strata_with_all_minimum_points_for_single_altitude_map(self):
        pmap = EarthMatrix([
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9],
            [9, 9, 9, 9, 9, 9]])
        self.assertEqual([
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1]], pmap.detect_borders())

    def test_detect_borders_should_set_true_for_strata_with_all_minimum_points_for_square_map(self):
        pmap = EarthMatrix([
            [9, 9, 9, 9, 9, 9],
            [9, 5, 5, 5, 5, 9],
            [9, 5, 8, 8, 5, 9],
            [9, 5, 5, 5, 5, 9],
            [9, 9, 9, 9, 9, 9]])
        self.assertEqual([
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 1, 1, 1, 1, 0],
            [0, 0, 0, 0, 0, 0]], pmap.detect_borders())

    def test_detect_borders_should_set_true_for_strata_with_all_minimum_points_for_square_map_reversed(self):
        pmap = EarthMatrix([
            [5, 5, 5, 5, 5, 5],
            [5, 9, 9, 9, 9, 5],
            [5, 9, 5, 5, 9, 5],
            [5, 9, 9, 9, 9, 5],
            [5, 5, 5, 5, 5, 5]])
        self.assertEqual([
            [1, 1, 1, 1, 1, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 0, 1, 1, 0, 1],
            [1, 0, 0, 0, 0, 1],
            [1, 1, 1, 1, 1, 1]], pmap.detect_borders())

    def test_compute_strata_should_set_same_stratum_to_neighbors_with_same_altitude(self):
        pmap = EarthMatrix([
            [1, 1, 1, 3],
            [2, 2, 1, 3],
            [1, 1, 1, 3]])
        pmap._compute_strata()
        strata_0 = [pmap[0, 0], pmap[0, 1], pmap[0, 2],
                    pmap[1, 2], pmap[2, 0], pmap[2, 1], pmap[2, 2]]
        strata_1 = [pmap[0, 3], pmap[1, 3], pmap[2, 3]]
        strata_2 = [pmap[1, 0], pmap[1, 1]]
        for point in strata_0:
            self.assertEqual(0, point.stratum)
        self.assertEqual(sorted(strata_0), sorted(pmap._strata[0]))
        for point in strata_1:
            self.assertEqual(1, point.stratum)
        self.assertEqual(sorted(strata_1), sorted(pmap._strata[1]))
        for point in strata_2:
            self.assertEqual(2, point.stratum)

    def test_init_stratum_should_assign_next_free_strata_group(self):
        pmap = EarthMatrix([[]])
        pmap._strata = [['strata_group_0'], ['strata_group_1']]
        point = EarthPoint(1, 5, 15)
        pmap._init_stratum(point)
        self.assertEqual(2, point.stratum)

    def test_init_stratum_should_append_point_to_strata_group(self):
        pmap = EarthMatrix([[]])
        pmap._strata = [['strata_group_0'], ['strata_group_1']]
        point = EarthPoint(1, 5, 15)
        pmap._init_stratum(point)
        self.assertEqual([point], pmap._strata[2])

    def test_transmit_stratum_to_neighbors_should_only_transmit_if_same_altitude(self):
        neighbor_1 = EarthPoint(0, 0, 5)
        neighbor_2 = EarthPoint(0, 2, 6)
        neighbor_3 = EarthPoint(1, 1, 7)
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([neighbor_1, neighbor_2, neighbor_3], [], [], [])):
            pmap = EarthMatrix([[]])
            pmap._strata.extend([[], [], []])
            pmap._transmit_stratum_to_neighbors(EarthPoint(0, 1, 6, stratum=2))
        self.assertEqual(neighbor_1.stratum, None)
        self.assertEqual(neighbor_2.stratum, 2)
        self.assertEqual(neighbor_3.stratum, None)
        self.assertEqual([neighbor_2], pmap._strata[2])

    def test_transmit_stratum_to_neighbors_should_only_transmit_if_no_stratum(self):
        neighbor_1 = EarthPoint(0, 0, 5)
        neighbor_2 = EarthPoint(0, 2, 6, stratum=5)
        neighbor_3 = EarthPoint(1, 1, 7)
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([neighbor_1, neighbor_2, neighbor_3], [], [], [])):
            pmap = EarthMatrix([[]])
            pmap._strata.extend([[], [], []])
            pmap._transmit_stratum_to_neighbors(EarthPoint(0, 1, 6, stratum=2))
        self.assertEqual(neighbor_1.stratum, None)
        self.assertEqual(neighbor_2.stratum, 5)
        self.assertEqual(neighbor_3.stratum, None)
        self.assertEqual([], pmap._strata[2])

    def test_is_minimum_should_return_true_if_altitude_is_lessthan_neighborss(self):
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([EarthPoint(0, 0, 2), EarthPoint(0, 1, 3), EarthPoint(0, 2, 4)],)):
            pmap = EarthMatrix([[]])
            self.assertTrue(pmap._is_minimum(EarthPoint(0, 0, 1)))

    def test_is_minimum_should_return_true_if_altitude_is_equal_to_neighborss(self):
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([EarthPoint(0, 0, 1), EarthPoint(0, 1, 1), EarthPoint(0, 2, 1)],)):
            pmap = EarthMatrix([[]])
            self.assertTrue(pmap._is_minimum(EarthPoint(0, 0, 1)))

    def test_is_minimum_should_return_true_if_altitude_is_lessequal_to_neighborss(self):
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([EarthPoint(0, 0, 1), EarthPoint(0, 1, 2), EarthPoint(0, 2, 3)],)):
            pmap = EarthMatrix([[]])
            self.assertTrue(pmap._is_minimum(EarthPoint(0, 0, 1)))

    def test_is_minimum_should_return_false_if_altitude_is_greaterthan_any_neighbors(self):
        with mock.patch(
                'earthmatrix.EarthMatrix._get_neighbors',
                side_effect=([EarthPoint(0, 0, 1), EarthPoint(0, 1, 0), EarthPoint(0, 2, 1)],)):
            pmap = EarthMatrix([[]])
            self.assertFalse(pmap._is_minimum(EarthPoint(0, 0, 1)))

    def test_get_neighbors_should_return_only_points_with_valid_coordinates(self):
        pmap = EarthMatrix([
            [5, 4, 3],
            [1, 2, 6],
            [7, 9, 0]])
        self.assertEqual(
            [EarthPoint(0, 1, 4), EarthPoint(1, 0, 1)],
            pmap._get_neighbors(pmap[0, 0]))
        self.assertEqual(
            [EarthPoint(0, 0, 5), EarthPoint(0, 2, 3), EarthPoint(1, 1, 2)],
            pmap._get_neighbors(pmap[0, 1]))
        self.assertEqual(
            [EarthPoint(0, 1, 4), EarthPoint(1, 2, 6)],
            pmap._get_neighbors(pmap[0, 2]))
        self.assertEqual(
            [EarthPoint(0, 0, 5), EarthPoint(1, 1, 2), EarthPoint(2, 0, 7)],
            pmap._get_neighbors(pmap[1, 0]))
        self.assertEqual(
            [EarthPoint(1, 0, 1), EarthPoint(0, 1, 4), EarthPoint(1, 2, 6), EarthPoint(2, 1, 9)],
            pmap._get_neighbors(pmap[1, 1]))
        self.assertEqual(
            [EarthPoint(1, 1, 2), EarthPoint(0, 2, 3), EarthPoint(2, 2, 0)],
            pmap._get_neighbors(pmap[1, 2]))
        self.assertEqual(
            [EarthPoint(1, 0, 1), EarthPoint(2, 1, 9)],
            pmap._get_neighbors(pmap[2, 0]))
        self.assertEqual(
            [EarthPoint(2, 0, 7), EarthPoint(1, 1, 2), EarthPoint(2, 2, 0)],
            pmap._get_neighbors(pmap[2, 1]))
        self.assertEqual(
            [EarthPoint(2, 1, 9), EarthPoint(1, 2, 6)],
            pmap._get_neighbors(pmap[2, 2]))

    def test_is_valid_coordinates_should_return_false_if_x_lessthan_0(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((-1, 0)))

    def test_is_valid_coordinates_should_return_false_if_x_equal_n_rows(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((5, 0)))

    def test_is_valid_coordinates_should_return_false_if_x_greater_n_rows(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((6, 0)))

    def test_is_valid_coordinates_should_return_false_if_y_lessthan_0(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((0, -1)))

    def test_is_valid_coordinates_should_return_false_if_y_equal_n_cols(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((0, 5)))

    def test_is_valid_coordinates_should_return_false_if_y_greater_n_cols(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertFalse(pmap._is_valid_coordinates((0, 6)))

    def test_is_valid_coordinates_should_return_true_if_x_y_are_valid(self):
        pmap = EarthMatrix([[]])
        pmap._n_rows = 5
        pmap._n_cols = 5
        self.assertTrue(pmap._is_valid_coordinates((0, 0)))

    def test_get_border_matrix_should_return_matrix_with_same_map_dimensions(self):
        pmap = EarthMatrix([
            [1, 2, 3],
            [7, 8, 9]])
        border_matrix = pmap._get_border_matrix()
        self.assertEqual(2, len(border_matrix))
        self.assertEqual(3, len(border_matrix[0]))

    def test_get_border_matrix_should_return_matrix_with_1_if_is_border_0_otherwise(self):
        pmap = EarthMatrix([
            [1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])
        pmap._points[0][0].is_border = True
        pmap._points[0][1].is_border = False
        pmap._points[0][2].is_border = True
        pmap._points[1][0].is_border = False
        pmap._points[1][1].is_border = True
        pmap._points[1][2].is_border = False
        pmap._points[2][0].is_border = True
        pmap._points[2][1].is_border = False
        pmap._points[2][2].is_border = True
        self.assertEqual([
            [1, 0, 1],
            [0, 1, 0],
            [1, 0, 1]], pmap._get_border_matrix())

    def test_getitem_should_return_points(self):
        pmap = EarthMatrix([
            [5, 4, 3],
            [1, 2, 6],
            [7, 9, 0]])
        self.assertEqual(EarthPoint(0, 0, 5), pmap[0, 0])
        self.assertEqual(EarthPoint(0, 1, 4), pmap[0, 1])
        self.assertEqual(EarthPoint(0, 2, 3), pmap[0, 2])
        self.assertEqual(EarthPoint(1, 0, 1), pmap[1, 0])
        self.assertEqual(EarthPoint(1, 1, 2), pmap[1, 1])
        self.assertEqual(EarthPoint(1, 2, 6), pmap[1, 2])
        self.assertEqual(EarthPoint(2, 0, 7), pmap[2, 0])
        self.assertEqual(EarthPoint(2, 1, 9), pmap[2, 1])
        self.assertEqual(EarthPoint(2, 2, 0), pmap[2, 2])

    def test_str_should_return_pipe_between_cols_and_newlines_between_rows(self):
        pmap = EarthMatrix([
            [5, 4, 3],
            [1, 2, 6],
            [7, 9, 0]])
        self.assertEqual(
            '{0}|{1}|{2}\n{3}|{4}|{5}\n{6}|{7}|{8}'.format(
                pmap[0, 0], pmap[0, 1], pmap[0, 2],
                pmap[1, 0], pmap[1, 1], pmap[1, 2],
                pmap[2, 0], pmap[2, 1], pmap[2, 2]), str(pmap))

if __name__ == '__main__':
    unittest.main()
