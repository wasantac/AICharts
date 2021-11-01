import random as rd

import random as rd
import matplotlib.pyplot as plt
import squarify
import xNB_Classes
import networkx as nx
word_dicc = {}
with open("test.txt","r") as file:
    words = file.readlines()
    for line in words:
        word_dicc.update({line.rstrip("\n"):rd.random()})

def AIChart_plot_data_treemap(xAAD):
    dictionary = xAAD.dictionary
    squarify.plot(list(dictionary.values())[:10],label=list(dictionary.keys())[:10],text_kwargs={'color': 'white', 'size': 18})
    plt.axis('off')
    plt.savefig('treemap.png')
    plt.show()
    
data = xNB_Classes.xAAD(rd.random(),word_dicc)


def AIChart_plot_data_word_graph(xAAD):
    dictionary = xAAD.dictionary
    G = nx.Graph()
    G.add_node(1)
    G.add_nodes_from([2, 3])
    G.add_edge(1, 2)
    e = (2, 3)
    G.add_edge(*e)
    nx.draw(G,with_labels=True, font_weight='bold')
    plt.show()

AIChart_plot_data_word_graph(data)