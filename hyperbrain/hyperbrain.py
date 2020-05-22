import os
import numpy as np
import copy
import pandas as pd

from graphbrain.notebook import *

class hyperGraph(object):
    def __init__(self):

        self.sents = {}
        

    def import_sent(self, edge, sentId, text = None):
        ''' Import an edge sentence'''
                
        self.sents[sentId] = hyperSent(edge, sentId, text = text)


class hyperSent(object):
    def __init__(self, edge, sentId = None, text = None):
        
        self.sentId = sentId
        self.edge = edge
        self.label = edge.label()
        self.text = text
        self.verb = self.edge[0].predicate().label()
        self.hedges = []
        
        self.dones = []
        self.split(edge)
        
    def verb_split(self, edge, id = id):
        '''Perform the verb_split'''
        
        output = []
        buffer = []
        
        
        if id in self.dones:
            return output
        
        self.dones.append(id)
        
        
        if not edge.is_atom():
            if (edge[0].type() == 'pm') | (edge[0].to_str() == ':/b/.'):
                
                for id in range(1,len(edge)):
                    
                    buffer.append(edge[id])
                    buffer.append(edge[id])

        if type(edge[0]) == str:
            for edge_verb in buffer:
                output.extend(self.edge_split(edge_verb))
                
            return output
        
                
        for arg in edge[0].argroles():
            for id,he in enumerate(edge.edges_with_argrole(arg)):
                
                out = hyperEdge()

                if not he.is_atom():
                    if (he[0].type() == 'pm') | (he[0].to_str() == ':/b/.'):
                        for he_id in range(1,len(he)):
                            buffer.append(he[he_id])
                            buffer.append(he[he_id])
                        continue
                    elif 'p' in he[0].type():
                        buffer.append(he)
                        continue
                
                
                out.verb = edge[0].predicate().label()
                out.arg = arg
                out.edge = he
                out.type = he.type()
                out.text = he.label()
                out.id = self.sentId
                
                output.append(out)
                
        for he in buffer:
            output.extend(self.verb_split(he))
            
        return output
    
    def split(self, edge):
        
        edges = [(id,edge) for (id,edge) in enumerate(edge.subedges())]
        
        edge_list = [(id,edge) for (id,edge) in edges if 'r' in edge.type()]

        for id,edge in edge_list:
            #print(edge)
            #print('---')
            self.hedges.extend(self.verb_split(edge = edge, id = id))

    def __repr__(self):
        if self.text is not None:
            return(self.text)
        else:
            return(self.label)

    def __getitem__(self, sentNumber):
          return self.hedges[sentNumber]
            
        
class hyperEdge(object):
    def __init__(self):
        
        self.id = None
        self.edge = None
        self.type = None
        self.arg = None
        self.verb = None
        self.text = None
        self.hypersent = None
        
        
    def __repr__(self):
        show(self.edge, roots_only = False, style='oneline')
        return(self.text)
        
        