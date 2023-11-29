"""
d = network prefix (organization owning traffic)
P = path

"""

import pandas as pd
import numpy as np

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
        #example: type is ingress(I). check feature value
    
    def getType(self):
        return self.type

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




#print(flowList)
def generatePaths():
    l = []
    for node in nested_list:
        destination = node[1]
        ingress = node[0][0]
        egress = node[0][-1]
        path = node[0]
        sp = False
        if node[4] == 'TRUE':
            sp = True
        
        P = str(RoutingPath(destination, ingress, egress, path, sp))
        print(P)
        l.append(P)
    return l

print(generatePaths())