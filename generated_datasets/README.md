# Generated EdgeSimPy Datasets

This directory contains 10 generated datasets based on two original datasets with variations in memory and CPU resources.

## Dataset Descriptions

### Original Datasets
- **dataset1.json** (Alta Demanda e Recursos Limitados): Focus on high demand with limited resources
  - Base memory: 8192 (8GB)
  - Base CPU cores: 8

- **dataset2.json** (Alta Mobilidade com Recursos Limitados): Focus on high mobility with limited resources
  - Base memory: 10240 (10GB) for some servers, 8192 (8GB) for others
  - Base CPU cores: Varies (7 or 8 cores)

### Generated Variations
The generated datasets maintain the same network architecture and structure as the original datasets, but with ±10% random variation in:
- Memory resources
- CPU cores

## Generation Method
Each dataset was created using a Python script that:
1. Loads the original dataset
2. Randomly varies each EdgeServer's memory and CPU cores by up to ±10%
3. Preserves all other attributes and relationships

## Datasets

### Based on Dataset 1 (Alta Demanda e Recursos Limitados)
- dataset1_variation_1.json
- dataset1_variation_2.json
- dataset1_variation_3.json
- dataset1_variation_4.json
- dataset1_variation_5.json

### Based on Dataset 2 (Alta Mobilidade com Recursos Limitados)
- dataset2_variation_1.json
- dataset2_variation_2.json
- dataset2_variation_3.json
- dataset2_variation_4.json
- dataset2_variation_5.json

## Purpose
These datasets with similar architectures but variations in resources are intended for evaluating the standard deviation of solutions in similar scenarios. 