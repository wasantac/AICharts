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
    df = pd.DataFrame.from_dict({'token':k,'weight':v}) #Dataframe to sort the data
    df_sorted = df.sort_values(by='weight',ascending=False).drop_duplicates(subset=['token']) #Sorted dataframe
    tokens = df_sorted['token'].to_list()
    weights = df_sorted['weight'].to_list() 
    if limit != 0: 
        if len(tokens) >= limit:
            tokens = tokens[:limit]
            weights = weights[:limit]
    cmap = cm.get_cmap('copper',100) #Color map for the treemap
    mini = min(weights)
    maxi = max(weights)
    norm = mpl.colors.Normalize(vmin=mini,vmax=maxi)
    colors = [cmap(norm(value)) for value in weights] #Color mapping normalization
    fig = figure(figsize=(10,10)) #Figure size
    ax = fig.add_subplot(111,aspect="equal")
    ax = squarify.plot(weights,label=tokens,text_kwargs={'color':'#ffffff' ,'size': 8},color=colors)
    plt.axis('off')
    ax.set_title(title)
    if saveImg:
        plt.savefig('{title}.png'.format(title=title))
    plt.show()
    



def AIChart_plot_data_word_graph(xAAD,text_list):
    dictionary = xAAD.dictionary
    G = nx.Graph()
    graph_dictionary = {}
    for k,v in dictionary.items():
        graph_dictionary.update({k:{'weight':v,'edges':[]}}) 
    keys = list(dictionary.keys())
    for k in range(len(text_list)): #Checks if words are near each other
        token = text_list[k]
        try:
            if text_list[k-1] not in graph_dictionary[token]:
                graph_dictionary[token]['edges'].append(text_list[k-1])
        except:
            pass
        try:
            if text_list[k+1] not in graph_dictionary[token]:
                graph_dictionary[token]['edges'].append(text_list[k+1])
        except:
            pass
    G.add_nodes_from(keys)
    node_size = []
    for k,v in graph_dictionary.items(): 
        node_size.append(10+500*v['weight']) #Linear function to adjust node size
        for edge in v['edges']:
            G.add_edge(k,edge)
    pos = nx.spring_layout(G, k=0.2, iterations=30)
    nx.draw(G,pos,with_labels=True,node_size=node_size,font_color="black",font_size=10,edge_color='#999999',width=1,node_color="#ff5757")
    plt.show()


def AIChart_plot_data_text(xAAD,text_list):
    dictionary = xAAD.dictionary
    fig = plt.figure()
    contador = 0
    while len(text_list) > contador*contador:
        contador = contador + 1
    next_line = 0
    next_word = 0
    for i in range(len(text_list)):
        if next_word % contador == 0 or next_word > contador:
            next_line = next_line + 1
            next_word = 0
        word = text_list[i]
        font_size = dictionary[word] * 30
        if font_size < 8:
            font_size = 9
        if font_size < 15:
            plt.text(next_word,contador - next_line,word,fontsize=font_size,color='blue',fontstyle='oblique',wrap=True)
        else:
            plt.text(next_word,contador - next_line,word,fontsize=font_size,color='red',wrap=True)
        
        next_word = next_word + len(word)*0.15*font_size/30 + 0.2

        #plt.text(j,contador - i - 1,text_list[indice],fontsize=font_size,wrap=True)
    plt.axis([0,contador+1,0,contador+1])
    plt.axis('off')
    plt.show()
#test
word_dicc = {}
full_text_list = []
with open("test.txt","r") as file:
    words = file.readlines()
    for line in words:
        full_text_list.append(line.rstrip("\n"))
        word_dicc.update({line.rstrip("\n"):rd.random()})
data = xNB_Classes.xAAD(rd.random(),word_dicc)


AIChart_plot_data_treemap(data)
AIChart_plot_data_word_graph(data,full_text_list)
AIChart_plot_data_text(data,full_text_list)