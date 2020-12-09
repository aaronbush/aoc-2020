import networkx as nx
import matplotlib.pyplot as plt
import sys

g = nx.DiGraph()

with open(sys.argv[1]) as f:
    for l in f:
        to_node = " ".join(l.split()[:2])
        inner_bags = " ".join(l.split()[4:]).split(',')
        for bag in inner_bags:
            if 'no other' in bag:
                continue
            qty = bag.split()[0]
            color = " ".join(bag.split()[1:3])
            print(f'{to_node} holds {qty} {color}')
            g.add_edge(color, to_node, qty=qty)

pos = nx.spring_layout(g)
print(g.number_of_edges())
print(g.number_of_nodes())
# nx.draw(g, pos=nx.nx_agraph.graphviz_layout(g), with_labels=1)
# plt.savefig('out.png')

print(g.in_edges('shiny gold'))


# assumes no cycles
def nodes_in(node_name: str, graph):
    for pred in g.predecessors(node_name):
        print(pred)
        nodes_in(pred, g)
