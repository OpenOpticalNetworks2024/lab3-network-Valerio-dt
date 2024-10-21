import json

class Signal_information(object):
    def __init__(self, path:list):
        self.latency = 0.0  # Initialize latency to 0
        self.path = path  # Initialize the path as a list of node labels

    @property
    def signal_power(self,signal_power):
        self.signal_power= signal_power
        print(self.signal_power)
        return self.signal_power

    def update_signal_power(self,new_signal_power:float):
        self.signal_power=new_signal_power
        print(self.signal_power)
        return self.signal_power

    @property
    def noise_power(self,noise_power:float=0.0):
        self.noise_power=noise_power
        return self.noise_power

    @noise_power.setter
    def noise_power(self):
        pass

    def update_noise_power(self, new_noise_power:float):
        self.noise_power=new_noise_power


    @property
    def latency(self, latency:float=0.0):
        self.latency=latency
        return self.latency

    @latency.setter
    def latency(self):
        pass

    def update_latency(self, new_latency):
        self.latency=new_latency

    @property
    def path(self):
        pass

    @path.setter
    def path(self):
        pass

    def update_path(self):
        pass


class Node(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def position(self):
        pass

    @property
    def connected_nodes(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def propagate(self):
        pass


class Line(object):
    def __init__(self):
        pass

    @property
    def label(self):
        pass

    @property
    def length(self):
        pass

    @property
    def successive(self):
        pass

    @successive.setter
    def successive(self):
        pass

    def latency_generation(self):
        pass

    def noise_generation(self):
        pass

    def propagate(self):
        pass


class Network(object):
    def __init__(self):
        pass

    @property
    def nodes(self):
        pass

    @property
    def lines(self):
        pass

    def draw(self):
        pass

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
