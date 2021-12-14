import math
import xNB_Classes
import numpy as np
import nltk
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import re
import AICharts_Report


stop_words = set(stopwords.words('english'))
stop_words.add('the')
stop_words.add('they')

def transform(data,tokenize=True,withNumbers=False):
    porter_stemmer = PorterStemmer()
    body = str(data).replace('\n',' ')
    if withNumbers:
        body = re.sub(' +', ' ', body)
        body = re.sub("[^a-zA-Z\d\,\.]+"," ",body)
        body = re.sub("[^a-zA-Z\d\,\s]+","",body)
    else:
        body = re.sub(' +', ' ', body)
        body = re.sub("[^a-zA-Z\.]+"," ",body)
        body = re.sub("[^a-zA-Z\s]+","",body)
    if tokenize:
        nltk_tokens = nltk.word_tokenize(body)
        nltk_tokens.pop()
        for i in range(len(nltk_tokens)):
            nltk_tokens[i] = porter_stemmer.stem(nltk_tokens[i])
            body = ' '.join(nltk_tokens)
    return body


def set_weights(data,ev):
    body = transform(data,tokenize=False,withNumbers=True)
    list_words = body.split(" ")
    dictionary = {}
    porter_stemmer = PorterStemmer()
    for i in list_words:
        token = porter_stemmer.stem(i)
        if token in ev.mu_hat[1].keys():
            dictionary.update({i: ev.mu_hat[1][token]*400}) 
        elif token in ev.nu_hat[1].keys():
            dictionary.update({i: -ev.nu_hat[1][token]*400}) 
        else:
            dictionary.update({i:0.0}) 
    return (body,xNB_Classes.xAAD(ev.hesitation(),dictionary))


def pre_processing_cat(filename):
    with open(filename) as file:
        lines = file.readlines()
        dictionary = {}
        for i in lines:
            line = i.split(' ')
            number = line[1].replace('\n','')
            if line[0] not in dictionary.keys():
                
                dictionary.update({line[0]:[number]})
            else:
                dictionary[line[0]].append(number)
    return dictionary


def pre_procesing_train(filename):
    with open(filename) as file:
        dictionary = {}
        content = file.readlines()
        for i in range(4,len(content) - 1 + 4,4): #desde 0 = .I numero , 1= .W , 2= parrafo  for i in range(0,100,4)
            number = content[i-4].split(" ")[-1].strip('\n')
            paragraph = content[i-2].strip('\n')
            dictionary.update({number:paragraph})
        return dictionary

        
def count_data(f,x):
    total = 0
    for word in x:
        if f == word:
            total += 1
    return total


def remove_stop_words(data):
    list_words = data.split(' ')
    list_words = list(filter(None,list_words))
    filtered_words = []
    for w in list_words:
        if w not in stop_words:
            filtered_words.append(w)
    filtered_words = [w for w in filtered_words  if len(w) > 2]
    list_words = filtered_words
    return list_words


