import customtkinter as ctk


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, iniciar_callback, parar_callback):
        super().__init__(master, corner_radius=0)

        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.header = ctk.CTkFrame(self)
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

        # CARD CONTROLES
        self.card_controle = ctk.CTkFrame(self)
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
            command=iniciar_callback
        )
        self.btn_start.grid(row=2, column=0, padx=18, pady=(0, 10), sticky="ew")

        self.btn_stop = ctk.CTkButton(
            self.card_controle,
            text="Parar bot",
            height=40,
            command=parar_callback
        )
        self.btn_stop.grid(row=3, column=0, padx=18, pady=(0, 18), sticky="ew")

        # CARD RESUMO
        self.card_info = ctk.CTkFrame(self)
        self.card_info.grid(row=1, column=1, sticky="nsew", padx=(8, 0))
        self.card_info.grid_columnconfigure(0, weight=1)
        self.card_info.grid_rowconfigure(1, weight=1)

        self.lbl_info = ctk.CTkLabel(
            self.card_info,
            text="Resumo",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.lbl_info.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="w")

        self.txt_info = ctk.CTkTextbox(self.card_info, height=260)
        self.txt_info.grid(row=1, column=0, padx=18, pady=(0, 18), sticky="nsew")

        self._set_textbox_content(
            "Bot parado.\n\n"
            "Quando iniciar, este painel poderá mostrar em tempo real:\n"
            "- tempo total da sessão\n"
            "- tempo desde o último reset\n"
            "- valor atual dos contadores\n"
            "- sinais de travamento do fluxo"
        )

    def _set_textbox_content(self, texto):
        self.txt_info.configure(state="normal")
        self.txt_info.delete("1.0", "end")
        self.txt_info.insert("1.0", texto)
        self.txt_info.configure(state="disabled")

    def set_status(self, texto):
        self.status_var.set(texto)

    def set_resumo(self, texto):
        self._set_textbox_content(texto)