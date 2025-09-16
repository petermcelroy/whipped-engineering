import unittest
from src.calculator import UValueCalculator

class TestUValueCalculator(unittest.TestCase):

    def setUp(self):
        self.calculator = UValueCalculator()

    def test_calculate_u_value(self):
        # Example test case for calculating U value
        # Assuming the method takes parameters: thickness, thermal_conductivity, and area
        thickness = 0.1  # in meters
        thermal_conductivity = 0.04  # W/(m·K)
        area = 10  # in square meters
        expected_u_value = self.calculator.calculate_u_value(thickness, thermal_conductivity, area)
        self.assertAlmostEqual(expected_u_value, 0.4, places=2)  # Replace with the correct expected value

    def test_invalid_thickness(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_u_value(-0.1, 0.04, 10)

    def test_invalid_thermal_conductivity(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_u_value(0.1, -0.04, 10)

    def test_invalid_area(self):
        with self.assertRaises(ValueError):
            self.calculator.calculate_u_value(0.1, 0.04, -10)

if __name__ == '__main__':
    unittest.main()