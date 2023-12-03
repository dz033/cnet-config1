import pandas as pd
import numpy as np
from path import RoutingPath, FeatureValue
from featurescore import feature_score
from argmax import argmax

"""
stuff to implement:

feature functions 
1) shortest path
    returns 1 (boolean) if P is the shortest path, else 0
2) Egress
    returns egress of P
3) Ingress
    returns ingress of P
4) Organizational feature function 
    returns org owning ip prefix

    
Feature score function

Compass algorithm 
line 5: greedily select a feature using max(score function)
line 6/7 excluding already found/used feature values and types
line 10-13: while loop to find max specs of the feature selected

do you need this equivalent path finder? seems like you would rarely find an equivalent path in the real world    
""" 



def compass(R, Q, V, k, t, feature_score, argmax): 
    #R is a set of routing paths
    #q1...ql is a set of feature functions
    #k is the limit on the number of specifications
    #t is the limit on the size of the specifications
    #V is the set of all feature values
    
    S = set() #specification set S
    L = set() #last computed specification L
    while len(S) < k:
        q, v = argmax(feature_score())  #if weight is traffic size, wehre do we get this data
        L.add(v)
        Q.remove(q)
        for value in V:
            if value[0] == q:
                V.remove(q)
        for path in R:
            if not path_meets_specification(path, v):
                R.remove(path)
        if len(L) == t:
            S = S.add(L)
            break
        #if there is an equivalent path to L with an additional feature value, add it instead because it will be more explanatory with the same coverage
        #while True: #there exists v belonging to Uq, for which LU{v} == L... (path equivalent): 
        for value in V:
            if check_path_equivalence(L, L.add(value), R):
                L = L.add(value)
                if len(L) == t:
                    S = S.add(L)
                    break
                Q.remove(value[0])
        

        for path in L:
            L.add(v)
            if len(L) == t:
                S.add(L)
                break
            Q.remove(q) #q is the feature value that v belongs to 
        S.add(L)

    return S

def check_path_equivalence(L, S, R): #path equivalence is a property of path specifications
    for path in R:
        if path_meets_specification(path, L) and not path_meets_specification(path, S):
            return False
        elif not path_meets_specification(path, L) and path_meets_specification(path, S):
            return False
    return True

def path_meets_specification(p, S):
    #for all feature values in S, the corresponding feature value in p is the same. 

    
    for feature_value in S:
        if feature_value.getType() == 'I':
            if not p.checkIngress(): #return false if ingress doesnt match
                return False
        elif feature_value.getType() == 'E':
            if not p.checkEgress(): 
                return False
        elif feature_value.getType() == 'O':
            if not p.checkOrganization(): 
                return False
        elif feature_value.getType() == 'SP': #use elif here because we may add more feature values
            if not p.checkShortestPath(): 
                return False
    return True

def path_meets_specification_set(p, SS):
    for specification in SS.specifications:     # call path meets specification for each specification in the set
        path_meets_specification(p, specification)
    return True

def main():
    flows = pd.read_csv("flow-10-egress_10000.csv")
    #print(f"flows: {flows}")
    nested_list = flows.values.tolist() #path, org, ip, 
    #print(nested_list) 




    #print(flowList)
    def generate_paths():
        l = []
        for node in nested_list:
            destination = node[1]
            ingress = node[0][0]
            egress = node[0][-1]
            path = node[0]
            sp = False
            bandwidth = node[3]
            if node[4] == 'TRUE':
                sp = True
            
            P = RoutingPath(destination, ingress, egress, path, sp, bandwidth)
            #print(str(P))
            l.append(P)
        return l

    pathList = generate_paths()
    


    #CREATING A LIST OF ALL FEATURE VALUES:
    #WE ARE GENERATING THIS OURSELVES, BUT IN A REAL SCENARIO THESE VALUES SHOULD BE FIXED BASED ON THE NETWORK
    ingressList = []
    egressList = []
    organizationList = []
    spList = [True, False]
    for path in pathList:
        if path.getIngress() not in ingressList:
            ingressList.append(path.getIngress())
        if path.getEgress() not in egressList:
            egressList.append(path.getEgress())
        if path.getOrganization() not in ingressList:
            organizationList.append(path.getOrganization())
    
    featureValueDict = {
        "ingress": ingressList,
        "egress": egressList,
        "organization": organizationList,
        "shortest_path": spList
    }

    S = compass(pathList, #R
            featureValueDict.keys(), #Q
            featureValueDict.items(), #V (not in the original paper, but added for path equivalence logic)
            4,  #k
            len(featureValueDict.keys()), #t
            feature_score, 
            argmax)
    print(S)

main()