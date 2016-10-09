import unittest

from earthmatrix import EarthPoint


class TestEarthEarthPoint(unittest.TestCase):
    def test_delta_should_return_2_element_tuple(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        self.assertEqual(tuple, type(point.delta(0, 0)))
        self.assertEqual(2, len(point.delta(0, 0)))

    def test_delta_should_apply_positive_increase_to_x(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(5, 2)
        self.assertEqual(1 + 5, delta[0])

    def test_delta_should_apply_negative_increase_to_x(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(-5, 2)
        self.assertEqual(1 - 5, delta[0])

    def test_delta_should_apply_nil_increase_to_x(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(0, 2)
        self.assertEqual(1, delta[0])

    def test_delta_should_apply_positive_increase_to_y(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(5, 3)
        self.assertEqual(2 + 3, delta[1])

    def test_delta_should_apply_negative_increase_to_y(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(5, -3)
        self.assertEqual(2 - 3, delta[1])

    def test_delta_should_apply_nil_increase_to_y(self):
        point = EarthPoint(x=1, y=2, altitude=5)
        delta = point.delta(0, 0)
        self.assertEqual(2, delta[1])

    def test_eq_should_return_true_if_all_properties_are_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        self.assertEqual(point_a, point_b)

    def test_eq_should_return_false_if_x_property_is_not_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=2, y=5, altitude=102, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_y_property_is_not_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=6, altitude=102, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_altitude_property_is_not_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=5, altitude=101, stratum=5, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_stratum_property_is_not_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=5, altitude=102, stratum=6, is_border=False)
        self.assertNotEqual(point_a, point_b)

    def test_eq_should_return_false_if_is_border_property_is_not_equal(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=True)
        self.assertNotEqual(point_a, point_b)

    def test_str_should_return_altitude_space_par_stratum_star_if_border(self):
        point_a = EarthPoint(x=1, y=5, altitude=102, stratum=5, is_border=False)
        point_b = EarthPoint(x=1, y=5, altitude=2, stratum=10, is_border=True)
        self.assertEqual("102 ( 5) ", str(point_a))
        self.assertEqual(" 2 (10)*", str(point_b))


if __name__ == '__main__':
    unittest.main()
