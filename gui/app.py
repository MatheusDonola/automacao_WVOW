import threading
import customtkinter as ctk

from main import main_loop, request_stop
from gui.sidebar_view import Sidebar
from gui.dashboard_view import Dashboard
from gui.logs_view import LogsView
from gui.stats_view import StatsView
from gui.config_view import ConfigView


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")



class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automação WVOW")
        self.geometry("980x620")
        self.minsize(900, 560)

        self.current_view = None

        self.bot_thread = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
        self,
        tema_callback=self.alterar_tema,
        dashboard_callback=self.mostrar_dashboard,
        config_callback=self.mostrar_config,
        logs_callback=self.mostrar_logs,
        stats_callback=self.mostrar_stats
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_area = ctk.CTkFrame(self, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

        self.dashboard = Dashboard(
            self.main_area,
            iniciar_callback=self.iniciar_bot,
            parar_callback=self.parar_bot
        )
        self.dashboard.grid(row=0, column=0, sticky="nsew")

        self.checar_thread()

        self.mostrar_dashboard()

    def iniciar_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.dashboard.set_status("Status: rodando")
            return

        self.bot_thread = threading.Thread(target=main_loop, daemon=True)
        self.bot_thread.start()
        self.dashboard.set_status("Status: rodando")

    def parar_bot(self):
        request_stop()
        self.dashboard.set_status("Status: parando...")

    def alterar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema.lower())

    def checar_thread(self):
        if self.bot_thread and not self.bot_thread.is_alive():
            self.dashboard.set_status("Status: parado")

        self.after(1000, self.checar_thread)

    def trocar_view(self, nova_view):
        if self.current_view is not None:
            self.current_view.destroy()

        self.current_view = nova_view
        self.current_view.grid(row=0, column=0, sticky="nsew")

    def mostrar_dashboard(self):
        self.trocar_view(
            Dashboard(
                self.main_area,
                iniciar_callback=self.iniciar_bot,
                parar_callback=self.parar_bot
          )
        )

    def mostrar_logs(self):
        self.trocar_view(LogsView(self.main_area))

    def mostrar_stats(self):
        self.trocar_view(StatsView(self.main_area))

    def mostrar_config(self):
        self.trocar_view(ConfigView(self.main_area))