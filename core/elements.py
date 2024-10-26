import json
import string
import math
import pandas as pd
from signal import signal


class Signal_information(object):
    def __init__(self,signal_power:float, path:list):
        self.signal_power=signal_power
        self.latency = 0.0
        self.noise_power=0.0
        self.path = path

    @property
    def signal_power(self):
        return self.signal_power

    def update_signal_power(self,new_signal_power:float):
        self.signal_power=self.signal_power+new_signal_power
        return self.signal_power

    @property
    def noise_power(self):
        return self.noise_power

    @noise_power.setter
    def noise_power(self, noise_power:float):
        self.noise_power = noise_power
        return self.noise_power

    def update_noise_power(self, new_noise_power:float):
        self.noise_power=self.noise_power+new_noise_power
        return self.noise_power

    @property
    def latency(self):
        return self.latency

    @latency.setter
    def latency(self, latency:float):
        self.latency= latency
        return self.latency

    def update_latency(self, new_latency):
        self.latency=self.latency+new_latency
        return self.latency

    @property
    def path(self, path:list):
        return path

    @path.setter
    def path(self, path:list):
        self.path=path

    def update_path(self, node:str):
        self.path.append(node)
        return self.path


class Node(object):
    def __init__(self,label:str,position:tuple,connected_nodes:list[string], successive:dict):
        self.label=label
        self.position=position
        self.connected_nodes=connected_nodes
        self.successive=successive

    @property
    def label(self):
        return self.label

    @property
    def position(self):
        return self.position

    @property
    def connected_nodes(self):
        return self.connected_nodes

    @property
    def successive(self):
        return self.successive

    @successive.setter
    def successive(self, successive:dict):
        self.successive=successive

    def propagate(self, signal:Signal_information):
        signal.update_path(self.label)
        next_line = self.successive[signal.path[-1]]
        next_line.propagate(signal)


class Line(object):
    def __init__(self, label:str, length:float):
        self.label=label
        self.length=length
        self.successive={}

    @property
    def label(self):
        return self.label

    @property
    def length(self):
        return self.length

    @property
    def successive(self):
        return self.successive

    @successive.setter
    def successive(self, successive:dict):
        self.successive=successive

    def latency_generation(self):
        return self.length / (2/3*3*10**8)

    def noise_generation(self, signal_power:float):
        return 1e-9*signal_power*self.length

    def propagate(self, signal:Signal_information):
        signal.update_latency(self.latency_generation())
        signal.update_noise_power(self.noise_generation(signal.get_signal_power()))
        next_node = self.successive[signal.path[-1]]
        next_node.propagate(signal)


class Network(object):
    def __init__(self, json_file:str):
        self.nodes = {}
        self.lines = {}

    @property
    def nodes(self, node:Node):
        self.nodes=node

    @property
    def lines(self):
        self.line=Line

        with open(json, 'r') as file:
            data = json.load(file)
            for node_label, node_data in data['nodes'].items():
                node = Node(node_label, node_data['position'], node_data['connected_nodes'])
                self.nodes[node_label] = node

            for node_label, node in self.nodes.items():
                for connected_node_label in node.connected_nodes:
                    node_position = node.position
                    connected_node_position = self.nodes[connected_node_label].position
                    length = math.sqrt((node_position[0] - connected_node_position[0]) ** 2 +
                                       (node_position[1] - connected_node_position[1]) ** 2)
                    line_label = node_label + connected_node_label
                    line = Line(line_label, length)
                    self.lines[line_label] = line



    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1:str, label2:str, path=[]):
        path = path + [label1]
        if label1 == label2:
            return [path]
        if label1 not in self.nodes:
            return []
        paths = []
        for node in self.nodes[label1].connected_nodes:
            if node not in path:
                newpaths = self.find_paths(node, label2, path)
                for newpath in newpaths:
                    paths.append(newpath)
        return paths

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        for node_label, node in self.nodes.items():
            for connected_node_label in node.connected_nodes:
                line_label = node_label + connected_node_label
                node.successive[connected_node_label] = self.lines[line_label]
                self.lines[line_label].successive[node_label] = self.nodes[connected_node_label]

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self,signal: Signal_information):
        start_node = self.nodes[signal.path[0]]
        start_node.propagate(signal)
        return signal

    def draw(self):
        import matplotlib.pyplot as plt

        plt.figure()
        for line in self.lines.values():
            node1 = self.nodes[line.label[0]].position
            node2 = self.nodes[line.label[1]].position
            plt.plot([node1[0], node2[0]], [node1[1], node2[1]], 'bo-')

        for node in self.nodes.values():
            plt.text(node.position[0], node.position[1], node.label, fontsize=12)

        plt.show()




