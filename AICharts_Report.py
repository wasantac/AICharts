import random as rd
import pandas as pd
import random as rd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
from matplotlib.pyplot import figure
import squarify
import xNB_Classes
import networkx as nx


def AIChart_plot_data_treemap(xAAD,title='Treemap',limit=0,saveImg = False):
    dictionary = xAAD.dictionary
    k,v = dictionary.keys(),dictionary.values()
    df = pd.DataFrame.from_dict({'token':k,'weight':v})
    df_sorted = df.sort_values(by='weight',ascending=False).drop_duplicates(subset=['token'])
    tokens = df_sorted['token'].to_list()
    weights = df_sorted['weight'].to_list()
    if limit != 0:
        if len(tokens) >= limit:
            tokens = tokens[:limit]
            weights = weights[:limit]
    cmap = cm.get_cmap('copper',100)
    mini = min(weights)
    maxi = max(weights)
    norm = mpl.colors.Normalize(vmin=mini,vmax=maxi)
    colors = [cmap(norm(value)) for value in weights]
    fig = figure(figsize=(10,10))
    ax = fig.add_subplot(111,aspect="equal")
    ax = squarify.plot(weights,label=tokens,text_kwargs={'color':'white' ,'size': 8},color=colors)
    plt.axis('off')
    ax.set_title(title)
    if saveImg:
        plt.savefig('{title}.png'.format(title=title))
    plt.show()
    



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


word_dicc = {}
with open("test.txt","r") as file:
    words = file.readlines()
    for line in words:
        word_dicc.update({line.rstrip("\n"):rd.random()})
data = xNB_Classes.xAAD(rd.random(),word_dicc)

AIChart_plot_data_treemap(data)