import random


class BottleModel:

    def __init__(self, nom, drunkenness, bonus_damage=0, accuracy_penalty=0, risque_coma=0):
        self._nom = nom
        self._drunkenness = drunkenness
        self._accuracy_penalty = accuracy_penalty
        self._bonus_damage=bonus_damage
        self._risque_coma = risque_coma  


    def drink(self, player):

        try:
            if self.getType() != "PLAYER":
                raise TypeError
        except TypeError:
            print("Error.drink.BottleModel :Caracter is not PLAYER")
            

        print(f"{player.nom} boit {self.nom} ")

        
        player.drunkenness += self.drunkenness

        if player.drunkenness > 100:
            player.drunkenness= 100

        
        player.bonus_damage += self.bonus_damage
        player.accuracy_penalty += self.accuracy_penalty

    
        tirage = random.randint(1, 100)

        if tirage <= self.risque_coma:
            print("ALCOHOLIC COMA !")
            player.pv = 0

        
