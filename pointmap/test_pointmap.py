import unittest
import mock

from pointmap import Point, PointMap, PointMapException


class TestPointMap(unittest.TestCase):
    def test_parse_points_should_codify_values_using_points(self):
        points = PointMap._parse_points([
            [5, 4, 3],
            [1, 2, 6],
            [7, 9, 0],
        ])
        self.assertEqual(3, len(points))
        self.assertEqual(3, len(points[0]))
        self.assertEqual(3, len(points[1]))
        self.assertEqual(3, len(points[2]))
        self.assertEqual(Point(0, 0, 5), points[0][0])
        self.assertEqual(Point(0, 1, 4), points[0][1])
        self.assertEqual(Point(0, 2, 3), points[0][2])
        self.assertEqual(Point(1, 0, 1), points[1][0])
        self.assertEqual(Point(1, 1, 2), points[1][1])
        self.assertEqual(Point(1, 2, 6), points[1][2])
        self.assertEqual(Point(2, 0, 7), points[2][0])
        self.assertEqual(Point(2, 1, 9), points[2][1])
        self.assertEqual(Point(2, 2, 0), points[2][2])

    def test_parse_points_should_return_empty_matrix_if_points_are_empty(self):
        points = PointMap._parse_points([[]])
        self.assertEqual(1, len(points))
        self.assertEqual(0, len(points[0]))

    @mock.patch(
        'pointmap.PointMap._validate_points',
        side_effect=PointMapException('Something wrong happened'))
    def test_parse_points_should_raise_if_validation_raises(self, mock_validate):
        with self.assertRaises(PointMapException) as context:
            PointMap._parse_points([[]])
        self.assertEqual('Something wrong happened', context.exception.message)

    def test_validate_points_should_raise_if_points_are_not_list(self):
        with self.assertRaises(PointMapException) as context:
            PointMap._validate_points(None)
        self.assertEqual(
            "'points' must be a list of lists", context.exception.message)

    def test_validate_points_should_raise_if_points_are_empty_list(self):
        with self.assertRaises(PointMapException) as context:
            PointMap._validate_points([])
        self.assertEqual(
            "'points' must be a non empty list", context.exception.message)

    def test_validate_points_should_raise_if_points_are_not_list_of_lists(self):
        with self.assertRaises(PointMapException) as context:
            PointMap._validate_points([
                [1, 2, 3],
                [4, 5, 6],
                (7, 8, 9)])
        self.assertEqual(
            "'points' must be a list of lists", context.exception.message)

    def test_validate_point_should_raise_if_lists_have_not_same_length(self):
        with self.assertRaises(PointMapException) as context:
            PointMap._validate_points([
                [1, 2, 3],
                [4, 5, 6],
                [7, 8]])
        self.assertEqual(
            "'points' lists must have same length", context.exception.message)

    def test_validate_points_should_return_points_if_no_exceptions(self):
        points = [
            [1, 2, 3],
            [4, 5, 6]]
        self.assertEqual(points, PointMap._validate_points(points))

