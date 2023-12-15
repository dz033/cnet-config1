"""
d = network prefix (organization owning traffic)
P = path

"""

import pandas as pd
import numpy as np
#from featurescore import feature_score
"""nodes = pd.read_csv('nodes.csv')
tempNodesList = nodes.to_string().split("\n")
nodesList = []
for node in tempNodesList[1:]:  #start from 1 to ignore the header
    cleanNode = node.split()
    print(cleanNode)
    nodesList.append(cleanNode)

print(nodesList)"""



class Destination:
    def __init__(self, ip, organization):
        self.ip = ip
        self.organization = organization

class FeatureValue:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.tupleFormat = (type, value)
        #example: type is ingress(I). check feature value
    
    def getType(self):
        return self.type
    def getValue(self):
        return self.value
    
    def __str__(self):
        return str(self.tupleFormat)
class RoutingPath:
    def __init__(self, d, ingress, egress, path, shortestPath, bandwidth):
        self.d = d
        self.ingress = ingress
        self.egress = egress
        self.path = path
        self.shortestPath = shortestPath #this should be a boolean
        self.bandwidth = bandwidth
        self.listFormat = [self.d, self.ingress, self.egress, self.path, self.shortestPath, self.bandwidth]

    def getIngress(self):
        return self.ingress
    def getEgress(self):
        return self.ingress
    def getOrganization(self):
        return self.d
    def getSP(self):
        return self.shortestPath
    def getBandwidth(self):
        return self.bandwidth

    def __str__(self):
        return str(self.listFormat)
    
    def check(self, type, value):
        if type == "O":
            return self.checkDestination(value)
        elif type == "I":
            return self.checkIngress(value)
        elif type == "E":
            return self.checkEgress(value)
        elif type == "SP":
            return self.checkShortestPath(value)
    
    
    def checkDestination(self, value):
        return self.d == value
    def checkIngress(self, value):
        return self.ingress == value
    def checkEgress(self, value):
        return self.egress == value
    def checkPath(self, value):
        return self.path == value
    def checkShortestPath(self, value):
        return self.shortestPath == value
    
    
    
class PathSpecification:
    def __init__(self, paths): #input paths as a list
        self.paths = paths

class SpecificationSet:
    def __init__(self, specifications, k): #input specifications as a list
        self.max_size = k
        self.specifications = specifications

flows = pd.read_csv("flow-10-egress_10000.csv")
#print(f"flows: {flows}")
nested_list = flows.values.tolist() #path, org, ip, 
#print(nested_list) 
nodes = pd.read_csv("nodes.csv")
node_n_to_location = {}
for line in nodes.values.tolist():
    node_n_to_location[line[0]] = line[1]




#print(flowList)
def generatePaths():
    l = []
    for node in nested_list:
        destination = node[1]
        ingress = node_n_to_location[int(node[0].split(" -> ")[0])] ##HNMMMM IM SO CLOSE
        egress = node_n_to_location[int(node[0].split(" -> ")[-1])]
        path = node[0]
        sp = node[4]
        bandwidth = node[3]
        #if node[4] == 'TRUE':
        #    sp = True
        #print(f"sp is {node[4]}")
        P = RoutingPath(destination, ingress, egress, path, sp, bandwidth)
        #print(str(P))
        l.append(P)
    return l

def generateV(R):
    V = []
    ingressList = []
    egressList = []
    organizationList = []
    spList = [True, False]
    for P in R:
        if P.getIngress() not in ingressList:
            ingressList.append(P.getIngress())
        if P.getEgress() not in egressList:
            egressList.append(P.getEgress())
        if P.getOrganization() not in organizationList:
            organizationList.append(P.getOrganization())
    for value in ingressList:
        V.append(FeatureValue("I", value))
    for value in egressList:
        V.append(FeatureValue("E", value))
    for value in organizationList:
        V.append(FeatureValue("O", value))
    for value in spList:
        V.append(FeatureValue("SP", value))
    #print(organizationList)
    return V
    

def feature_score(R, v):
    
    score = 0
    q = v.getType()
    value = v.getValue()
    for P in R:
        if P.check(q, value):
            score += P.getBandwidth() #the weight of P

    return score

def argmax(R, V):
    max_score = 0
    max_v = None
    for v in V:
        v_score = feature_score(R, v)
        if v_score > max_score:
            max_score = v_score
            max_v = v
            #print(f"NEW KING: score {v_score} type {v.getType()} value {v.getValue()}")
    #print(F"FINAL KING: score {max_score} type {max_v.getType()} value {max_v.getValue()}")
    return max_v.getType(), max_v.getValue()



def main():
    R = generatePaths()[0:-1:25]
    #R = generatePaths()#[0:15000]
    V = generateV(R)
    #print(R)
    sampleValue = FeatureValue("SP", False)
    score = feature_score(R, sampleValue)
    #print(score)
    q, v = argmax(R, V)
    #print(f"q is {q} and v is {v}")
    #print(len(V))
    #print(len(R))
    
    
    #print(node_n_to_location)
#print(node_n_to_location)


#for node in nested_list:
#    pathList = node[0].split(" -> ")
main()
#v = FeatureValue("I", "SLKC")
#print(v)