from dataclasses import dataclass

@dataclass
class Cibo:
    food_code:int
    display_name:str


    def __hash__(self):
        return hash(self.food_code)

    def __str__(self):
        return f"{self.display_name}"