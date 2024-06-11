from dataclasses import dataclass

@dataclass
class Connessione:
    v1:str
    v2:str
    peso:int



    def __str__(self):
        return f"{self.v1} - {self.v2}"