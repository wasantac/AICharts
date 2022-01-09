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

plt.rcParams['text.latex.preamble'] = r'\usepackage{mathptmx}'  # load times roman font
plt.rcParams['font.family'] = 'serif'  # use serif font as default
plt.rcParams['text.usetex'] = True  # enable LaTeX rendering globally


def AIChart_save_file(title,saveImg = False,savePDF = False,saveEPS= False):
    if saveImg:
        plt.savefig('{title}.png'.format(title=title)) #saves as png
    if savePDF:
        plt.savefig('{title}.pdf'.format(title=title)) #saves as pdf
    if saveEPS:
        plt.savefig('{title}.eps'.format(title=title),format='eps')#saves as eps


def AIChart_plot_data_treemap(xAAD,mode='p',title='Treemap',limit=0,saveImg = False,savePDF = False,saveEPS=False,show=True):
    """
        This is an implementation of a treemap shown in [3] for text categorization. 

        [3] T. Bock, "Seven (beautiful) alternatives to word clouds for visualizing data from long lists.", Displayr, 2021. [Online]. Available: https://www.displayr.com/alternatives-word-cloud/.
    """
    dictionary = xAAD.dictionary
    k,v = dictionary.keys(),dictionary.values()
    df = pd.DataFrame.from_dict({'token':k,'weight':v}) #Dataframe to sort the data
    if mode == 'p':
        df = df.loc[df['weight'] > 0]
    else:
        df = df.loc[df['weight'] < 0]
    df_sorted = df.sort_values(by='weight',ascending=False).drop_duplicates(subset=['token']) #Sorted dataframe
    tokens = df_sorted['token'].to_list()
    weights = df_sorted['weight'].to_list() 
    if limit != 0: 
        if len(tokens) >= limit:
            tokens = tokens[:limit]
            weights = weights[:limit]
    cmap = cm.get_cmap('copper',100) #Color map for the treemap
    if mode != 'p':
        cmap = cm.get_cmap('cividis',100)
    mini = min(weights)
    maxi = max(weights)
    norm = mpl.colors.Normalize(vmin=mini,vmax=maxi)
    colors = [cmap(norm(value)) for value in weights] #Color mapping normalization
    fig = figure(figsize=(10,10)) #Figure size
    ax = fig.add_subplot(111,aspect="equal")
    ax = squarify.plot(weights,label=tokens,text_kwargs={'color':'#ffffff' ,'size': 8},color=colors,bar_kwargs=dict(linewidth=1, edgecolor="#222222"))
    plt.axis('off')
    ax.set_title(title)
    AIChart_save_file(title,saveImg=saveImg,savePDF=savePDF,saveEPS=saveEPS)
    if show:
        plt.show()
    



def AIChart_plot_data_word_graph(xAAD,text_list,show=True,title="Word Graph",saveImg = False,savePDF = False,saveEPS= False):
    """
        This is a implementation of a word graph used in text categorization from [2].

        [2] F. Rousseau, E. Kiagias, and M. Vazirgiannis, “Text Categorization as a Graph Classification Problem,” in Proceedings of the 53rd Annual Meeting of the Association for Computational Linguistics and the 7th International Joint Conference on Natural LanguageProcessing (Volume 1: Long Papers), Beijing, China, 2015, pp. 1702–1712. doi: 10.3115/v1/P15-1164.
    """
    dictionary = xAAD.dictionary
    fig = plt.figure()
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
        if v['weight'] <= 0:
            node_size.append(0)
        else:
            node_size.append(10+500*v['weight']) #Linear function to adjust node size
        for edge in v['edges']:
            G.add_edge(k,edge)
    pos = nx.spring_layout(G, k=0.2, iterations=30)
    ax = fig.add_subplot(111,aspect="equal")
    nx.draw(G,pos,with_labels=True,node_size=node_size,font_color="black",font_size=10,edge_color='#999999',width=1,node_color="#ff5757") #graph drawing function
    ax.set_title(title)
    AIChart_save_file(title,saveImg=saveImg,savePDF=savePDF,saveEPS=saveEPS)
    if show:
        plt.show()


def AIChart_plot_data_Influence_Map(xAAD,text_list,title="Influence Map",show=True,saveImg = False,savePDF = False,saveEPS= False,color=False):
    """
        THis is a implementation of a Influence Map shown in [1] for text categorization.

        [1] M. Loor and G. De Tré, “Contextualizing Naive Bayes Predictions,” in Information Processing and Management of Uncertainty in Knowledge-Based Systems, Cham, 2020, pp. 814–827. [Online]. Available: https://link.springer.com/chapter/10.1007/978-3-030-50153-2_60
    """
    dictionary = xAAD.dictionary
    fig = figure(figsize=(16,9))
    ax = fig.add_subplot(111,aspect=9/16)
    contador = 0
    while len(text_list) > contador*contador:
        contador = contador + 1
    next_line = 0
    next_word = 0
    for i in range(len(text_list)): #Calculates word spacing depending on fontsize
        if next_word % contador == 0 or next_word > contador:
            next_line = next_line + 1
            next_word = 0
        word = text_list[i]
        font_size = 15
        if word not in dictionary.keys():
            plt.text(next_word,contador - next_line,word,fontsize=15,color='black',wrap=True)
        elif dictionary[word] == 0:
            plt.text(next_word,contador - next_line,word,fontsize=15,color='black',wrap=True)
        else:
            font_size = (dictionary[word]  ) * 30
            if font_size < 8:
                font_size = 9
            if dictionary[word] < 0:
                font_size = -dictionary[word] * 30
                if font_size < 8:
                    font_size = 9
                if color:
                    plt.text(next_word,contador - next_line,word,fontsize=font_size,color='blue',wrap=True)
                else:
                    plt.text(next_word,contador - next_line,r'\underline{%s}'%(word),fontsize=font_size,color='black',wrap=True)
            else:
                if color:
                    plt.text(next_word,contador - next_line,word,fontsize=font_size,color='red',wrap=True)
                else:
                    plt.text(next_word,contador - next_line,r'\emph{%s}'%(word),fontsize=font_size,color='black',wrap=True)


            
        next_word = next_word + len(word)*0.13*font_size/30 + 0.15
        #plt.text(j,contador - i - 1,text_list[indice],fontsize=font_size,wrap=True)
    ax.set_title(title)
    plt.axis([0.5,contador,0.5,contador])
    plt.axis('off')
    AIChart_save_file(title,saveImg=saveImg,savePDF=savePDF,saveEPS=saveEPS)
    if show:
        plt.show()
