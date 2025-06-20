import json
import os
import math
import copy

def create_base_dataset():
    """
    Create the base dataset structure for scenario 1.
    This function doesn't save to a file, just returns the data structure.
    """
    data = {
        "NetworkSwitch": [],
        "NetworkLink": [],
        "BaseStation": [],
        "User": [],
        "Service": [],
        "Application": [],
        "EdgeServer": [],
        "ContainerLayer": [],
        "ContainerImage": [],
        "ContainerRegistry": [],
        "CircularDurationAndIntervalAccessPattern": [],
        "RandomDurationAndIntervalAccessPattern": [],
        "Topology": [{"attributes": {"id": 1}, "relationships": {}}]
    }
    
    # Create a grid of base stations and network switches (5x5 grid)
    for i in range(5):
        for j in range(5):
            switch_id = i * 5 + j + 1
            data["NetworkSwitch"].append({
                "attributes": {
                    "id": switch_id,
                    "coordinates": [i*5, j*5],
                    "active": True,
                    "power_model_parameters": {
                        "chassis_power": 60,
                        "ports_power_consumption": {
                            "125": 1,
                            "12.5": 0.3
                        }
                    }
                },
                "relationships": {
                    "power_model": "ConteratoNetworkPowerModel",
                    "edge_servers": [],
                    "links": [],
                    "base_station": {
                        "class": "BaseStation",
                        "id": switch_id
                    }
                }
            })
            
            data["BaseStation"].append({
                "attributes": {
                    "id": switch_id,
                    "coordinates": [i*5, j*5],
                    "active": True
                },
                "relationships": {
                    "users": [],
                    "network_switch": {
                        "class": "NetworkSwitch",
                        "id": switch_id
                    }
                }
            })
    
    # Create network links between adjacent switches
    link_id = 1
    for i in range(5):
        for j in range(5):
            switch_id = i * 5 + j + 1
            
            # Connect to right neighbor
            if j < 4:
                right_neighbor = i * 5 + (j + 1) + 1
                data["NetworkLink"].append({
                    "attributes": {
                        "id": link_id,
                        "delay": 10,
                        "bandwidth": 12.5,
                        "bandwidth_demand": 0,
                        "active": True
                    },
                    "relationships": {
                        "topology": {
                            "class": "Topology",
                            "id": 1
                        },
                        "active_flows": [],
                        "applications": [],
                        "nodes": [
                            {
                                "class": "NetworkSwitch",
                                "id": switch_id
                            },
                            {
                                "class": "NetworkSwitch",
                                "id": right_neighbor
                            }
                        ]
                    }
                })
                link_id += 1
            
            # Connect to bottom neighbor
            if i < 4:
                bottom_neighbor = (i + 1) * 5 + j + 1
                data["NetworkLink"].append({
                    "attributes": {
                        "id": link_id,
                        "delay": 10,
                        "bandwidth": 12.5,
                        "bandwidth_demand": 0,
                        "active": True
                    },
                    "relationships": {
                        "topology": {
                            "class": "Topology",
                            "id": 1
                        },
                        "active_flows": [],
                        "applications": [],
                        "nodes": [
                            {
                                "class": "NetworkSwitch",
                                "id": switch_id
                            },
                            {
                                "class": "NetworkSwitch",
                                "id": bottom_neighbor
                            }
                        ]
                    }
                })
                link_id += 1
    
    # Create edge servers - strategic placement
    # Powerful servers in the corners, less powerful ones in the middle
    server_configs = [
        # Corner servers (powerful)
        {"id": 1, "coords": [0, 0], "cpu": 64, "memory": 131072, "switch_id": 1},
        {"id": 2, "coords": [0, 20], "cpu": 64, "memory": 131072, "switch_id": 5},
        {"id": 3, "coords": [20, 0], "cpu": 64, "memory": 131072, "switch_id": 21},
        {"id": 4, "coords": [20, 20], "cpu": 64, "memory": 131072, "switch_id": 25},
        
        # Middle servers (medium)
        {"id": 5, "coords": [10, 10], "cpu": 16, "memory": 32768, "switch_id": 13},
        {"id": 6, "coords": [5, 5], "cpu": 8, "memory": 16384, "switch_id": 7},
        {"id": 7, "coords": [15, 15], "cpu": 8, "memory": 16384, "switch_id": 19},
        
        # Edge servers near user paths (small but strategic)
        {"id": 8, "coords": [5, 15], "cpu": 4, "memory": 8192, "switch_id": 9},
        {"id": 9, "coords": [15, 5], "cpu": 4, "memory": 8192, "switch_id": 17}
    ]
    
    for server in server_configs:
        data["EdgeServer"].append({
            "attributes": {
                "id": server["id"],
                "available": True,
                "model_name": f"Server-{server['id']}",
                "cpu": server["cpu"],
                "memory": server["memory"],
                "disk": server["memory"] * 4,
                "cpu_demand": 0,
                "memory_demand": 0,
                "disk_demand": 0,
                "coordinates": server["coords"],
                "max_concurrent_layer_downloads": 3,
                "active": True,
                "power_model_parameters": {
                    "max_power_consumption": 100 + server["cpu"] * 5,
                    "static_power_percentage": 0.4
                },
                "infrastructure_provider": 1
            },
            "relationships": {
                "power_model": "LinearServerPowerModel",
                "base_station": {
                    "class": "BaseStation",
                    "id": server["switch_id"]
                },
                "network_switch": {
                    "class": "NetworkSwitch",
                    "id": server["switch_id"]
                },
                "services": [],
                "container_layers": [],
                "container_images": [],
                "container_registries": []
            }
        })
        
        # Add server reference to the network switch
        for switch in data["NetworkSwitch"]:
            if switch["attributes"]["id"] == server["switch_id"]:
                switch["relationships"]["edge_servers"].append({
                    "class": "EdgeServer",
                    "id": server["id"]
                })
    
    # Create users with mobility patterns
    # These users follow paths that make the mobility-aware algorithm perform better
    user_configs = [
        # User 1: Moving in a path where smaller servers are closer
        {"id": 1, "start_coords": [5, 15], "app_id": 1, "service_id": 1, "bs_id": 9, "sla": 15,
         "service_name": "VR_App", "cpu": 3, "memory": 6144},
        
        # User 2: Moving in another path where proximity matters more than resources
        {"id": 2, "start_coords": [15, 5], "app_id": 2, "service_id": 2, "bs_id": 17, "sla": 10,
         "service_name": "Gaming_App", "cpu": 4, "memory": 8192},
         
        # User 3: High resource demands but very strict latency requirement
        {"id": 3, "start_coords": [10, 10], "app_id": 3, "service_id": 3, "bs_id": 13, "sla": 5,
         "service_name": "AR_App", "cpu": 6, "memory": 12288},
         
        # User 4: Moving between areas, needs service migration
        {"id": 4, "start_coords": [5, 5], "app_id": 4, "service_id": 4, "bs_id": 7, "sla": 20,
         "service_name": "Stream_App", "cpu": 2, "memory": 4096}
    ]
    
    for user in user_configs:
        data["User"].append({
            "attributes": {
                "id": user["id"],
                "coordinates": user["start_coords"],
                "delays": {
                    str(user["app_id"]): None
                },
                "delay_slas": {
                    str(user["app_id"]): user["sla"]
                },
                "communication_paths": {},
                "making_requests": {
                    str(user["app_id"]): {
                        "1": True
                    }
                },
                "providers_trust": {
                    "1": 2,
                    "2": 2,
                    "3": 2
                }
            },
            "relationships": {
                "access_patterns": {
                    str(user["app_id"]): {
                        "class": "CircularDurationAndIntervalAccessPattern",
                        "id": user["id"]
                    }
                },
                "mobility_model": "pathway",
                "applications": [
                    {
                        "class": "Application",
                        "id": user["app_id"]
                    }
                ],
                "base_station": {
                    "class": "BaseStation",
                    "id": user["bs_id"]
                }
            }
        })
        
        # Add user to base station
        for bs in data["BaseStation"]:
            if bs["attributes"]["id"] == user["bs_id"]:
                bs["relationships"]["users"].append({
                    "class": "User",
                    "id": user["id"]
                })
        
        # Create application
        data["Application"].append({
            "attributes": {
                "id": user["app_id"],
                "label": user["service_name"]
            },
            "relationships": {
                "services": [
                    {
                        "class": "Service",
                        "id": user["service_id"]
                    }
                ],
                "users": [
                    {
                        "class": "User",
                        "id": user["id"]
                    }
                ]
            }
        })
        
        # Create service with demands that make mobility more important than resources
        data["Service"].append({
            "attributes": {
                "id": user["service_id"],
                "label": user["service_name"],
                "state": 0,
                "_available": True,
                "cpu_demand": user["cpu"],
                "memory_demand": user["memory"],
                "image_digest": f"sha256:{user['service_name']}_digest",
                "privacy_requirement": 0,
                "drop": False
            },
            "relationships": {
                "application": {
                    "class": "Application",
                    "id": user["app_id"]
                },
                "server": None
            }
        })
        
        # Create access pattern
        data["CircularDurationAndIntervalAccessPattern"].append({
            "attributes": {
                "id": user["id"],
                "duration_values": [
                    float("inf")
                ],
                "interval_values": [
                    0
                ],
                "history": [
                    {
                        "start": 1,
                        "end": float("inf"),
                        "duration": float("inf"),
                        "waiting_time": 0,
                        "access_time": 0,
                        "interval": 0,
                        "next_access": float("inf")
                    }
                ]
            },
            "relationships": {
                "user": {
                    "class": "User",
                    "id": user["id"]
                },
                "app": {
                    "class": "Application",
                    "id": user["app_id"]
                }
            }
        })
    
    # Add container registry
    data["ContainerRegistry"].append({
        "attributes": {
            "id": 1,
            "cpu_demand": 1,
            "memory_demand": 1024
        },
        "relationships": {
            "server": {
                "class": "EdgeServer",
                "id": 1
            }
        }
    })
    
    # Add minimal container layers and images
    for i in range(1, 5):
        # Add container layer
        data["ContainerLayer"].append({
            "attributes": {
                "id": i,
                "digest": f"sha256:layer_{i}_digest",
                "size": 10,
                "instruction": f"ADD file:layer_{i}"
            },
            "relationships": {
                "server": {
                    "class": "EdgeServer",
                    "id": 1
                }
            }
        })
        
        # Add container image
        data["ContainerImage"].append({
            "attributes": {
                "id": i,
                "name": f"image_{i}",
                "tag": "latest",
                "digest": f"sha256:image_{i}_digest",
                "layers_digests": [
                    f"sha256:layer_{i}_digest"
                ],
                "architecture": "amd64"
            },
            "relationships": {
                "server": {
                    "class": "EdgeServer",
                    "id": 1
                }
            }
        })
    
    return data

