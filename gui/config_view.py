import customtkinter as ctk
import config


class ConfigView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)

        # Título
        self.title_label = ctk.CTkLabel(
            self,
            text="Settings",
            font=ctk.CTkFont(size=36, weight="bold")
        )
        self.title_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self,
            text="Bot configuration panel."
        )
        self.subtitle_label.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="w")

        # Card principal
        self.card = ctk.CTkFrame(self, corner_radius=12)
        self.card.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        self.card.grid_columnconfigure(1, weight=1)

        # ===== SPEED MODE =====
        self.speed_label = ctk.CTkLabel(self.card, text="Speed Mode")
        self.speed_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        self.speed_menu = ctk.CTkOptionMenu(
            self.card,
            values=["SLOW", "NORMAL", "FAST"]
        )
        self.speed_menu.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="ew")
        self.speed_menu.set(config.SPEED_MODE)

        # ===== TIPO =====
        self.mode_label = ctk.CTkLabel(self.card, text="Target")
        self.mode_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.mode_menu = ctk.CTkOptionMenu(
            self.card,
            values=["Firelizard", "Rebel"]
        )
        self.mode_menu.grid(row=1, column=1, padx=20, pady=10, sticky="ew")
        self.mode_menu.set("Firelizard" if config.FIRELIZARD else "Rebel")

        # ===== TEMPO STOP =====
        self.stop_label = ctk.CTkLabel(self.card, text="MAX TIME (3600 sec = 1 hour)")
        self.stop_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.stop_entry = ctk.CTkEntry(self.card, placeholder_text="Type the time in seconds")
        self.stop_entry.grid(row=2, column=1, padx=20, pady=10, sticky="ew")
        self.stop_entry.insert(0, str(config.TEMPO_STOP))

        # ===== TEMPO RESET =====
        self.reset_label = ctk.CTkLabel(self.card, text="CACHE RESET(recommended 600)")
        self.reset_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.reset_entry = ctk.CTkEntry(self.card, placeholder_text="Type the time in second")
        self.reset_entry.grid(row=3, column=1, padx=20, pady=10, sticky="ew")
        self.reset_entry.insert(0, str(config.TEMPO_RESET))

        # ===== STATUS =====
        self.status_label = ctk.CTkLabel(self.card, text="", text_color="lightgreen")
        self.status_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(10, 5), sticky="w")

        # ===== BOTÃO SALVAR =====
        self.save_button = ctk.CTkButton(
            self.card,
            text="Save Configurations",
            command=self.save_config
        )
        self.save_button.grid(row=5, column=0, columnspan=2, padx=20, pady=(10, 20), sticky="ew")

    def save_config(self):
        try:
            tempo_stop = int(self.stop_entry.get().strip())
            tempo_reset = int(self.reset_entry.get().strip())

            if tempo_stop < 0 or tempo_reset < 0:
                self.status_label.configure(
                    text="The time should be higher than 0",
                    text_color="red"
                )
                return

            speed_mode = self.speed_menu.get()
            firelizard = self.mode_menu.get() == "Firelizard"

            # Atualiza em memória
            config.SPEED_MODE = speed_mode
            config.FIRELIZARD = firelizard
            config.TEMPO_STOP = tempo_stop
            config.TEMPO_RESET = tempo_reset

            # Atualiza o arquivo config.py sem apagar o resto
            with open("config.py", "r", encoding="utf-8") as f:
                content = f.read()

            import re

            content = re.sub(
                r'^FIRELIZARD\s*=\s*(True|False)',
                f'FIRELIZARD = {firelizard}',
                content,
                flags=re.MULTILINE
            )

            content = re.sub(
                r'^SPEED_MODE\s*=\s*".*"',
                f'SPEED_MODE = "{speed_mode}"',
                content,
                flags=re.MULTILINE
            )

            content = re.sub(
                r'^TEMPO_STOP\s*=\s*\d+',
                f'TEMPO_STOP = {tempo_stop}',
                content,
                flags=re.MULTILINE
            )

            content = re.sub(
                r'^TEMPO_RESET\s*=\s*\d+',
                f'TEMPO_RESET = {tempo_reset}',
                content,
                flags=re.MULTILINE
            )

            with open("config.py", "w", encoding="utf-8") as f:
                f.write(content)

            self.status_label.configure(
                text="Succes saving the configs.",
                text_color="lightgreen"
            )

        except ValueError:
            self.status_label.configure(
                text="MAX TIME and CACHE RESET must be integers",
                text_color="red"
            )
        except Exception as e:
            self.status_label.configure(
                text=f"Erro ao salvar: {e}",
                text_color="red"
            )