import json
import string
import math


class Signal_information(object):
    def __init__(self, path:list):
        self.latency = 0.0  # Initialize latency to 0
        self.path = path  # Initialize the path as a list of node labels

    @property
    def signal_power(self,signal_power):
        self.signal_power= signal_power
        return self.signal_power

    def update_signal_power(self,new_signal_power:float):
        self.signal_power=self.signal_power+new_signal_power
        return self.signal_power

    @property
    def noise_power(self,noise_power:float=0.0):
        self.noise_power=noise_power
        return self.noise_power

    @noise_power.setter
    def noise_power(self, noise_power:float=0.0):
        self.noise_power = self.noise_power+noise_power
        return self.noise_power

    def update_noise_power(self, new_noise_power:float):
        self.noise_power=self.noise_power+new_noise_power
        return self.noise_power

    @property
    def latency(self, latency:float=0.0):
        self.latency=latency
        return self.latency

    @latency.setter
    def latency(self, latency:float=0.0):
        self.latency= latency
        return self.latency

    def update_latency(self, new_latency):
        self.latency=self.latency+new_latency
        return self.latency

    @property
    def path(self, path:list):
        self.path=path
        return path

    @path.setter
    def path(self, path:list):
        self.path=path

    def update_path(self, node:str):
        self.path.append(node)
        return self.path


class Node(object):
    def __init__(self,label:str,position:tuple(float,float),connected_nodes:list[string],successive:dict[0]):
        pass

    @property
    def label(self,label:str):
        self.label=label
        return self.label

    @property
    def position(self,position:tuple(float,float)):
        self.position=position
        return self.position

    @property
    def connected_nodes(self, connected_nodes:list):
        self.connected_nodes=connected_nodes

    @property
    def successive(self, successive:dict[0]):
        self.successive=successive
        return self.successive

    @successive.setter
    def successive(self):
        pass

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
    def label(self, label:str):
        self.label=label
        return self.label

    @property
    def length(self, length:float):
        self.length=length
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
    def lines(self, line:Line):
        self.line=Line

    def draw(self):
        import matplotlib.pyplot as plt

        plt.figure()
        for line in self.lines.values():
            node1 = self.nodes[line.label[0]].get_position()
            node2 = self.nodes[line.label[1]].get_position()
            plt.plot([node1[0], node2[0]], [node1[1], node2[1]], 'bo-')
            print(self.node1)
        for node in self.nodes.values():
            plt.text(node.get_position()[0], node.get_position()[1], node.get_label(), fontsize=12)

        plt.show()

    # find_paths: given two node labels, returns all paths that connect the 2 nodes
    # as a list of node labels. Admissible path only if cross any node at most once
    def find_paths(self, label1, label2):
        pass

    # connect function set the successive attributes of all NEs as dicts
    # each node must have dict of lines and viceversa
    def connect(self):
        pass

    # propagate signal_information through path specified in it
    # and returns the modified spectral information
    def propagate(self, signal_information):
        pass
