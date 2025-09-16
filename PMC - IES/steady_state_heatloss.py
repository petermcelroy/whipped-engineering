import pandas as pd
from tabulate import tabulate

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
    print("--- Interactive Steady-State Heat Loss Calculator ---")
    
    # 1. Get environmental inputs from the user
    try:
        external_temp_C = float(input("\nEnter the external temperature in °C: "))
        internal_temp_C = float(input("Enter the internal temperature in °C: "))
    except ValueError:
        print("Invalid temperature input. Please enter a number.")
        return

    print("\nNow, enter the details for each building component.")
    print("Type 'done' at the name prompt to finish.")

    # 2. Get building component inputs from the user
    building_components = []
    while True:
        component_name = input("\nEnter component name (or 'done'): ")
        if component_name.lower() == 'done':
            break
        
        try:
            component_area = float(input(f"Enter the area of '{component_name}' in m^2: "))
            component_u_value = float(input(f"Enter the U-Value for '{component_name}' in W/m^2K: "))
            
            building_components.append({
                'name': component_name,
                'area_sqm': component_area,
                'u_value_W_per_sqmK': component_u_value,
                # 'orientation': 'Not specified in this input method'
            })
        except ValueError:
            print("Invalid input for area or U-Value. Please enter a number and try again.")
            continue # Continue the loop to ask for the same component again

    # Check if any components were entered
    if not building_components:
        print("No components were entered. Exiting.")
        return

    # 3. Calculate the heat loss
    calculated_data = calculate_heat_loss(building_components, internal_temp_C, external_temp_C)

    # Convert the results to a pandas DataFrame for easy tabulation
    results_df = pd.DataFrame(calculated_data['component_results'])

    # 4. Print results
    print(f"\nCalculation Parameters:")
    print(f"  Internal Temperature: {internal_temp_C:.1f} °C")
    print(f"  External Temperature: {external_temp_C:.1f} °C")
    print(f"  Temperature Difference (ΔT): {internal_temp_C - external_temp_C:.1f} K")

    print("\nIndividual Component Heat Loss:")
    print(tabulate(results_df, headers='keys', tablefmt='pipe', numalign='right', floatfmt=".2f"))

    print(f"\nTotal Building Heat Loss: {calculated_data['total_heat_loss']:.2f} Watts")

if __name__ == '__main__':
    main()
