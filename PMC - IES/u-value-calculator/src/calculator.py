class UValueCalculator:
    def __init__(self, thickness, thermal_conductivity):
        self.thickness = thickness  # in meters
        self.thermal_conductivity = thermal_conductivity  # in W/(m·K)

    def calculate_u_value(self):
        """
        Calculate the U value based on the thickness and thermal conductivity.
        
        U value is calculated using the formula:
        U = k / d
        where:
        k = thermal conductivity (W/(m·K))
        d = thickness (m)
        
        Returns:
            float: The calculated U value (W/(m²·K))
        """
        if self.thickness <= 0:
            raise ValueError("Thickness must be greater than zero.")
        if self.thermal_conductivity <= 0:
            raise ValueError("Thermal conductivity must be greater than zero.")
        
        u_value = self.thermal_conductivity / self.thickness
        return u_value