def learning_process(A,Xo,categories):
    members_A = 0
    non_members_A = 0
    Fxo = set() #Feature Set
    F_is_a = {} #F is member of category A
    F_not_a = {} # F is not member of category A
    for keys,values in Xo.items(): #Count Words and Memebers
        list_words = remove_stop_words(values)
        if keys in categories[A]:
            members_A += 1
            for f in set(list_words):
                if f not in F_is_a.keys():
                    F_is_a.update({f:{'count':count_data(f,list_words),'prob':0}}) 
                else:
                    F_is_a.update({f:{'count':F_is_a[f]['count']  + count_data(f,list_words),'prob':0}}) 
                Fxo.add(f)
        else:
            non_members_A += 1
            for f in set(list_words):
                if f not in F_not_a.keys():
                    F_not_a.update({f:{'count':count_data(f,list_words),'prob':0}}) 
                else:
                    F_not_a.update({f:{'count':F_not_a[f]['count']  + count_data(f,list_words),'prob':0}}) 
                Fxo.add(f)

    total = members_A + non_members_A 
    prob_A = math.log((members_A + 1)/(total+1),10) #Probability of A
    prob_not_A = math.log((non_members_A + 1)/(total + 1),10) #Probability of not A
    for f in Fxo: #Conditional Probabilites
        if f in F_is_a.keys() and f in F_not_a.keys():
            calc_a = (F_is_a[f]['count'] + 1)/(F_is_a[f]['count'] + F_not_a[f]['count'] + len(Fxo)) 
            calc_not_a = (F_not_a[f]['count'] + 1)/(F_is_a[f]['count'] + F_not_a[f]['count'] + len(Fxo)) 

            prob_f_a = math.log(calc_a,10) 
            prob_f_not_a = math.log(calc_not_a,10) 

            F_is_a[f]['prob'] = prob_f_a
            F_not_a[f]['prob'] =  prob_f_not_a
        elif f in F_is_a.keys() and f not in F_not_a.keys():
            calc_a = (F_is_a[f]['count'] + 1)/(F_is_a[f]['count'] + 0 + len(Fxo))
            prob_f_a = math.log(calc_a,10) 
            F_is_a[f]['prob'] = prob_f_a

        elif f not in F_is_a.keys() and f in F_not_a.keys():
            calc_not_a = (F_not_a[f]['count'] + 1)/( 0+ F_not_a[f]['count'] + len(Fxo))
            prob_f_not_a = math.log(calc_not_a ,10) 
            F_not_a[f]['prob'] =  prob_f_not_a
    b = prob_A - prob_not_A
    w_dicc ={} # w <- 0
    for f in Fxo: 
        if f in F_is_a.keys() and f in F_not_a.keys():
            calc = (F_is_a[f]['prob'] - F_not_a[f]['prob'])
            w_dicc.update({f:calc})
        elif f in F_is_a.keys() and f not in F_not_a.keys():
            calc = (F_is_a[f]['prob'])
            w_dicc.update({f:calc})
        elif f not in F_is_a.keys() and f in F_not_a.keys():
            calc = (0 - F_not_a[f]['prob'])
            w_dicc.update({f:calc})
        else:
             w_dicc.update({f:0.0})
    magnitude = np.linalg.norm(np.array(list(w_dicc.values())))# ||w||
    for k,v in w_dicc.items():      #w / ||w||
        w_dicc.update({k:v/magnitude}) 
    ta = -b / magnitude #-b / ||w|| threshold
    knowledge_model = (w_dicc,ta)
    return knowledge_model


def evaluation_process(x,knowledge_model):
    Pro_membership = {}
    Pro_nonmembership = {}
    pro_membership_score = 0
    pro_nonmembership_score = 0
    if knowledge_model[1] < 0:
        pro_membership_score = pro_membership_score + math.fabs(knowledge_model[1])
    else:
        pro_nonmembership_score = pro_nonmembership_score + knowledge_model[1]
    list_words = remove_stop_words(x)
    for f in set(list_words):
        sf = count_data(f,list_words) * knowledge_model[0][f]
        if sf > 0:
            pro_membership_score = pro_membership_score + sf
            Pro_membership.update({f:sf})
        else:
            pro_nonmembership_score = pro_nonmembership_score + math.fabs(sf)
            Pro_nonmembership.update({f:math.fabs(sf)})
    maxLevel = max([1,pro_membership_score + pro_nonmembership_score])
    for k,v in Pro_membership.items():
        Pro_membership.update({k:v/maxLevel})
    for k,v in Pro_nonmembership.items():
        Pro_nonmembership.update({k:v/maxLevel})
    pro_membership_score_max_level = pro_membership_score / maxLevel
    pro_nonmembership_score_max_level = pro_nonmembership_score / maxLevel
    return xNB_Classes.xAIFSElement(x,(pro_membership_score_max_level,Pro_membership),(pro_nonmembership_score_max_level,Pro_nonmembership))


know = learning_process('grain',pre_procesing_train('./processed/reuters-training.dat'),pre_processing_cat('./processed/reuters-cat-doc.qrels'))
test1 = '''Food Department officials said the U.S.
Department of Agriculture approved the Continental Grain Co
sale of 52,500 tonnes of soft wheat at 89 U.S. Dlrs a tonne C
and F from Pacific Northwest to Colombo.
    They said the shipment was for April 8 to 20 delivery.
 REUTER'''
tokenized = transform(test1)
ev = evaluation_process(tokenized,know)
final_data = set_weights(test1,ev)
AICharts_Report.AIChart_plot_data_Influence_Map(final_data[1],final_data[0].split(' '),color=False,title="Grain",saveImg=True)