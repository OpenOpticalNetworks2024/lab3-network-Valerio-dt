import json
import sys
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
core_path= Path(__file__).parent.parent / 'core'
sys.path.append(str(core_path))
from elements.py import Network, Signal_information

# Exercise Lab3: Network

ROOT = Path(__file__).parent.parent
INPUT_FOLDER = ROOT / 'resources'
file_input = INPUT_FOLDER / 'nodes.json'


# Load the Network from the JSON file, connect nodes and lines in Network.
# Then propagate a Signal Information object of 1mW in the network and save the results in a dataframe.
# Convert this dataframe in a csv file called 'weighted_path' and finally plot the network.
# Follow all the instructions in README.md file

data = []
for start_node in network.nodes:
    for end_node in network.nodes:
        if start_node != end_node:
            paths = network.find_paths(start_node, end_node)
            for path in paths:
                signal_info = Signal_information(signal_power, path)
                updated_signal_info = network.propagate(signal_info)
                snr = 10 * math.log10(
                    updated_signal_info.signal_power / updated_signal_info.noise_power) if updated_signal_info.noise_power != 0 else float(
                    'inf')
                data.append({
                    "Path": "->".join(path),
                    "Latency (s)": updated_signal_info.latency,
                    "Noise Power (W)": updated_signal_info.noise_power,
                    "SNR (dB)": snr
                })

