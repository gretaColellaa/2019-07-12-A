import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def handle_analisi(self, e):
        grafo = self._model.creaGrafo(int(self._view.txt_porzioni.value))
        self._view.txt_result.controls.append(ft.Text("Grafo correttamente creato."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumNodes()} nodi."))
        self._view.txt_result.controls.append(ft.Text(f"Il grafo contiene "
                                                      f"{self._model.getNumEdges()} archi."))
        cibi=grafo.nodes
        for cibo in cibi:
            self._view.ddCibo.options.append(ft.dropdown.Option(
                text=cibo))
        self._view.update_page()
    def handle_calorie(self, e):
       dizio=self._model.calorie(self._view.ddCibo.value)
       dizioOrdinato= dict(sorted(dizio.items(), key=lambda item: item[1]))
       print(dizio)
       self._view.txt_result.controls.append(ft.Text(f"I 5 vicini migliori di {self._view.ddCibo.value} sono:"))
       contatore=0
       dizio5={}
       for chiave in dizioOrdinato.keys():
           if contatore < 5:
               dizio5[chiave] = dizio[chiave]
               contatore += 1
       for chiave in dizio5.keys():
           self._view.txt_result.controls.append(ft.Text(f"{chiave} - {dizio[chiave]}"))
       self._view.update_page()

    def handle_simula(self, e):
        try: int(self._view.txt_k.value)
        except: self._view.create_alert("inserire un numero intero")

        numero_cibi, tempo = self._model.simula(self._view.ddCibo.value, int(self._view.txt_k.value))
        self._view.txt_result.controls.append(ft.Text(f"Con {int(self._view.txt_k.value)} stazioni si "
                                                      f"preparano {numero_cibi} cibi in {tempo} minuti,"
                                                      f"a partire da {self._view.ddCibo.value}"))
        self._view.update_page()