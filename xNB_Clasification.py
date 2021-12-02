import math
import xNB_Classes
import numpy as np
def count_data(f,x):
    total = 0
    for data in x:
        if data ==f:
            total +=1
    return total

def learning_process(A,Xo):
    members_A = 0
    non_members_A = 0
    Fxo = set()
    F_is_a = {}
    F_not_a = {}
    for x in Xo:
        if x in A:
            members_A += 1
            for f in x:
                if f not in F_is_a.keys():
                    F_is_a.update({f:count_data(f,x)}) 
                else:
                    F_is_a.update({f:count_data(f,x) + F_is_a[f]}) 
                Fxo.add(f)
        else:
            non_members_A += 1
            for f in x:
                if f not in F_not_a.keys():
                    F_not_a.update({f:count_data(f,x)}) 
                else:
                    F_not_a.update({f:count_data(f,x) + F_not_a[f]}) 
                Fxo.add(f)
    total = members_A + non_members_A
    prob_A = math.log((members_A + 1)/(total+1))
    prob_not_A = math.log((non_members_A + 1)/(total + 1))

    for f in Fxo:
        prob_f_a = math.log((F_is_a[f] + 1)/(F_is_a[f] + F_not_a[f] + len(Fxo)))
        prob_f_not_a = math.log((F_not_a[f] + 1)/(F_is_a[f] + F_not_a[f] + len(Fxo)))
        F_is_a.update({f:prob_f_a})
        F_not_a.update({f:prob_f_not_a})

    w = 0
    b = prob_A - prob_not_A

    w_list = []
    for f in Fxo:
        w_list.append((F_is_a[f] - F_not_a[f]) * f.feature)
        w = w + (F_is_a[f] - F_not_a[f]) * f.feature

    magnitude = np.linalg.norm(np.array(w_list)) # ||w||
    ua = w / magnitude #w / ||w||
    
    ta = -b / magnitude #-b / ||w||
    knowledge_model = (ua,ta)
    return knowledge_model

def evaluation_process(x,knowledge_model):
    Pro_membership = {}
    Pro_nonmembership = {}
    pro_membership_score = 0
    pro_nonmembership_score = 0

    if knowledge_model[1] < 0:
        pro_membership_score = pro_membership_score + math.fabs(knowledge_model[1])
    else:
        prop_nonmembership_score = pro_nonmembership_score + knowledge_model[1]
    
    for f in x:
        sf = count_data(f,x) * f.w
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


