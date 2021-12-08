import math
import xNB_Classes
import numpy as np
import AICharts_Report


def pre_processing_cat(filename='./data/reuter2-cat-doc.qrels'):
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

def pre_procesing_train(filename='./data/reuter2-training.dat'):
    with open(filename) as file:
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
    Fxo = set() #Feature Set
    F_is_a = {} #F is member of category A
    F_not_a = {} # F is not member of category A
    for keys,values in Xo.items(): #Count Words and Memebers
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
    w_dicc ={}
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


    magnitude = abs(np.linalg.norm(np.array(list(w_dicc.values()))) )# ||w||
    for k,v in w_dicc.items():      #w / ||w||
        w_dicc.update({k:v/magnitude}) 
    ta = -b / magnitude #-b / ||w|| threshold
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
        pro_nonmembership_score = pro_nonmembership_score + knowledge_model[1]
    
    list_words = x.split(' ')
    list_words = list(filter(None,list_words))
    for f in list_words:
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

know = learning_process('wheat',pre_procesing_train('./processed/reuters-training.dat'),pre_processing_cat('./processed/reuters-cat-doc.qrels'))

test = 'the london stock exchang s tradedopt market plan volum growth of at least pct a year and will more than doubl the rang of option avail by theend of option committe chairman geoffrey chamberlainsaid he told a news confer that more option contract weretrad in than in the previou seven year of the market sexist chamberlain said the daili averag volum of contractstrad in februari thi year almost tripl to from in the same month last year and further rapid growthwa expect we re aim for stock option class by the end of said chamberlain these would correspond to the eligibleconstitu of the ft se share index chamberlain ad that two new equiti option were to beintroduc thi month option will be avail in sear plc lt sehl l gt from march and in plessey co plc lt plyl l gt frommarch the london stock exchang is the largest outsid the unitedst for option trade forty f equiti option twocurr option two govern bond gilt option and anopt on the ftse index are avail at present chamberlain said the stock exchang aim to consolidateth london option market s lead posit in europ especi import with french and swiss equiti optionstrad plan to start thi year i d go so far as to say the plan for growth areconserv one lead option analyst said predictingcontinu volum growth of around pct a month for at leastth next year he said much of the recent growth in option had come frominter market mak trade aim at hedg book posit butnow the retail option market wa begin to take off the market trade from a corner of the now larg desertedfloor of the london stock exchang the floor ha been leftalmost empti in the wake of the recent regulatori chang inth equiti and gilt govern bond market which haveencourag a move to electron off floor trade yesterday the stock exchang decid to close the floor toequiti trade altogeth and said it expect to make afin decis on the floor s futur by the end of the floor space could be use for a purpose built optionsmarket but chamberlain said that it wa unlik that theoption market would need more than half of the availablespac'

ev = evaluation_process(test,know)
print(ev)

