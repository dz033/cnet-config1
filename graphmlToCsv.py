import networkx as nx
import csv

def graphml_to_csv(graphml_file, nodes_csv, edges_csv):

    G = nx.read_graphml(graphml_file)

    # writing nodes to csv
    with open(nodes_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'label', 'type', 'country', 'latitude', 'longitude', 'internal'])

        for node_id in G.nodes:
            node_data = G.nodes[node_id]
            writer.writerow([
                node_id,
                node_data.get('label', ''),
                node_data.get('type', ''),
                node_data.get('Country', ''),
                node_data.get('Latitude', ''),
                node_data.get('Longitude', ''),
                node_data.get('Internal', '')
            ])

    # writing edges to csv
    with open(edges_csv, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['id', 'source', 'target', 'link_label', 'key'])

        for edge_id, (source, target, data) in enumerate(G.edges(data=True)):
            writer.writerow([
                edge_id,
                source,
                target,
                data.get('LinkLabel', ''),
                data.get('key', '')
            ])


graphml_file_path = 'examples/att_na/AttMpls.graphml'
nodes_csv_path = './nodes.csv'
edges_csv_path = './edges.csv'

graphml_to_csv(graphml_file_path, nodes_csv_path, edges_csv_path)
