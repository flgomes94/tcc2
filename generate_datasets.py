import json
import random
import copy
import os
import math

# Define the range for variation
VARIATION_PERCENTAGE = 0.1  # 10% variation

def vary_value(value, percentage=VARIATION_PERCENTAGE):
    """Vary a value by a random percentage within the given range."""
    variation = random.uniform(-percentage, percentage)
    varied_value = value * (1 + variation)
    
    # For CPU cores, round to the nearest integer (minimum 1)
    if value < 100:  # Assume this is CPU cores if value is small
        return max(1, round(varied_value))
    # For memory, round to the nearest power of 2 division (common for memory)
    else:
        return round(varied_value)

def modify_dataset(dataset_path, output_path):
    """Modify a dataset by varying memory, CPU, and CPU cores values."""
    with open(dataset_path, 'r') as file:
        data = json.load(file)
    
    # Create a deep copy to avoid modifying the original
    modified_data = copy.deepcopy(data)
    
    # Modify EdgeServer attributes
    if "EdgeServer" in modified_data:
        for server in modified_data["EdgeServer"]:
            if "attributes" in server:
                # Modify CPU cores (keep at least 1 core)
                if "cpu" in server["attributes"]:
                    server["attributes"]["cpu"] = vary_value(server["attributes"]["cpu"])
                
                # Modify memory
                if "memory" in server["attributes"]:
                    server["attributes"]["memory"] = vary_value(server["attributes"]["memory"])
    
    # Save the modified dataset
    with open(output_path, 'w') as file:
        json.dump(modified_data, file, indent=4)
    
    return output_path

def main():
    # Base dataset paths
    dataset1_path = "/home/fabio/projetos/tcc-agora-vai/tcc2/dataset1.json"
    dataset2_path = "/home/fabio/projetos/tcc-agora-vai/tcc2/dataset2.json"
    
    # Create output directory if it doesn't exist
    output_dir = "/home/fabio/projetos/tcc-agora-vai/tcc2/generated_datasets"
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate 5 datasets based on dataset1
    for i in range(1, 11):
        output_path = f"{output_dir}/dataset1_{i}.json"
        modify_dataset(dataset1_path, output_path)
        print(f"Generated {output_path}")
    
    # Generate 5 datasets based on dataset2
    for i in range(1, 11):
        output_path = f"{output_dir}/dataset2_{i}.json"
        modify_dataset(dataset2_path, output_path)
        print(f"Generated {output_path}")

if __name__ == "__main__":
    # Set a fixed seed for reproducibility
    random.seed(42)
    main()
    print("All datasets generated successfully!") 