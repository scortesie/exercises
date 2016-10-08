import unittest

from pointmap import Point


class TestPointMap(unittest.TestCase):
    def test_eq_should_return_true_if_all_properties_are_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        self.assertEqual(point_a, point_b)

    def test_eq_should_return_false_if_x_property_is_not_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=2, y=5, value=102, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_y_property_is_not_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=6, value=102, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_value_property_is_not_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=5, value=101, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_stratum_property_is_not_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=5, value=102, stratum=6, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_is_border_property_is_not_equal(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=5, value=102, stratum=5, is_border=True)
        self.assertNotEqual(point_a, point_b)

    def test_str_should_return_value_space_par_stratum_star_if_border(self):
        point_a = Point(x=1, y=5, value=102, stratum=5, is_border=False)
        point_b = Point(x=1, y=5, value=2, stratum=10, is_border=True)
        self.assertEqual("102 ( 5) ", str(point_a))
        self.assertEqual(" 2 (10)*", str(point_b))


if __name__ == '__main__':
    unittest.main()