#    def test_getitem_should_return_points(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(5, pmap[0, 0])
#        self.assertEqual(4, pmap[0, 1])
#        self.assertEqual(3, pmap[0, 2])
#        self.assertEqual(1, pmap[1, 0])
#        self.assertEqual(2, pmap[1, 1])
#        self.assertEqual(6, pmap[1, 2])
#        self.assertEqual(7, pmap[2, 0])
#        self.assertEqual(9, pmap[2, 1])
#        self.assertEqual(0, pmap[2, 2])
#
#    def test_parse_points_should_codify_values_using_points(self):
#        points = PointMap._parse_points([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0],
#        ])
#        self.assertEqual(3, len(points))
#        self.assertEqual(3, len(points[0]))
#        self.assertEqual(3, len(points[1]))
#        self.assertEqual(3, len(points[2]))
#        self.assertEqual(Point(0, 0, 5, None), points[0][0])
#        self.assertEqual(Point(0, 1, 4, None), points[0][1])
#        self.assertEqual(Point(0, 2, 3, None), points[0][2])
#        self.assertEqual(Point(1, 0, 1, None), points[1][0])
#        self.assertEqual(Point(1, 1, 2, None), points[1][1])
#        self.assertEqual(Point(1, 2, 6, None), points[1][2])
#        self.assertEqual(Point(2, 0, 7, None), points[2][0])
#        self.assertEqual(Point(2, 1, 9, None), points[2][1])
#        self.assertEqual(Point(2, 2, 0, None), points[2][2])
#
#    def test_get_neighbors(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(
#            [Point(0, 1, 4), Point(1, 0, 1)],
#            pmap._get_neighbors(pmap[0, 0]))
#        self.assertEqual(
#            [Point(0, 0, 5), Point(0, 2, 3), Point(1, 1, 2)],
#            pmap._get_neighbors(pmap[0, 1]))
#        self.assertEqual(
#            [Point(0, 1, 4), Point(1, 2, 6)],
#            pmap._get_neighbors(pmap[0, 2]))
#        self.assertEqual(
#            [Point(0, 0, 5), Point(1, 1, 2), Point(2, 0, 7)],
#            pmap._get_neighbors(pmap[1, 0]))
#        self.assertEqual(
#            [Point(1, 0, 1), Point(0, 1, 4), Point(1, 2, 6), Point(2, 1, 9)],
#            pmap._get_neighbors(pmap[1, 1]))
#        self.assertEqual(
#            [Point(1, 1, 2), Point(0, 2, 3), Point(2, 2, 0)],
#            pmap._get_neighbors(pmap[1, 2]))
#        self.assertEqual(
#            [Point(1, 0, 1), Point(2, 1, 9)],
#            pmap._get_neighbors(pmap[2, 0]))
#        self.assertEqual(
#            [Point(2, 0, 7), Point(1, 1, 2), Point(2, 2, 0)],
#            pmap._get_neighbors(pmap[2, 1]))
#        self.assertEqual(
#            [Point(2, 1, 9), Point(1, 2, 6)],
#            pmap._get_neighbors(pmap[2, 2]))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_up_left(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(0, 0, -1, -1))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_left(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(0, 0, 0, -1))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_up(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(0, 0, -1, 0))
#
#    def test_get_neighbor_value_should_return_item_if_0_0(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(5, pmap._get_neighbor_value(0, 0, 0, 0))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_up_right(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(0, 2, 1, 1))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_right(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(0, 2, 0, 1))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_left_down(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(2, 0, 1, -1))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_down(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(2, 0, 1, 0))
#
#    def test_get_neighbor_value_should_return_none_if_out_of_range_from_right_down(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertIsNone(pmap._get_neighbor_value(2, 2, 1, 1))
#
#    def test_get_neighbor_values_should_return_right_down_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([4, 1], pmap._get_neighbor_values(0, 0))
#
#    def test_get_neighbor_values_should_return_right_down_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([3, 2, 5], pmap._get_neighbor_values(0, 1))
#
#    def test_get_neighbor_values_should_return_down_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([6, 4], pmap._get_neighbor_values(0, 2))
#
#    def test_get_neighbor_values_should_return_up_right_down_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([5, 2, 7], pmap._get_neighbor_values(1, 0))
#
#    def test_get_neighbor_values_should_return_up_right_down_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([4, 6, 9, 1], pmap._get_neighbor_values(1, 1))
#
#    def test_get_neighbor_values_should_return_up_down_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([3, 0, 2], pmap._get_neighbor_values(1, 2))
#
#    def test_get_neighbor_values_should_return_up_right_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([1, 9], pmap._get_neighbor_values(2, 0))
#
#    def test_get_neighbor_values_should_return_up_right_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([2, 0, 7], pmap._get_neighbor_values(2, 1))
#
#    def test_get_neighbor_values_should_return_up_left_values(self):
#        pmap = PointMap([
#            [5, 4, 3],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual([6, 9], pmap._get_neighbor_values(2, 2))
#
#    def test_classify_minimum_should_return_global(self):
#        pmap = PointMap([
#            [5, 8, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(PointMap.MINIMUM_GLOBAL, pmap._classify_minimum(1, 0))
#        self.assertEqual(PointMap.MINIMUM_GLOBAL, pmap._classify_minimum(2, 2))
#
#    def test_classify_minimum_should_return_local(self):
#        pmap = PointMap([
#            [5, 8, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(PointMap.MINIMUM_LOCAL, pmap._classify_minimum(0, 2))
#
#    def test_classify_minimum_should_return_other(self):
#        pmap = PointMap([
#            [5, 8, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(0, 0))
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(0, 1))
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(1, 1))
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(1, 2))
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(2, 0))
#        self.assertEqual(PointMap.MINIMUM_OTHER, pmap._classify_minimum(2, 1))
#
#    def test_compute_minima_should_fill_matrix(self):
#        pmap = PointMap([
#            [5, 8, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        pmap.compute_minima()
#        self.assertEqual([
#            [PointMap.MINIMUM_OTHER, PointMap.MINIMUM_OTHER, PointMap.MINIMUM_LOCAL],
#            [PointMap.MINIMUM_GLOBAL, PointMap.MINIMUM_OTHER, PointMap.MINIMUM_OTHER],
#            [PointMap.MINIMUM_OTHER, PointMap.MINIMUM_OTHER, PointMap.MINIMUM_GLOBAL],
#            ], pmap._minima)
#
#    def test_init_stratum_should_set_stratum(self):
#        pmap = PointMap([
#            [3, 5, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        pmap._strata = [[None for _ in range(3)] for _ in range(3)]
#        pmap._init_stratum(0, 0)
#        self.assertEqual(0, pmap._strata[0][0])
#        self.assertEqual([(0, 0)], pmap._strata_groups[0])
#
#    def test_transmit_stratum_should_transmit_to_neighbors(self):
#        pmap = PointMap([
#            [3, 2, 6],
#            [2, 2, 6],
#            [7, 9, 0]])
#        pmap._strata = [
#            [None, None, None],
#            [None, 9, None],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(1, 1)
#        self.assertEqual([
#            [None, 9, None],
#            [9, 9, None],
#            [None, None, None]], pmap._strata)
#        self.assertEqual(
#            [(1, 0), (0, 1)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_left_up(self):
#        pmap = PointMap([
#            [3, 3, 6],
#            [3, 2, 6],
#            [7, 9, 0]])
#        pmap._strata = [
#            [9, None, None],
#            [None, None, None],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(0, 0)
#        self.assertEqual([
#            [9, 9, None],
#            [9, None, None],
#            [None, None, None]], pmap._strata)
#        self.assertEqual(
#            [(0, 1), (1, 0)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_up(self):
#        pmap = PointMap([
#            [5, 5, 5],
#            [1, 5, 6],
#            [7, 9, 0]])
#        pmap._strata = [
#            [None, 9, None],
#            [None, None, None],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(0, 1)
#        self.assertEqual([
#            [9, 9, 9],
#            [None, 9, None],
#            [None, None, None]], pmap._strata)
#        self.assertEqual(
#            [(0, 0), (0, 2), (1, 1)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_right_up(self):
#        pmap = PointMap([
#            [3, 6, 6],
#            [1, 2, 6],
#            [7, 9, 0]])
#        pmap._strata = [
#            [None, None, 9],
#            [None, None, None],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(0, 2)
#        self.assertEqual([
#            [None, 9, 9],
#            [None, None, 9],
#            [None, None, None]], pmap._strata)
#        self.assertEqual(
#            [(0, 1), (1, 2)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_left(self):
#        pmap = PointMap([
#            [1, 5, 6],
#            [1, 1, 6],
#            [1, 9, 0]])
#        pmap._strata = [
#            [None, None, None],
#            [9, None, None],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(1, 0)
#        self.assertEqual([
#            [9, None, None],
#            [9, 9, None],
#            [9, None, None]], pmap._strata)
#        self.assertEqual(
#            [(0, 0), (1, 1), (2, 0)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_right(self):
#        pmap = PointMap([
#            [3, 5, 6],
#            [1, 6, 6],
#            [7, 9, 6]])
#        pmap._strata = [
#            [None, None, None],
#            [None, None, 9],
#            [None, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(1, 2)
#        self.assertEqual([
#            [None, None, 9],
#            [None, 9, 9],
#            [None, None, 9]], pmap._strata)
#        self.assertEqual(
#            [(1, 1), (0, 2), (2, 2)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_left_down(self):
#        pmap = PointMap([
#            [3, 5, 6],
#            [7, 2, 6],
#            [7, 7, 0]])
#        pmap._strata = [
#            [None, None, None],
#            [None, None, None],
#            [9, None, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(2, 0)
#        self.assertEqual([
#            [None, None, None],
#            [9, None, None],
#            [9, 9, None]], pmap._strata)
#        self.assertEqual(
#            [(1, 0), (2, 1)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_down(self):
#        pmap = PointMap([
#            [3, 5, 6],
#            [1, 9, 6],
#            [9, 9, 9]])
#        pmap._strata = [
#            [None, None, None],
#            [None, None, None],
#            [None, 9, None]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(2, 1)
#        self.assertEqual([
#            [None, None, None],
#            [None, 9, None],
#            [9, 9, 9]], pmap._strata)
#        self.assertEqual(
#            [(2, 0), (1, 1), (2, 2)], pmap._strata_groups[9])
#
#    def test_transmit_stratum_should_transmit_to_neighbors_when_no_right_down(self):
#        pmap = PointMap([
#            [3, 5, 6],
#            [1, 2, 0],
#            [7, 0, 0]])
#        pmap._strata = [
#            [None, None, None],
#            [None, None, None],
#            [None, None, 9]]
#        pmap._strata_groups = [[] for _ in range(10)]
#        pmap._transmit_stratum(2, 2)
#        self.assertEqual([
#            [None, None, None],
#            [None, None, 9],
#            [None, 9, 9]], pmap._strata)
#        self.assertEqual(
#            [(2, 1), (1, 2)], pmap._strata_groups[9])
#
#    def test_compute_strata_should_compute_matrix(self):
#        pmap = PointMap([
#            [9, 2, 2, 2, 3, 5],
#            [9, 8, 3, 2, 4, 5],
#            [9, 7, 2, 2, 4, 3],
#            [9, 9, 2, 4, 4, 3],
#            [9, 2, 3, 4, 3, 5]])
#        pmap.compute_strata()
#        self.assertEqual([
#            [0, 1, 1, 1, 2, 3],
#            [0, 4, 5, 1, 6, 3],
#            [0, 7, 1, 1, 6, 8],
#            [0, 0, 1, 6, 6, 8],
#            [0, 9, 10, 6, 11, 12]], pmap._strata)


#if __name__ == '__main__':
#    unittest.main()