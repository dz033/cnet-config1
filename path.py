"""
d = network prefix (organization owning traffic)
P = path

"""
class NetworkPath:
    def __init__(self, ingress, egress, path):
        self.ingress = ingress
        self.egress = egress
        self.path = path
        self.P = [ingress, egress, path] #this is the most important attribute and the one we will be passing into RoutingPath

class Destination:
    def __init__(self, ip, organization):
        self.ip = ip
        self.organization = organization

class RoutingPath:

    def __init__(self, d, P): # d is class Destination P is class NetworkPath
        self.d = d
        self.P = P

class PathSpecification:
    def __init__(self, paths): #input paths as a list
        self.paths = paths

class SpecificationSet:
    def __init__(self, specifications, k): #input specifications as a list
        self.max_size = k
        self.specifications = specifications