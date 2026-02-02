import random


class Bouteille:

    def __init__(self, nom, ivresse, bonus_degats=0, malus_precision=0, risque_coma=0):
        self.nom = nom
        self.ivresse = ivresse

        self.bonus_degats = bonus_degats
        self.malus_precision = malus_precision

        self.risque_coma = risque_coma  


    def boire(self, personnage):

        print(f"{personnage.nom} boit {self.nom} ")

        
        personnage.ivresse += self.ivresse

        if personnage.ivresse > 100:
            personnage.ivresse = 100

        
        personnage.bonus_degats += self.bonus_degats
        personnage.malus_precision += self.malus_precision

       
        tirage = random.randint(1, 100)

        if tirage <= self.risque_coma:
            print("COMA ÉTHYLIQUE !")
            personnage.pv = 0
