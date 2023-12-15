from path import FeatureValue, argmax, generatePaths, generateV

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



def compass(R1, Q, V, k, t): 
    #R is a set of routing paths
    #q1...ql is a set of feature functions
    #k is the limit on the number of specifications
    #t is the limit on the size of the specifications
    #V is the set of all feature values
    R = R1
    S = [] #specification set S
    L = set() #last computed specification L
    #x = 0
    while len(S) < k:
        
        q, v = argmax(R, V)  #if weight is traffic size, wehre do we get this data
        #print(f"q is {q} and v is {v}")
        L.add(FeatureValue(q,v))
        #print(f"Q is {Q} and q is {q}")
        Q.remove(q)
        for value in reversed(V):
            if value.getType() == q:
                #print(value.getType())
                V.remove(value)
                #print("removed")
        for path in R:
            #print("checking paths in R")
            if not path.check(q, v):
             #   print("removed")
                R.remove(path)
        #print(f"  R after removals: {len(R)}")
        if len(L) == t:
            S.append(L)
            #L = set()
            #R = R1
            #print(len(L))
            break
        #print(f"L is {L}")
        #if there is an equivalent path to L with an additional feature value, add it instead because it will be more explanatory with the same coverage
        #while True: #there exists v belonging to Uq, for which LU{v} == L... (path equivalent): 
        
        for value in V:
            L2 = L
            L2.add(value)
            if check_path_equivalence(L, L2, R):
                print(f"{L} and {L2} extending {value} PE!!!!!!!!!")
                if len(L) == t:
                    S.append(L.copy())
                    break
                #Q.remove(value.getType())
                break

        #for path in L:
        #    L.add(v)
        #    if len(L) == t:
        #        S.add(L)
        #        break
            #print(Q)
            #print(q)
            #Q.remove(q) #q is the feature value that v belongs to 
        S.append(L.copy())
        #print(f"end of run {x}")
        #x +=1
        #print(f"S is {S}")
        #print(f"added {L}")
        
    #print(S)
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
    if S == None:
        return True
    for feature_value in S:
        if not p.check(feature_value.getType(), feature_value.getValue()):
            return False
    return True

def path_meets_specification_set(p, SS):
    for specification in SS.specifications:     # call path meets specification for each specification in the set
        path_meets_specification(p, specification)
    return True

def main():
    R = generatePaths()[0:-1:25]
    V = generateV(R)
    #print(V[0:50])
    Q = ["O", "I", "E", "SP"]
    k = 4
    t = len(Q)
    #print(f"R before removals: {len(R)}")
    S = compass(R, Q, V, k, t)
    SasString = []
    for PS in S:
        PSString = set()
        for featureValue in PS:
            PSString.add(str(featureValue))
        SasString.append(PSString)
    print(SasString)

main()