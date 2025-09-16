import pandas as pd
from tabulate import tabulate

# Core function to perform the heat loss calculation.
# This function is flexible and can be used with any set of components.
def calculate_heat_loss(components, internal_temp, external_temp):
    """
    Calculates the steady-state heat loss for a list of building components.

    Args:
        components (list of dict): A list where each dictionary represents a
                                   building component with 'name', 'area_sqm',
                                   and 'u_value_W_per_sqmK' keys.
        internal_temp (float): The internal temperature in degrees Celsius.
        external_temp (float): The external temperature in degrees Celsius.

    Returns:
        dict: A dictionary containing a list of calculated results for each
              component and the total heat loss.
    """
    # Calculate the temperature difference (Delta T)
    delta_T = internal_temp - external_temp

    # Initialize a list to hold the results for each component
    results = []
    total_heat_loss = 0.0

    # Iterate through each component and calculate its heat loss
    for component in components:
        # The core heat loss formula: Q = U * A * Delta T
        # Q is the heat loss (Watts)
        # U is the U-Value (W/m^2K)
        # A is the Area (m^2)
        # Delta T is the temperature difference (K or degrees C)
        q_component = component['u_value_W_per_sqmK'] * component['area_sqm'] * delta_T
        
        # Append the results for the current component
        results.append({
            'Name': component['name'],
            'Area ($m^2$)': component['area_sqm'],
            'U-Value ($W/m^2K$)': component['u_value_W_per_sqmK'],
            'Heat Loss (W)': q_component
        })

        # Add to the total heat loss
        total_heat_loss += q_component
    
    return {'component_results': results, 'total_heat_loss': total_heat_loss}

def main():
    """
    Main function to run the thermal calculation and display the results.
    """
    print("--- Steady-State Heat Loss Calculator ---")

    # The input data in a flexible, tabulated format.
    # This list of dictionaries is easy to create manually from your notes
    # or programmatically from a drawing file (.dwg) in the future.
    # The 'orientation' field is included as an input for future extensions,
    # for instance, when calculating solar gains.
    building_components = [
        {'name': 'Exterior Wall 1', 'area_sqm': 20.0, 'u_value_W_per_sqmK': 0.25, 'orientation': 'North'},
        {'name': 'Exterior Wall 2', 'area_sqm': 15.0, 'u_value_W_per_sqmK': 0.25, 'orientation': 'South'},
        {'name': 'Window 1', 'area_sqm': 2.5, 'u_value_W_per_sqmK': 1.6, 'orientation': 'North'},
        {'name': 'Window 2', 'area_sqm': 3.0, 'u_value_W_per_sqmK': 1.6, 'orientation': 'South'},
        {'name': 'Roof', 'area_sqm': 40.0, 'u_value_W_per_sqmK': 0.15, 'orientation': 'Horizontal'},
        {'name': 'Floor', 'area_sqm': 40.0, 'u_value_W_per_sqmK': 0.2, 'orientation': 'Horizontal'},
    ]

    # Define the external and internal temperatures
    external_temp_C = -5.0
    internal_temp_C = 20.0
    
    # Calculate the heat loss using the defined function
    calculated_data = calculate_heat_loss(building_components, internal_temp_C, external_temp_C)

    # Convert the results to a pandas DataFrame for easy tabulation
    results_df = pd.DataFrame(calculated_data['component_results'])

    # Print a summary of the calculation parameters
    print(f"\nCalculation Parameters:")
    print(f"  Internal Temperature: {internal_temp_C:.1f} °C")
    print(f"  External Temperature: {external_temp_C:.1f} °C")
    print(f"  Temperature Difference (ΔT): {internal_temp_C - external_temp_C:.1f} K")

    # Print the tabulated results
    print("\nIndividual Component Heat Loss:")
    print(tabulate(results_df, headers='keys', tablefmt='pipe', numalign='right', floatfmt=".2f"))

    # Print the final total heat loss
    print(f"\nTotal Building Heat Loss: {calculated_data['total_heat_loss']:.2f} Watts")

if __name__ == '__main__':
    main()
