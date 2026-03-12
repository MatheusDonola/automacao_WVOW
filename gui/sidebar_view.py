import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(
    self,
    master,
    tema_callback,
    dashboard_callback,
    config_callback,
    logs_callback,
    stats_callback
    ):
        super().__init__(master, width=260, corner_radius=0)

        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(8, weight=1)

        self.lbl_titulo = ctk.CTkLabel(
            self,
            text="Automação WVOW",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.lbl_titulo.grid(row=0, column=0, padx=20, pady=(25, 8), sticky="w")

        self.lbl_subtitulo = ctk.CTkLabel(
            self,
            text="Painel inicial",
            font=ctk.CTkFont(size=13)
        )
        self.lbl_subtitulo.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        self.btn_dashboard = ctk.CTkButton(
            self,
            text="Dashboard",
            command=dashboard_callback
        )

        self.btn_config = ctk.CTkButton(
        self,
        text="Configurações",
        command=config_callback
        )

        self.btn_logs = ctk.CTkButton(
        self,
        text="Logs",
        command=logs_callback
        )
        self.btn_logs.grid(row=4, column=0, padx=20, pady=8, sticky="ew")

        self.btn_stats = ctk.CTkButton(
        self,
        text="Estatísticas",
        command=stats_callback
        )
        self.btn_stats.grid(row=5, column=0, padx=20, pady=8, sticky="ew")

        self.menu_tema = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"],
            command=tema_callback
        )
        self.menu_tema.set("Dark")
        self.menu_tema.grid(row=9, column=0, padx=20, pady=(10, 25), sticky="ew")