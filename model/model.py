import copy

import networkx as nx

from database.DAO import DAO


class Model:
    def __init__(self):
        self.cibi=DAO.getCibi()
        self.grafo=nx.Graph()
        self._idMap = {}
        self.dict={}
        for v in self.cibi:
            self._idMap[v.food_code] = v
        self._solBest = []
        self._costBest = 0



    def creaGrafo(self,nporzioni):
        self.nodi = DAO.getNodi(nporzioni)
        self.grafo.add_nodes_from(self.nodi)
        self.addEdges()
        return self.grafo

    def addEdges(self):
         self.grafo.clear_edges()
         allEdges = DAO.getConnessioni()
         for connessione in allEdges:
             nodo1=self._idMap[connessione.v1]
             nodo2=self._idMap[connessione.v2]
             if nodo1 in self.grafo.nodes and nodo2 in self.grafo.nodes:
                 if self.grafo.has_edge(nodo1,nodo2)==False:
                     self.grafo.add_edge(nodo1,nodo2, weight=connessione.peso)
    def getNumNodes(self):
        return len(self.grafo.nodes)

    def getNumEdges(self):
        return len(self.grafo.edges)
    def calorie(self, nomeCibo):
        nodoIniziale=(0,0)
        listaVicini={}
        listaViciniOrder={}
        lista5Vicini={}
        for cibo in self.grafo.nodes:
            if cibo.display_name==nomeCibo:
                nodoIniziale=cibo
        for vicini in self.grafo.neighbors(nodoIniziale):
            listaVicini[vicini]=self.grafo[nodoIniziale][vicini]["weight"]
        return listaVicini