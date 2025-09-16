# U Value Calculator

## Overview
The U Value Calculator is a Python project designed to calculate the U value (thermal transmittance) of building materials. The U value is a measure of how effective a building material is as an insulator. Lower U values indicate better insulating properties.

## Features
- Calculate U values based on material properties.
- Utility functions for input validation and unit conversions.

## Installation
To install the required dependencies, run the following command:

```
pip install -r requirements.txt
```

## Usage
To use the U Value Calculator, you can import the `UValueCalculator` class from the `calculator` module and call the `calculate_u_value` method with the necessary parameters.

### Example
```python
from src.calculator import UValueCalculator

calculator = UValueCalculator()
u_value = calculator.calculate_u_value(material_thickness, thermal_conductivity)
print(f"The calculated U value is: {u_value}")
```

## Testing
Unit tests for the `UValueCalculator` class can be found in the `tests/test_calculator.py` file. To run the tests, use the following command:

```
pytest tests/
```

## Contributing
Contributions are welcome! Please feel free to submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.