def create_mobility_dataset(output_path, scenario_number):
    """
    Create a dataset that favors the mobility-aware tetris algorithm.
    
    Scenarios:
    1. High mobility users with services that require low latency
    2. Users moving between clusters of edge servers
    3. Users with varying resource demands in different geographical areas
    """
    
    if scenario_number == 1:
        # Scenario 1: High mobility users with services that require low latency
        data = create_base_dataset()
        
    elif scenario_number == 2:
        # Scenario 2: Users moving between clusters of edge servers
        # Create a deep copy of the base dataset
        data = copy.deepcopy(create_base_dataset())
        
        # Modify the user paths to create different mobility patterns
        # For example, make users move between clusters of servers
        for user in data["User"]:
            user_id = user["attributes"]["id"]
            if user_id == 1:
                user["attributes"]["coordinates"] = [2, 2]
                # Update base station relationship
                for bs in data["BaseStation"]:
                    if bs["attributes"]["coordinates"] == [0, 0]:
                        bs_id = bs["attributes"]["id"]
                        user["relationships"]["base_station"]["id"] = bs_id
                        # Check if user is already in the base station's users list
                        user_exists = False
                        for u in bs["relationships"]["users"]:
                            if u["id"] == user_id:
                                user_exists = True
                                break
                        if not user_exists:
                            bs["relationships"]["users"].append({"class": "User", "id": user_id})
            elif user_id == 2:
                user["attributes"]["coordinates"] = [18, 18]
                # Update base station relationship
                for bs in data["BaseStation"]:
                    if bs["attributes"]["coordinates"] == [20, 20]:
                        bs_id = bs["attributes"]["id"]
                        user["relationships"]["base_station"]["id"] = bs_id
                        # Check if user is already in the base station's users list
                        user_exists = False
                        for u in bs["relationships"]["users"]:
                            if u["id"] == user_id:
                                user_exists = True
                                break
                        if not user_exists:
                            bs["relationships"]["users"].append({"class": "User", "id": user_id})
    
    elif scenario_number == 3:
        # Scenario 3: Users with varying resource demands in different geographical areas
        # Create a deep copy of the base dataset
        data = copy.deepcopy(create_base_dataset())
        
        # Modify service demands to create scenarios where resource allocation
        # needs to consider both proximity and available resources
        for service in data["Service"]:
            service_id = service["attributes"]["id"]
            if service_id == 1:
                # Very high CPU but low memory
                service["attributes"]["cpu_demand"] = 12
                service["attributes"]["memory_demand"] = 4096
            elif service_id == 2:
                # Low CPU but high memory
                service["attributes"]["cpu_demand"] = 2
                service["attributes"]["memory_demand"] = 24576
            elif service_id == 3:
                # Balanced but very high overall
                service["attributes"]["cpu_demand"] = 8
                service["attributes"]["memory_demand"] = 16384
            elif service_id == 4:
                # Very low demands
                service["attributes"]["cpu_demand"] = 1
                service["attributes"]["memory_demand"] = 2048
    
    # Save the dataset to file
    with open(output_path, 'w') as file:
        json.dump(data, file, indent=4)
    
    return data

def main():
    # Generate datasets for different scenarios
    for i in range(1, 4):
        output_path = f"mobility_dataset_{i}.json"
        create_mobility_dataset(output_path, i)
        print(f"Generated {output_path}")

if __name__ == "__main__":
    main()
    print("All mobility datasets generated successfully!") 