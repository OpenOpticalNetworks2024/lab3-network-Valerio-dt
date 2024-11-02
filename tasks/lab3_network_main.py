import json
import math
import numpy as np
import matplotlib.pyplot as plt
import sys
import pandas as pd
from pathlib import Path
project_root=Path(__file__).parent.parent
core_path=project_root / 'core'

from core.elements import Network, Signal_information
# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file





with open(file_input, 'r') as f:
    network_data = json.load(f)

# Extract nodes and lines from the JSON data
nodes = network_data.get("nodes", {})
lines = network_data.get("lines", {})

# Initialize the Network instance with nodes and lines
network = Network(nodes,lines, file_input)
network.connect()
network.draw()
def generate_path(network: Network, signal_power: float):
    data = []
    for start_node in network.nodes:
        for end_node in network.nodes:
            if start_node != end_node:
                paths = network.find_paths(start_node, end_node)
                for path in paths:
                    signal_info = Signal_information(signal_power, path)
                    updated_signal_info = network.propagate(signal_info)
                    snr = 10 * math.log10(updated_signal_info.signal_power / updated_signal_info.noise_power) if updated_signal_info.noise_power != 0 else float('inf')
                    data.append({
                        "Path": "->".join(path),
                        "Latency (s)": updated_signal_info.latency,
                        "Noise Power (W)": updated_signal_info.noise_power,
                        "SNR (dB)": snr
                    })
    return pd.DataFrame(data)



df_paths = generate_path(network, signal_power=0.001)
OUTPUT_FILE = ROOT / 'weighted_path.csv'
df_paths.to_csv(OUTPUT_FILE, index=False)
print(f"Data saved to {OUTPUT_FILE}")


