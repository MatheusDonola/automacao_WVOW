from helpers.logger import log
from config import FIRELIZARD

class Statistics:

    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.energia_inicial = None
        self.energia_final = None

        self.rallies_sucesso = 0

        self.premium_card = 0
        self.advanced_chest = 0
        self.green_book = 0
        self.materials = 0

        self.game_crashes = 0


    def energia_gasta(self):
        if self.energia_inicial is None or self.energia_final is None:
            log(f"Pelo menos um dos valores de energia não foi encontrado, energia inicial:{self.energia_inicial}, final:{self.energia_final}")
            return None

        return self.energia_inicial - self.energia_final
    
    def add_game_crash(self):
        self.game_crashes += 1


    def rallies_feitos(self):
        energia = self.energia_gasta()

        if energia is None:
            return None

        custo = 150 if FIRELIZARD else 50
        self.rallies_sucesso = energia // custo

        return self.rallies_sucesso

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
        self.loot_taken()

        log(f"Starting energy: {self.energia_inicial}")
        log(f"Final energy: {self.energia_final}")
        log(f"Energy Spent: {self.energia_gasta()}")
        log(f"Successful Rallys: {self.rallies_sucesso}")
        log(f"Green books: {self.green_book}")
        log(f"Premium cards: {self.premium_card}")
        log(f"Advanced chests: {self.advanced_chest}")
        log(f"Materials: {self.materials}")
        log(f"Number of game crashes: {self.game_crashes}")

STATS = Statistics()
