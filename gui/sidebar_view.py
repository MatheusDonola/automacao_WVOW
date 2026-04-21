import customtkinter as ctk


class SidebarView(ctk.CTkFrame):
    def __init__(self, master, on_nav_change=None, on_theme_change=None):
        super().__init__(master, width=260, corner_radius=0)

        self.on_nav_change = on_nav_change
        self.on_theme_change = on_theme_change

        self.grid_propagate(False)

        self._build_layout()

    def _build_layout(self):
        self.grid_rowconfigure(7, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.title_label = ctk.CTkLabel(
            self,
            text="WVOW Automation",
            font=ctk.CTkFont(size=24, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(22, 4), sticky="ew")

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Control Panel",
            font=ctk.CTkFont(size=16),
            anchor="w",
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 18), sticky="ew")

        button_height = 48

        self.main_button = ctk.CTkButton(
            self,
            text="Main",
            height=button_height,
            command=lambda: self._handle_nav("main"),
        )
        self.main_button.grid(row=2, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.settings_button = ctk.CTkButton(
            self,
            text="Settings",
            height=button_height,
            command=lambda: self._handle_nav("settings"),
        )
        self.settings_button.grid(row=3, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.logs_button = ctk.CTkButton(
            self,
            text="Logs",
            height=button_height,
            command=lambda: self._handle_nav("logs"),
        )
        self.logs_button.grid(row=4, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.stats_button = ctk.CTkButton(
            self,
            text="Statistics",
            height=button_height,
            command=lambda: self._handle_nav("statistics"),
        )
        self.stats_button.grid(row=5, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.tower_siege_button = ctk.CTkButton(
            self,
            text="Tower Siege",
            height=button_height,
            command=lambda: self._handle_nav("tower_siege"),
        )
        self.tower_siege_button.grid(row=6, column=0, padx=18, pady=(0, 12), sticky="ew")

        self.theme_menu = ctk.CTkOptionMenu(
            self,
            values=["Dark", "Light", "System"],
            command=self._handle_theme_change,
        )
        self.theme_menu.set("Dark")
        self.theme_menu.grid(row=8, column=0, padx=18, pady=18, sticky="ew")

    def _handle_nav(self, view_name):
        if self.on_nav_change:
            self.on_nav_change(view_name)

    def _handle_theme_change(self, theme_name):
        if self.on_theme_change:
            self.on_theme_change(theme_name)