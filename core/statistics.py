from helpers.logger import log
from config import FIRELIZARD

class Statistics:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.energia_inicial = None
        self.energia_final = None

        self.rallies_tentados = 0
        self.rallies_sucesso = 0
        self.rallies_falha = 0

        self.premium_card = 0
        self.advanced_chest = 0
        self.green_book = 0
        self.materials = 0


    def energia_gasta(self):
        if self.energia_inicial is None or self.energia_final is None:
            log(f"Pelo menos um dos valores de energia não foi encontrado, energia inicial:{self.energia_inicial}, final:{self.energia_final}")
            return None

        return self.energia_inicial - self.energia_final


    def rallies_feitos(self):
        energia = self.energia_gasta()

        if energia is None:
            return None

        custo = 150 if FIRELIZARD else 50
        self.rallies_sucesso = energia // custo

        return self.rallies_sucesso

    def rallies_perdidos(self):
        sucesso = self.rallies_feitos()

        if sucesso is None:
            return None

        self.rallies_falha = self.rallies_tentados - sucesso
        return self.rallies_falha

    def taxa_sucesso(self):
        if self.rallies_tentados == 0:
            return 0
        
        sucesso = self.rallies_feitos()
        if sucesso is None:
            return None
        
        return (sucesso / self.rallies_tentados) * 100

    def loot_taken(self):
        rallies = self.rallies_feitos()

        if rallies is None or rallies == 0:
            return None

        self.green_book = rallies * 25
        self.premium_card = rallies
        self.advanced_chest = rallies * 2
        self.materials = rallies * 120000

        return {
            "green_book": self.green_book,
            "premium_card": self.premium_card,
            "advanced_chest": self.advanced_chest,
            "materials": self.materials
        }
        
    def close_session(self):
        self.rallies_feitos()
        self.rallies_perdidos()
        self.loot_taken()


STATS = Statistics()

print("TEM close_session?", hasattr(STATS, "close_session"))
print("METODOS:", [x for x in dir(STATS) if "session" in x or "loot" in x or "rallies" in x])