import customtkinter as ctk
import threading

from main import main_loop, request_stop


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Automação WVOW")
        self.geometry("980x620")
        self.minsize(900, 560)

        self.bot_thread = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.criar_sidebar()
        self.criar_area_principal()

    def criar_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.sidebar.grid_columnconfigure(0, weight=1)
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self.sidebar,
            text="Automação WVOW",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=(25, 8), sticky="w")

        self.lbl_subtitulo = ctk.CTkLabel(
            self.sidebar,
            text="Painel inicial",
            font=ctk.CTkFont(size=13)
        )
        self.lbl_subtitulo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.btn_dashboard = ctk.CTkButton(self.sidebar, text="Dashboard")
        self.btn_dashboard.grid(row=2, column=0, padx=20, pady=8, sticky="ew")

        self.btn_config = ctk.CTkButton(self.sidebar, text="Configurações")
        self.btn_config.grid(row=3, column=0, padx=20, pady=8, sticky="ew")

        self.btn_logs = ctk.CTkButton(self.sidebar, text="Logs")
        self.btn_logs.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        self.btn_stats = ctk.CTkButton(self.sidebar, text="Estatísticas")
        self.btn_stats.grid(row=5, column=0, padx=20, pady=8, sticky="ew")

        self.menu_tema = ctk.CTkOptionMenu(
            self.sidebar,
            values=["Dark", "Light", "System"],
            command=self.alterar_tema
        )
        self.menu_tema.set("Dark")
        self.menu_tema.grid(row=9, column=0, padx=20, pady=(10, 25), sticky="ew")

    def criar_area_principal(self):
        self.main = ctk.CTkFrame(self, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew", padx=18, pady=18)

        self.main.grid_columnconfigure((0, 1), weight=1)
        self.main.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self.main)
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 12))
        self.header.grid_columnconfigure(0, weight=1)

        self.lbl_header = ctk.CTkLabel(
            self.header,
            text="Controle da automação",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.lbl_header.grid(row=0, column=0, padx=18, pady=(16, 4), sticky="w")

        self.lbl_desc = ctk.CTkLabel(
            self.header,
            text="Primeira versão da interface para iniciar, parar e acompanhar o status do bot.",
            font=ctk.CTkFont(size=13)
        )
        self.lbl_desc.grid(row=1, column=0, padx=18, pady=(0, 16), sticky="w")

        self.card_controle = ctk.CTkFrame(self.main)
        self.card_controle.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.card_controle.grid_columnconfigure(0, weight=1)

        self.lbl_controle = ctk.CTkLabel(
            self.card_controle,
            text="Controles",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_controle.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        self.status_var = ctk.StringVar(value="Status: parado")
        self.lbl_status = ctk.CTkLabel(
            self.card_controle,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=15)
        )
        self.lbl_status.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="w")

        self.btn_start = ctk.CTkButton(
            self.card_controle,
            text="Iniciar bot",
            height=40,
            command=self.iniciar_bot
        )
        self.btn_start.grid(row=2, column=0, padx=18, pady=(0, 10), sticky="ew")

        self.btn_stop = ctk.CTkButton(
            self.card_controle,
            text="Parar bot",
            height=40,
            command=self.parar_bot
        )
        self.btn_stop.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="ew")

        self.card_info = ctk.CTkFrame(self.main)
        self.card_info.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        self.card_info.grid_columnconfigure(0, weight=1)

        self.lbl_info = ctk.CTkLabel(
            self.card_info,
            text="Resumo",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_info.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        self.txt_info = ctk.CTkTextbox(self.card_info, height=260)
        self.txt_info.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")
        self.txt_info.insert("1.0", "Interface inicial criada com sucesso.\n\nPróximos passos naturais:\n- ligar status em tempo real\n- mostrar logs na tela\n- criar área de configurações\n- adicionar estatísticas")
        self.txt_info.configure(state="disabled")

    def iniciar_bot(self):
        if self.bot_thread and self.bot_thread.is_alive():
            self.status_var.set("Status: rodando")
            return

        self.bot_thread = threading.Thread(target=main_loop, daemon=True)
        self.bot_thread.start()
        self.status_var.set("Status: rodando")

    def parar_bot(self):
        request_stop()
        self.status_var.set("Status: parando...")

    def alterar_tema(self, novo_tema):
        ctk.set_appearance_mode(novo_tema.lower())


if __name__ == "__main__":
    app = App()
    app.mainloop()