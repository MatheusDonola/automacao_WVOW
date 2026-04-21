import customtkinter as ctk


class TowerSiegeView(ctk.CTkFrame):
    def __init__(self, master, on_set_spawn):
        super().__init__(master, corner_radius=0)

        self.on_set_spawn = on_set_spawn

        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="Tower Siege",
            font=ctk.CTkFont(size=34, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Mode_2 configuration area. Set the tower spawn coordinates here \n After clicking the button alt tab to the game and click on center of free spot." 
            "",
            font=ctk.CTkFont(size=16),
            anchor="w",
            justify="left",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 20))

        self.status_label = ctk.CTkLabel(
            self,
            text="Status: waiting for configuration",
            font=ctk.CTkFont(size=15),
            anchor="w",
        )
        self.status_label.grid(row=2, column=0, sticky="w", pady=(0, 20))

        self.set_spawn_button = ctk.CTkButton(
            self,
            text="Set Tower Spawn",
            command=self.on_set_spawn,
            width=180,
            height=40,
        )
        self.set_spawn_button.grid(row=3, column=0, sticky="w", pady=(0, 20))

    def set_status(self, message):
        self.status_label.configure(text=message)