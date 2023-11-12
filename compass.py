
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

def Egress(p):
    return p.P[1] #simply returns egress from the NetworkPath of the RoutingPath

def Ingress(p):
    return p.P[0] #same logic as egress

def Organization(p):
    return p.d.organization

def Shortest_Path(p):
    if p.P[2].isShortestPath(): #figure out how to do this
        return 1
    return 0

def CreateFeatureList(p): #creates a list of feature values of p for easy comparison to path specifications
    l = [] 
    
    #ordered alphabetically
    l.append(Egress(p))
    l.append(Ingress(p))
    l.append(Organization(p))
    l.append(Shortest_Path(p))
    
    return l

def PathMeetsSpecification(p, S):
    #for all feature values in S, the corresponding feature value in p is the same. 
    l = CreateFeatureList(p)
    for feature_value in S.paths:
        if feature_value not in l:  #if p meets S,  then all feature values in S are in p. necessary and sufficient condition
            return False
    return True

def PathMeetsSpecificationSet(p, SS):
    for specification in SS.specifications:     # call path meets specification for each specification in the set
        PathMeetsSpecification(p, specification)
    return True