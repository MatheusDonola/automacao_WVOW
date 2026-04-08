import threading
import time
import customtkinter as ctk

from main import main_loop, request_stop
from core.state import STATE
from gui.dashboard_view import Dashboard
from gui.sidebar_view import Sidebar


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automação WVOW")
        self.geometry("980x620")
        self.minsize(900, 560)

        self.bot_thread = None
        self.bot_rodando = False

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            dashboard_callback=self.mostrar_dashboard,
            config_callback=self.mostrar_config,
            logs_callback=self.mostrar_logs,
            stats_callback=self.mostrar_stats,
            tema_callback=self.alterar_tema
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        self.dashboard = Dashboard(
            self.main_area,
            iniciar_callback=self.iniciar_bot,
            parar_callback=self.parar_bot
        )
        self.dashboard.grid(row=0, column=0, sticky="nsew")

        self.dashboard.set_status("Status: parado")
        self.dashboard.set_resumo(
            "Bot parado.\n\n"
            "Teste de estabilidade da interface.\n"
            "O resumo automático foi desligado temporariamente."
        )

    def alterar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema.lower())

    def iniciar_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.dashboard.set_status("Status: rodando")
            return

        agora = time.time()
        STATE["start"] = agora
        STATE["evento_reset"] = agora

        self.bot_rodando = True
        self.dashboard.set_status("Status: rodando")

        self.bot_thread = threading.Thread(target=main_loop, daemon=True)
        self.bot_thread.start()

    def parar_bot(self):
        request_stop()
        self.dashboard.set_status("Status: parando...")

    def mostrar_dashboard(self):
        self.dashboard.grid(row=0, column=0, sticky="nsew")

    def mostrar_config(self):
        print("Tela de configurações ainda não implementada")

    def mostrar_logs(self):
        print("Tela de logs ainda não implementada")

    def mostrar_stats(self):
        print("Tela de estatísticas ainda não implementada")