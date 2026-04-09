import customtkinter as ctk


class DashboardView(ctk.CTkFrame):
    def __init__(self, master, on_start=None, on_stop=None):
        super().__init__(master, corner_radius=0)

        self.on_start = on_start
        self.on_stop = on_stop

        self.status_var = ctk.StringVar(value="Status: stopped")

        self._build_layout()

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))

        self.top_bar.grid_columnconfigure(0, weight=1)
        self.top_bar.grid_columnconfigure(1, weight=0)

        self.header_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="nw", padx=(0, 20))

        self.actions_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.actions_frame.grid(row=0, column=1, sticky="ne")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Main",
            font=ctk.CTkFont(size=34, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Main control area for the bot.",
            font=ctk.CTkFont(size=16),
            anchor="w",
            justify="left",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(0, 8))

        self.status_label = ctk.CTkLabel(
            self.header_frame,
            textvariable=self.status_var,
            font=ctk.CTkFont(size=15),
            anchor="w",
        )
        self.status_label.grid(row=2, column=0, sticky="w")

        self.start_button = ctk.CTkButton(
            self.actions_frame,
            text="Start Bot",
            width=140,
            height=48,
            command=self._handle_start,
        )
        self.start_button.grid(row=0, column=0, padx=(0, 12), pady=(8, 0))

        self.stop_button = ctk.CTkButton(
            self.actions_frame,
            text="Stop Bot",
            width=140,
            height=48,
            command=self._handle_stop,
        )
        self.stop_button.grid(row=0, column=1, pady=(8, 0))

        self.logs_frame = ctk.CTkFrame(self)
        self.logs_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=(0, 20))

        self.logs_frame.grid_columnconfigure(0, weight=1)
        self.logs_frame.grid_rowconfigure(1, weight=1)

        self.logs_title = ctk.CTkLabel(
            self.logs_frame,
            text="Main Logs",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self.logs_title.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        self.logs_box = ctk.CTkTextbox(
            self.logs_frame,
            wrap="word",
            font=ctk.CTkFont(size=14),
        )
        self.logs_box.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))
        self.logs_box.insert("1.0", "Main view is ready.\n")
        self.logs_box.configure(state="disabled")

    def _handle_start(self):
        if self.on_start:
            self.on_start()

    def _handle_stop(self):
        if self.on_stop:
            self.on_stop()

    def set_status(self, text):
        self.status_var.set(text)

    def append_log(self, message):
        self.logs_box.configure(state="normal")
        self.logs_box.insert("end", f"{message}\n")
        self.logs_box.see("end")
        self.logs_box.configure(state="disabled")

    def clear_logs(self):
        self.logs_box.configure(state="normal")
        self.logs_box.delete("1.0", "end")
        self.logs_box.configure(state="disabled")