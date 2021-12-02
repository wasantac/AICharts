import math
import xNB_Classes

def learning_process(A,Xo):
    members_A = 0
    non_members_A = 0
    for x in Xo:
        if x in A:
            members_A += 1
            for f in x:
                f.a = f.a + x.count(f)#por el momento
        else:
            non_members_A += 1
            for f in x:
                f.na = f.na + x.count(f)#por el momento
    total = members_A + non_members_A
    prob_A = math.log((members_A + 1)/(total+1))
    prob_not_A = math.log((non_members_A + 1)/(total + 1))

    #for f in Fxo
    #p(f|a)
    #p(f|not_a)

    w = 0
    b = prob_A - prob_not_A

    #for f un Fxo
    # w = w + (P(f|a) - P(f|not_a)* f_sub
    ua = w / 1 #w / ||w||
    
    ta = -b / 1 #-b / ||w||
    knowledge_model = (ua,)
    return knowledge_model

def evaluation_process(x,knowledge_model):
    Pro_membership = {}
    Pro_nonmembership = {}
    pro_membership_score = 0
    pro_nonmembership_score = 0

    if knowledge_model.ta < 0:
        pro_membership_score = pro_membership_score + math.fabs(knowledge_model.ta)
    else:
        prop_nonmembership_score = pro_nonmembership_score + knowledge_model.ta
    
    for f in x:
        sf = x.count(f) * f.w
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


