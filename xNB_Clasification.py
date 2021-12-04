import math
import xNB_Classes
import numpy as np
import re
import AICharts_Report
def pre_processing_cat():
    with open('./data/reuter2-cat-doc.qrels') as file:
        lines = file.readlines()
        dictionary = {}
        for i in lines:
            line = i.split(' ')
            if line[0] not in dictionary.keys():
                dictionary.update({line[0]:[line[1]]})
            else:
                dictionary[line[0]].append(line[1])
    return dictionary

def pre_procesing_train():
    with open('./data/reuter2-training.dat') as file:
        dictionary = {}
        content = file.readlines()
        for i in range(4,len(content) - 1 + 4,4): #desde 0 = .I numero , 1= .W , 2= parrafo  for i in range(0,100,4)
            number = content[i-4].split(" ")[-1].strip('\n')
            paragraph = content[i-2].strip('\n')
            dictionary.update({number:paragraph})
        return dictionary

        

def learning_process(A,Xo,categories):
    members_A = 0
    non_members_A = 0
    Fxo = set()
    F_is_a = {}
    F_not_a = {}
    for keys,values in Xo.items():
        list_words = values.split(' ')
        list_words = list(filter(None,list_words))
        if keys in categories[A]:
            members_A += 1
            for f in list_words:
                if f not in F_is_a.keys():
                    F_is_a.update({f:{'count':1,'prob':0}}) 
                else:
                    F_is_a[f]['count'] += 1
                Fxo.add(f)
        else:
            non_members_A += 1
            for f in list_words:
                if f not in F_not_a.keys():
                    F_not_a.update({f:{'count':1,'prob':0}}) 
                else:
                    F_not_a[f]['count'] += 1
                Fxo.add(f)
    total = members_A + non_members_A
    prob_A = math.log((members_A + 1)/(total+1))
    prob_not_A = math.log((non_members_A + 1)/(total + 1))
    for f in Fxo:
        if f in F_is_a.keys():
            try:
                prob_f_a = math.log((F_is_a[f]['count'] + 1)/(F_is_a[f]['count'] + F_not_a[f]['count'] + len(Fxo)))
                F_is_a[f]['prob'] = prob_f_a
            except KeyError:
                prob_f_a = math.log((F_is_a[f]['count'] + 1)/(F_is_a[f]['count'] + 0 + len(Fxo)))
                F_is_a[f]['prob'] = prob_f_a
        if f in F_not_a.keys():
            try:
                prob_f_not_a = math.log((F_not_a[f]['count'] + 1)/(F_is_a[f]['count'] + F_not_a[f]['count'] + len(Fxo)))
                F_not_a[f]['prob'] = prob_f_not_a 
            except KeyError:
                prob_f_not_a = math.log((F_not_a[f]['count'] + 1)/(0 + F_not_a[f]['count'] + len(Fxo)))
                F_not_a[f]['prob'] = prob_f_not_a 
    b = prob_A - prob_not_A
    w_dicc ={}
    for f in Fxo:
        if f in F_is_a.keys() and f in F_not_a.keys():
            w_dicc.update({f:(F_is_a[f]['prob'] - F_not_a[f]['prob'])*(F_is_a[f]['count'] + F_not_a[f]['count'])})
        elif f in F_is_a.keys() and f not in F_not_a.keys():
            w_dicc.update({f:F_is_a[f]['prob']*F_is_a[f]['count']})
        elif f not in F_is_a.keys() and f in F_not_a.keys():
            w_dicc.update({f:F_not_a[f]['prob']*F_not_a[f]['count']})
        else:
             w_dicc.update({f:0.0})




    magnitude = abs(np.linalg.norm(np.array(list(w_dicc.values()))) )# ||w||
    for k,v in w_dicc.items():      #w / ||w||
        w_dicc.update({k:v/magnitude})    
    ta = -b / magnitude #-b / ||w||
    knowledge_model = (w_dicc,ta)
    return knowledge_model



def count_data(f,x):
    total = 0
    for word in x:
        if f == word:
            total += 1
    return total

def evaluation_process(x,knowledge_model):
    Pro_membership = {}
    Pro_nonmembership = {}
    pro_membership_score = 0
    pro_nonmembership_score = 0

    if knowledge_model[1] < 0:
        pro_membership_score = pro_membership_score + math.fabs(knowledge_model[1])
    else:
        prop_nonmembership_score = pro_nonmembership_score + knowledge_model[1]
    
    list_words = x.split(' ')
    list_words = list(filter(None,list_words))
    for f in list_words:
        sf = count_data(f,list_words) * knowledge_model[0][f]
        if sf > 0:
            pro_membership_score = pro_membership_score + sf
            Pro_membership.update({f:sf})
        else:
            prop_nonmembership_score = prop_nonmembership_score + math.fabs(sf)
            Pro_nonmembership.update({f:math.fabs(sf)})

    maxLevel = max([1,pro_membership_score + prop_nonmembership_score])
    for k,v in Pro_membership.items():
        Pro_membership.update({k:v/maxLevel})
    for k,v in Pro_nonmembership.items():
        Pro_nonmembership.update({k:v/maxLevel})
    
    pro_membership_score_max_level = pro_membership_score / maxLevel
    pro_nonmembership_score_max_level = pro_nonmembership_score / maxLevel

    return xNB_Classes.xAIFSElement(x,(pro_membership_score_max_level,Pro_membership),(pro_nonmembership_score_max_level,Pro_nonmembership))

know = learning_process('earn',pre_procesing_train(),pre_processing_cat())

test = 'champion product board director approv twoforon stock split common share sharehold record april compani board vote recommend sharehold annual meet april increas author capit stock mln mln share'

ev = evaluation_process(test,know)

element  = xNB_Classes.xAAD(ev.mu_hat[0],ev.mu_hat[1])

AICharts_Report.AIChart_plot_data_treemap(element,limit=10)