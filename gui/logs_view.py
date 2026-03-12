import customtkinter as ctk


class LogsView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        titulo = ctk.CTkLabel(
            self,
            text="Logs",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        titulo.pack(pady=30)