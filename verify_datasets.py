import json
import os
import pandas as pd
from tabulate import tabulate

def analyze_dataset(file_path):
    """Analyze a dataset and extract CPU and memory information."""
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    servers = []
    
    if "EdgeServer" in data:
        for server in data["EdgeServer"]:
            if "attributes" in server:
                server_id = server["attributes"].get("id", "N/A")
                cpu = server["attributes"].get("cpu", "N/A")
                memory = server["attributes"].get("memory", "N/A")
                
                servers.append({
                    "server_id": server_id,
                    "cpu": cpu,
                    "memory": memory
                })
    
    return servers

def main():
    # Define paths
    original_datasets = [
        "/home/fabio/projetos/tcc-agora-vai/tcc2/dataset1.json",
        "/home/fabio/projetos/tcc-agora-vai/tcc2/dataset2.json"
    ]
    
    generated_dir = "/home/fabio/projetos/tcc-agora-vai/tcc2/generated_datasets"
    
    # Analyze original datasets first
    print("Original Datasets:")
    for dataset_path in original_datasets:
        dataset_name = os.path.basename(dataset_path)
        servers = analyze_dataset(dataset_path)
        
        print(f"\n{dataset_name}:")
        df = pd.DataFrame(servers)
        print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))
    
    # Analyze generated datasets
    print("\nGenerated Datasets:")
    for dataset_type in ["dataset1", "dataset2"]:
        for i in range(1, 6):
            dataset_name = f"{dataset_type}_variation_{i}.json"
            dataset_path = os.path.join(generated_dir, dataset_name)
            
            if os.path.exists(dataset_path):
                servers = analyze_dataset(dataset_path)
                
                print(f"\n{dataset_name}:")
                df = pd.DataFrame(servers)
                print(tabulate(df, headers='keys', tablefmt='grid', showindex=False))

if __name__ == "__main__":
    main() 