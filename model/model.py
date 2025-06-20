import copy
import heapq

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

        self._dizioOrdinato = dict(sorted(listaVicini.items(), key=lambda item: item[1]))
        return listaVicini


    # def simula(self, k, nodo):
    #     source = None
    #     for n in self.nodi:
    #         if str(n) == nodo:
    #             source = nodo
    #
    #     self._best_path = []
    #     self._best_peso = 0
    #
    #
    #     primiK = []
    #     visited = {source}
    #     for v in self._dizioOrdinato.keys():
    #         if len(primiK)<k:
    #             primiK.append(v)
    #             visited.add(self._idMap[v])
    #
    #     for v in primiK:
    #         self.ricorsione( [source, self._idMap[v]], 0, visited)
    #
    #     return len(self._best_path), self._best_peso
    #
    # def ricorsione(self, cammino_parziale, peso_parziale, visited):
    #     ultimo = cammino_parziale[-1]
    #
    #     # Caso finale: aggiorna se questo cammino è migliore
    #     if peso_parziale > self._best_peso:
    #         best_peso = peso_parziale
    #         best_cammino = list(cammino_parziale)
    #
    #
    #     for vicino in self.grafo.neighbors(ultimo):
    #         if vicino not in visited:
    #             peso = self.grafo[ultimo][vicino]['weight']
    #
    #             visited.add(vicino)
    #             cammino_parziale.append(vicino)
    #
    #             self.ricorsione(cammino_parziale, peso_parziale + peso, visited)
    #
    #             # Backtrack
    #             visited.remove(vicino)
    #             cammino_parziale.pop()

    import heapq


    def simula( self, inizio: int, K: int):
        tempo_totale = 0
        preparati = set()
        in_preparazione = set()
        coda_eventi = []  # heap di tuple: (tempo fine, id stazione, cibo corrente)
        source = None
        for n in self.nodi:
            if str(n) == inizio:
                source = n
        # Step iniziale: avviare fino a K stazioni
        adiacenti = list(self.grafo.neighbors(source))
        ad_ordinati = sorted(adiacenti, key=lambda x: self.grafo[source][x]['weight'], reverse=True)
        iniziali = ad_ordinati[:K]  # massimo K cibi iniziali

        for idx, cibo in enumerate(iniziali):
            durata = self.grafo[source][cibo]['weight']
            heapq.heappush(coda_eventi, (durata, idx, cibo))
            in_preparazione.add(cibo)

        while coda_eventi:
            tempo_fine, stazione, cibo_corrente = heapq.heappop(coda_eventi)
            tempo_totale = max(tempo_totale, tempo_fine)
            preparati.add(cibo_corrente)
            in_preparazione.remove(cibo_corrente)

            # Trova prossimo cibo da preparare per questa stazione
            prossimi = list(self.grafo.neighbors(cibo_corrente))
            candidati = [(self.grafo[cibo_corrente][succ]['weight'], succ)
                         for succ in prossimi
                         if succ not in preparati and succ not in in_preparazione]

            if candidati:
                candidati.sort(key=lambda x:x[0],reverse=True)  # massima calorie congiunte
                peso, prossimo = candidati[0]
                in_preparazione.add(prossimo)
                heapq.heappush(coda_eventi, (tempo_fine + peso, stazione, prossimo))

        return len(preparati), tempo_totale



