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
            "Clique em Iniciar bot para começar uma nova sessão."
        )

        self.after(500, self.atualizar_interface)

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

    def atualizar_interface(self):
        thread_viva = self.bot_thread and self.bot_thread.is_alive()

        if thread_viva:
            self.bot_rodando = True
            self.dashboard.set_resumo(self.montar_resumo())

        else:
            if self.bot_rodando:
                self.bot_rodando = False
                self.dashboard.set_status("Status: parado")
                self.dashboard.set_resumo(
                    "Bot parado.\n\n"
                    "Clique em Iniciar bot para começar uma nova sessão."
                )

        self.after(500, self.atualizar_interface)

    def montar_resumo(self):
        agora = time.time()
        inicio = STATE.get("start", agora)
        ultimo_reset = STATE.get("evento_reset", inicio)

        tempo_total = max(0, int(agora - inicio))
        tempo_reset = max(0, int(agora - ultimo_reset))

        return (
            "Monitor do bot\n\n"
            f"Tempo total da sessão: {self.formatar_tempo(tempo_total)}\n"
            f"Tempo desde o último reset: {self.formatar_tempo(tempo_reset)}\n\n"
            f"Sessão iniciada em: {time.strftime('%H:%M:%S', time.localtime(inicio))}\n"
            f"Último reset em: {time.strftime('%H:%M:%S', time.localtime(ultimo_reset))}"
        )

    @staticmethod
    def formatar_tempo(total_segundos):
        horas = total_segundos // 3600
        minutos = (total_segundos % 3600) // 60
        segundos = total_segundos % 60
        return f"{horas:02d}:{minutos:02d}:{segundos:02d}"
    
    def mostrar_dashboard(self):
        self.dashboard.grid(row=0, column=0, sticky="nsew")

    def mostrar_config(self):
        print("Tela de configurações ainda não implementada")

    def mostrar_logs(self):
        print("Tela de logs ainda não implementada")

    def mostrar_stats(self):
        print("Tela de estatísticas ainda não implementada")