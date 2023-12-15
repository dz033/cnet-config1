import argparse
import networkx as nx
import os
import pickle
import csv
import random

class NDBEntry(object):
    def __init__(self, path, destination, prefix, shortest_path, additional_features, traffic_size=1):
        self.path = path
        self.prefix = prefix
        self.destination = destination
        self.shortest_path = shortest_path
        self.additional_features = additional_features
        self.traffic_size = traffic_size

    def to_csv_row(self):
        return [
            " -> ".join(str(node) for node in self.path),
            self.destination,
            self.prefix,
            self.traffic_size,
            self.shortest_path
        ]

def load_example(topo_path, data_path):
    with open(data_path, 'rb') as infile:
        data = pickle.load(infile)

    with open(topo_path, 'rb') as infile:
        topo = pickle.load(infile)

    paths = []
    for path in data['paths']:
        shortest_path = len(path[0]) <= len(nx.shortest_path(topo, source=path[0][0], target=path[0][-1]))
        paths.append(NDBEntry(path[0], path[1], path[2], shortest_path, path[4], path[3]))

    return paths

def export_to_csv(paths, filename):
    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Path', 'Organization', 'Prefix', 'Bandwidth', 'Shortest Path'])

        for entry in paths:
            writer.writerow(entry.to_csv_row())

def main(example_path):
    topo_file = "ndb_topo.out"
    data_file = "ndb_dump.out"

    topo_path = os.path.join(example_path, topo_file)
    data_path = os.path.join(example_path, data_file)

    paths = load_example(topo_path, data_path)
    export_to_csv(paths, 'network_data.csv')

    print(f"Exported {len(paths)} entries to network_data.csv")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help='path to the directory containing the example', type=str)
    parsed_args = parser.parse_args()
    main(parsed_args.path)

    # path = "examples/att_na/AttMpls-10-egress_100"
    # main(path)
