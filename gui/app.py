from multiprocessing import Process, Event, Queue
from queue import Empty

import customtkinter as ctk

from gui.sidebar_view import SidebarView
from gui.dashboard_view import DashboardView
from gui.config_view import ConfigView
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

        self.dashboard_logs = ["Main view is ready."]
        self.dashboard_status = "Status: stopped"

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

            self.current_view.set_status(self.dashboard_status)
            self.current_view.load_logs(self.dashboard_logs)
            return

        if view_name == "settings":
            self.current_view = ConfigView(self.main_container)
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
            return

        self.current_view = ctk.CTkFrame(self.main_container, corner_radius=0)
        self.current_view.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.current_view.grid_columnconfigure(0, weight=1)

        title_map = {
            "logs": "Logs",
            "statistics": "Statistics",
        }

        subtitle_map = {
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

    def append_dashboard_log(self, message):
        self.dashboard_logs.append(message)

        if isinstance(self.current_view, DashboardView):
            self.current_view.append_log(message)

    def set_dashboard_status(self, message):
        self.dashboard_status = message

        if isinstance(self.current_view, DashboardView):
            self.current_view.set_status(message)

    def start_bot(self):
        self.force_cleanup_previous_process()

        if self.bot_process is not None and self.bot_process.is_alive():
            self.set_dashboard_status("Status: running")
            self.append_dashboard_log("Bot is already running.")
            return

        self.set_dashboard_status("Status: starting...")
        self.append_dashboard_log("Starting bot process...")

        self.stop_event = Event()
        self.log_queue = Queue()

        self.bot_process = Process(
            target=run_bot,
            args=(self.stop_event, self.log_queue),
            daemon=False,
        )
        self.bot_process.start()

        self.set_dashboard_status("Status: running")

    def stop_bot(self):
        if not self.bot_process:
            self.set_dashboard_status("Status: stopped")
            self.append_dashboard_log("No bot process to stop.")
            return

        self.append_dashboard_log("Stop requested by user.")
        self.set_dashboard_status("Status: stopping...")

        if self.stop_event:
            self.stop_event.set()

        self.after(1500, self.ensure_process_stopped)

    def ensure_process_stopped(self):
        if not self.bot_process:
            self.finalize_process_cleanup()
            return

        if self.bot_process.is_alive():
            self.append_dashboard_log("Bot did not exit in time. Terminating process...")
            try:
                self.bot_process.terminate()
            except Exception as e:
                self.append_dashboard_log(f"Terminate error: {e}")

            try:
                self.bot_process.join(timeout=2)
            except Exception as e:
                self.append_dashboard_log(f"Join after terminate error: {e}")

        self.finalize_process_cleanup()

    def finalize_process_cleanup(self):
        if self.bot_process:
            try:
                if self.bot_process.is_alive():
                    return
                self.bot_process.join(timeout=0.2)
            except Exception:
                pass

        self.bot_process = None
        self.stop_event = None

        if self.log_queue is not None:
            try:
                self.log_queue.close()
            except Exception:
                pass
            try:
                self.log_queue.cancel_join_thread()
            except Exception:
                pass

        self.log_queue = None
        self.set_dashboard_status("Status: stopped")

    def force_cleanup_previous_process(self):
        if not self.bot_process:
            self.stop_event = None
            self.log_queue = None
            return

        try:
            if self.bot_process.is_alive():
                if self.stop_event:
                    self.stop_event.set()

                self.bot_process.join(timeout=1.0)

                if self.bot_process.is_alive():
                    self.append_dashboard_log("Cleaning up stale bot process...")
                    self.bot_process.terminate()
                    self.bot_process.join(timeout=2.0)
        except Exception as e:
            self.append_dashboard_log(f"Cleanup error: {e}")

        self.finalize_process_cleanup()

    def check_bot_process(self):
        try:
            if self.bot_process is not None and not self.bot_process.is_alive():
                self.finalize_process_cleanup()
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
                        self.append_dashboard_log("Bot finished.")
                        processed += 1
                        continue

                    self.append_dashboard_log(message)
                    processed += 1

        except Empty:
            pass
        except Exception as e:
            print(f"[GUI ERROR] process_log_queue: {e}")
        finally:
            self.after(100, self.process_log_queue)

