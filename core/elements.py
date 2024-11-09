import json
import string
import numpy
import math
import matplotlib.pyplot as plt
import pandas as pd
from signal import signal
from typing import List
from pathlib import Path

class Signal_information(object):
    def __init__(self,signal_power:float, path:list):
        self._signal_power=signal_power
        self._latency =float(0.0)
        self._noise_power=float(0.0)
        self._path = path

    @property
    def signal_power(self):
        return self._signal_power

    def update_signal_power(self,new_signal_power:float):
        self._signal_power=self.signal_power+new_signal_power


    @property
    def noise_power(self):
        return self._noise_power

    @noise_power.setter
    def noise_power(self, noise_power:float):
        self._noise_power = noise_power


    def update_noise_power(self, new_noise_power:float):
        self._noise_power=self._noise_power+new_noise_power

    @property
    def latency(self):
        return self._latency

    @latency.setter
    def latency(self, latency:float):
        self._latency= latency


    def update_latency(self, new_latency):
        self._latency=self._latency+new_latency


    @property
    def path(self, path:list):
        return path

    @path.setter
    def path(self, path:list):
        self._path=path

    def update_path(self, node:str):
        self._path.append(node)



class Node(object):
    def __init__(self,label:str,position:tuple,connected_nodes:list[string]):
        self._label=label
        self._position=position
        self._connected_nodes=connected_nodes
        self.successive= {}

    @property
    def label(self):
        return self._label
    @label.setter
    def label(self, label):
        self._label=label


    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive:dict):
        self._successive=successive

    def propagate(self, signal: Signal_information):
        if len(signal._path) <= 1 or self._label in signal._path[1:]:
            return
        if len(signal._path) <= 1 and signal._path[0] == self._label:
            return

        current_node_label = signal._path.pop(0)
        signal.update_path(self._label)

        if signal._path:
            next_node_label = signal._path[0]
            next_line = self._successive.get(next_node_label)
            if next_line:
                next_line.propagate(signal)


class Line(object):
    def __init__(self, label:str, length:float):
        self._label=label
        self._length=length
        self._successive={}

    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @successive.setter
    def successive(self, successive:dict):
        self._successive=successive

    def latency_generation(self):
        return self._length / ((2/3)*3*10**8)

    def noise_generation(self, signal_power:float):
        noise_generated=1**-9*signal_power*self._length
        return noise_generated

    def propagate(self, signal:Signal_information):
      signal.update_latency(self.latency_generation())
      signal.update_noise_power(self.noise_generation(signal._signal_power))

      if len(signal._path) > 1:

          signal._path.pop(0)
          next_node_label = signal._path[0]

          if next_node_label in self._successive:
              next_node = self._successive[next_node_label]
              next_node.propagate(signal)




class Network(object):
    def __init__(self, json_file):
        self.nodes={}
        self.lines={}

        with open(json_file, 'r') as file:
            data = json.load(file)

            for node_label, node_data in data.items():
                node = Node(node_label, node_data['position'], node_data['connected_nodes'])
                self.nodes[node_label] = node

            for node_label, node in self.nodes.items():
                for connected_node_label in node.connected_nodes:
                    node_position = node.position
                    connected_node_position = self.nodes[connected_node_label].position
                    length = math.sqrt((node_position[0] - connected_node_position[0]) ** 2 + (node_position[1] - connected_node_position[1]) ** 2)
                    line_label = node_label + connected_node_label
                    line = Line(line_label, length)
                    self.lines[line_label] = line



    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, start: str, end: str) -> List[List[str]]:
        paths = []

        def recursive_find_paths(current_node, end_node, current_path):
            current_path.append(current_node)

            if current_node == end_node:
                paths.append(current_path[:])
            else:
                for next_node in self.nodes[current_node].connected_nodes:
                    if next_node not in current_path:
                        recursive_find_paths(next_node, end_node, current_path)

            current_path.pop()
        recursive_find_paths(start, end, [])

        unique_paths = [list(path) for path in {tuple(p) for p in paths}]
        return unique_paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for node_label, node in self.nodes.items():
            for connected_node_label in node.connected_nodes:
                line_label_forward = node_label + connected_node_label
                line_label_reverse = connected_node_label + node_label

                position1 = node.position
                position2 = self.nodes[connected_node_label].position
                line_length = math.sqrt((position1[0] - position2[0]) ** 2 + (position1[1] - position2[1]) ** 2)

                if line_label_forward not in self.lines:
                    self.lines[line_label_forward] = Line(label=line_label_forward, length=line_length)

                if line_label_reverse not in self.lines:
                    self.lines[line_label_reverse] = Line(label=line_label_reverse, length=line_length)

                node.successive[connected_node_label] = self.lines[line_label_forward]
                self.lines[line_label_forward].successive[connected_node_label] = self.nodes[connected_node_label]

                self.nodes[connected_node_label].successive[node_label] = self.lines[line_label_reverse]
                self.lines[line_label_reverse].successive[node_label] = node

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self,signal: Signal_information):
        start_node = self.nodes[signal._path[0]]
        start_node.propagate(signal)
        return signal

    def draw(self):

        plt.figure()
        for line in self.lines.values():
            node1 = self.nodes[line.label[0]].position
            node2 = self.nodes[line.label[1]].position
            plt.plot([node1[0], node2[0]], [node1[1], node2[1]], 'bo-')

        for node in self.nodes.values():
            plt.text(node.position[0], node.position[1], node.label, fontsize=12)

        save_path = Path("..") / "results" / "network_plot.png"

        plt.savefig(save_path, format='png')
        plt.show()



