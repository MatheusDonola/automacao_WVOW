from multiprocessing import Process, Event, Queue
from queue import Empty

import customtkinter as ctk

from gui.sidebar_view import SidebarView
from gui.dashboard_view import DashboardView
from bot_runner import run_bot


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("WVOW Automation")
        self.geometry("980x620")
        self.minsize(900, 560)

        ctk.set_appearance_mode("dark")

        self.bot_process = None
        self.stop_event = None
        self.log_queue = None
        self.current_view = None

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = SidebarView(
            self,
            on_nav_change=self.change_view,
            on_theme_change=self.change_theme,
        )
        self.sidebar.grid(row=0, column=0, sticky="ns")

        self.main_container = ctk.CTkFrame(self, corner_radius=0)
        self.main_container.grid(row=0, column=1, sticky="nsew")
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)

        self.change_view("main")

        self.after(200, self.check_bot_process)
        self.after(100, self.process_log_queue)

    def change_theme(self, theme_name):
        ctk.set_appearance_mode(theme_name.lower())

    def change_view(self, view_name):
        if self.current_view is not None:
            self.current_view.destroy()

        if view_name == "main":
            self.current_view = DashboardView(
                self.main_container,
                on_start=self.start_bot,
                on_stop=self.stop_bot,
            )
            self.current_view.grid(row=0, column=0, sticky="nsew")
            return

        self.current_view = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.current_view.grid_columnconfigure(0, weight=1)

        title_map = {
            "settings": "Settings",
            "logs": "Logs",
            "statistics": "Statistics",
        }

        subtitle_map = {
            "settings": "Bot configuration panel.",
            "logs": "Log monitoring area.",
            "statistics": "Session statistics area.",
        }

        title = title_map.get(view_name, "View")
        subtitle = subtitle_map.get(view_name, "")

        title_label = ctk.CTkLabel(
            self.current_view,
            text=title,
            font=ctk.CTkFont(size=34, weight="bold"),
            anchor="w",
        )
        title_label.grid(row=0, column=0, sticky="ew", pady=(0, 8))

        subtitle_label = ctk.CTkLabel(
            self.current_view,
            text=subtitle,
            font=ctk.CTkFont(size=16),
            anchor="w",
            justify="left",
        )
        subtitle_label.grid(row=1, column=0, sticky="nw")

    def start_bot(self):
        self.cleanup_finished_process(force=True)

        if self.bot_process and self.bot_process.is_alive():
            if isinstance(self.current_view, DashboardView):
                self.current_view.set_status("Status: running")
                self.current_view.append_log("Bot is already running.")
            return

        if isinstance(self.current_view, DashboardView):
            self.current_view.set_status("Status: starting...")
            self.current_view.append_log("Starting bot process...")

        self.stop_event = Event()
        self.log_queue = Queue()

        self.bot_process = Process(
            target=run_bot,
            args=(self.stop_event, self.log_queue),
        )
        self.bot_process.start()

        if isinstance(self.current_view, DashboardView):
            self.current_view.set_status("Status: running")

    def stop_bot(self):
        if self.stop_event and self.bot_process:
            self.stop_event.set()

            if isinstance(self.current_view, DashboardView):
                self.current_view.set_status("Status: stopping...")
                self.current_view.append_log("Stop requested by user.")

    def cleanup_finished_process(self, force=False):
        if not self.bot_process:
            return

        finished = False

        if force:
            try:
                self.bot_process.join(timeout=0.1)
            except Exception:
                pass

        if self.bot_process.exitcode is not None:
            finished = True
        elif not self.bot_process.is_alive():
            try:
                self.bot_process.join(timeout=0.1)
            except Exception:
                pass
            finished = True

        if finished:
            self.bot_process = None
            self.stop_event = None
            self.log_queue = None

            if isinstance(self.current_view, DashboardView):
                self.current_view.set_status("Status: stopped")

    def check_bot_process(self):
        try:
            self.cleanup_finished_process()
        except Exception as e:
            print(f"[GUI ERROR] check_bot_process: {e}")
        finally:
            self.after(200, self.check_bot_process)

    def process_log_queue(self):
        try:
            if self.log_queue is not None:
                processed = 0
                max_per_cycle = 50

                while processed < max_per_cycle:
                    message = self.log_queue.get_nowait()

                    if message == "__BOT_FINISHED__":
                        if isinstance(self.current_view, DashboardView):
                            self.current_view.append_log("Bot finished.")
                        self.cleanup_finished_process(force=True)
                        break

                    if isinstance(self.current_view, DashboardView):
                        self.current_view.append_log(message)

                    processed += 1

        except Empty:
            pass
        except Exception as e:
            print(f"[GUI ERROR] process_log_queue: {e}")
        finally:
            self.after(100, self.process_log_queue)