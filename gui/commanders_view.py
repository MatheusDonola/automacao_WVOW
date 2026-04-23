import shutil
from pathlib import Path

import customtkinter as ctk
from PIL import Image


class CommandersView(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, corner_radius=0)

        self.project_root = Path(__file__).resolve().parents[1]
        self.assets_dir = self.project_root / "assets"
        self.cmds_dir = self.assets_dir / "cmds"
        self.allcmds_dir = self.assets_dir / "allcmds"
        self.allcmds_preview_dir = self.assets_dir / "allcmds_preview"

        self.allcmds_dir.mkdir(parents=True, exist_ok=True)
        self.allcmds_preview_dir.mkdir(parents=True, exist_ok=True)
        self.cmds_dir.mkdir(parents=True, exist_ok=True)
        self.allcmds_dir.mkdir(parents=True, exist_ok=True)
        self.cmds_preview_dir = self.assets_dir / "cmds_preview"
        self.cmds_preview_dir.mkdir(parents=True, exist_ok=True)

        self.commander_count = ctk.IntVar(value=3)
        self.selected_slot = 1

        self.slot_frames = {}
        self.slot_image_labels = {}
        self.slot_name_labels = {}
        self.gallery_cards = []
        self._image_refs = []

        self._build_layout()
        self._load_selected_slots()
        self._load_gallery()

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)

        # topo
        self.top_bar = ctk.CTkFrame(self, fg_color="transparent")
        self.top_bar.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        self.top_bar.grid_columnconfigure(0, weight=1)

        self.header_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.header_frame.grid(row=0, column=0, sticky="w")

        self.actions_frame = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        self.actions_frame.grid(row=0, column=1, sticky="e")

        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Commanders",
            font=ctk.CTkFont(size=34, weight="bold"),
            anchor="w",
        )
        self.title_label.grid(row=0, column=0, sticky="w")

        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="Select 3 or 4 commanders and save them to the cmds folder.",
            font=ctk.CTkFont(size=16),
            anchor="w",
            justify="left",
        )
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(6, 0))

        self.count_menu = ctk.CTkOptionMenu(
            self.actions_frame,
            values=["3", "4"],
            command=self._on_count_change,
            width=90,
            height=40,
        )
        self.count_menu.set("3")
        self.count_menu.grid(row=0, column=0, padx=(0, 10))

        self.info_label = ctk.CTkLabel(
            self.actions_frame,
            text="Selected slot: cmd1",
            font=ctk.CTkFont(size=14),
        )
        self.info_label.grid(row=0, column=1)

        # slots
        self.slots_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.slots_frame.grid(row=1, column=0, sticky="ew", padx=20, pady=(10, 14))
        for col in range(4):
            self.slots_frame.grid_columnconfigure(col, weight=1)

        for slot_index in range(1, 5):
            card = ctk.CTkFrame(self.slots_frame, corner_radius=12)
            card.grid(row=0, column=slot_index - 1, sticky="nsew", padx=8)
            card.grid_rowconfigure(1, weight=1)
            card.grid_columnconfigure(0, weight=1)

            button = ctk.CTkButton(
                card,
                text=f"cmd{slot_index}",
                command=lambda s=slot_index: self._select_slot(s),
                height=34,
            )
            button.grid(row=0, column=0, sticky="ew", padx=12, pady=(12, 8))

            image_label = ctk.CTkLabel(card, text="Empty", width=120, height=90)
            image_label.grid(row=1, column=0, padx=12, pady=6)

            name_label = ctk.CTkLabel(
                card,
                text="No commander selected",
                font=ctk.CTkFont(size=12),
                wraplength=150,
            )
            name_label.grid(row=2, column=0, padx=12, pady=(4, 12))

            self.slot_frames[slot_index] = card
            self.slot_image_labels[slot_index] = image_label
            self.slot_name_labels[slot_index] = name_label

        self._highlight_selected_slot()

        # divisória
        self.divider = ctk.CTkFrame(self, height=2)
        self.divider.grid(row=2, column=0, sticky="ew", padx=20, pady=(0, 14))

        # galeria
        self.gallery_container = ctk.CTkFrame(self)
        self.gallery_container.grid(row=3, column=0, sticky="nsew", padx=20, pady=(0, 20))
        self.gallery_container.grid_columnconfigure(0, weight=1)
        self.gallery_container.grid_rowconfigure(1, weight=1)

        self.gallery_title = ctk.CTkLabel(
            self.gallery_container,
            text="Available Commanders",
            font=ctk.CTkFont(size=22, weight="bold"),
            anchor="w",
        )
        self.gallery_title.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 8))

        self.gallery_scroll = ctk.CTkScrollableFrame(self.gallery_container)
        self.gallery_scroll.grid(row=1, column=0, sticky="nsew", padx=16, pady=(0, 16))

    def _on_count_change(self, value):
        count = int(value)
        self.commander_count.set(count)

        if self.selected_slot > count:
            self.selected_slot = count
            self.info_label.configure(text=f"Selected slot: cmd{self.selected_slot}")

        cmd4_preview_path = self.cmds_preview_dir / "cmd4.png"
        if count == 3 and cmd4_preview_path.exists():
            cmd4_preview_path.unlink()

        self._load_selected_slots()
        self._highlight_selected_slot()

    def _select_slot(self, slot_index):
        if slot_index > self.commander_count.get():
            return

        self.selected_slot = slot_index
        self.info_label.configure(text=f"Selected slot: cmd{slot_index}")
        self._highlight_selected_slot()

    def _highlight_selected_slot(self):
        for slot_index, frame in self.slot_frames.items():
            border_width = 3 if slot_index == self.selected_slot and slot_index <= self.commander_count.get() else 1
            frame.configure(border_width=border_width)

            if slot_index <= self.commander_count.get():
                frame.grid()
            else:
                frame.grid_remove()

    def _load_selected_slots(self):
        self._image_refs = []

        for slot_index in range(1, 5):
            image_label = self.slot_image_labels[slot_index]
            name_label = self.slot_name_labels[slot_index]

            technical_path = self.cmds_dir / f"cmd{slot_index}.png"
            display_path = self._get_selected_slot_display_path(slot_index)

            if slot_index > self.commander_count.get():
                continue

            if technical_path.exists():
                image = self._build_ctk_image(display_path, (96, 96))
                image_label.configure(text="", image=image)
                name_label.configure(text=technical_path.name)
                self._image_refs.append(image)
            else:
                image_label.configure(text="Empty", image=None)
                name_label.configure(text="No commander selected")

    def _load_gallery(self):
        for widget in self.gallery_scroll.winfo_children():
            widget.destroy()

        self.gallery_cards.clear()
        self._image_refs = []

        image_files = self._get_image_files(self.allcmds_dir)

        if not image_files:
            empty_label = ctk.CTkLabel(
                self.gallery_scroll,
                text="No images found in assets/allcmds",
                font=ctk.CTkFont(size=14),
            )
            empty_label.pack(anchor="w", padx=6, pady=6)
            return

        cols = 4
        for col in range(cols):
            self.gallery_scroll.grid_columnconfigure(col, weight=1)

        for index, image_path in enumerate(image_files):
            row = index // cols
            col = index % cols

            card = ctk.CTkFrame(self.gallery_scroll, corner_radius=12)
            card.grid(row=row, column=col, sticky="nsew", padx=8, pady=8)
            card.grid_columnconfigure(0, weight=1)

            display_path = self._get_display_image_path(image_path)
            preview = self._build_ctk_image(display_path, (92, 92))
            self._image_refs.append(preview)

            img_label = ctk.CTkLabel(card, text="", image=preview)
            img_label.grid(row=0, column=0, padx=12, pady=(12, 8))

            name_label = ctk.CTkLabel(
                card,
                text=image_path.stem,
                wraplength=140,
                font=ctk.CTkFont(size=12),
            )
            name_label.grid(row=1, column=0, padx=10, pady=(0, 8))

            select_button = ctk.CTkButton(
                card,
                text="Use in selected slot",
                command=lambda p=image_path: self._assign_commander_to_selected_slot(p),
                height=32,
            )
            select_button.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 12))

            self.gallery_cards.append(card)

    def _assign_commander_to_selected_slot(self, source_path):
        slot_index = self.selected_slot

        if slot_index > self.commander_count.get():
            return

        technical_target = self.cmds_dir / f"cmd{slot_index}.png"
        preview_target = self.cmds_preview_dir / f"cmd{slot_index}.png"

        shutil.copyfile(source_path, technical_target)

        display_source = self._get_display_image_path(source_path)
        shutil.copyfile(display_source, preview_target)

        self._load_selected_slots()

    def _get_image_files(self, folder: Path):
        valid_suffixes = {".png", ".jpg", ".jpeg", ".webp"}
        return sorted([p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in valid_suffixes])

    def _build_ctk_image(self, image_path: Path, size: tuple[int, int]):
        pil_image = Image.open(image_path)
        return ctk.CTkImage(light_image=pil_image, dark_image=pil_image, size=size)
    
    def _get_display_image_path(self, technical_path):
        preview_path = self.allcmds_preview_dir / technical_path.name

        if preview_path.exists():
            return preview_path

        return technical_path
    
    def _get_selected_slot_display_path(self, slot_index):
        preview_path = self.cmds_preview_dir / f"cmd{slot_index}.png"
        technical_path = self.cmds_dir / f"cmd{slot_index}.png"

        if preview_path.exists():
            return preview_path

        return technical_path