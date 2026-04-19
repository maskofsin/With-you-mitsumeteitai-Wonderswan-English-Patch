#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
With You - Mitsumete Itai (WonderSwan Color) font viewer/editor.

Main font bank format (verified):
- ROM base: 0x3D0000
- u16 count
- count * u16 sorted code table
- 6 bytes of FF padding
- glyph records, 24 bytes each
- glyph layout is 12x12 1bpp-like packed as:
    bytes 0x00-0x0B: rows 0..11, left 8 pixels, bit 7 = x0 .. bit 0 = x7
    bytes 0x0C-0x17: rows 0..11, right 4 pixels only in HIGH nibble
                       bit 7 = x8, bit 6 = x9, bit 5 = x10, bit 4 = x11
                       low nibble must remain zero/padding

This editor preserves the unused low nibble on save.
"""

from __future__ import annotations

import os
import shutil
import struct
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import List, Optional, Tuple

APP_TITLE = "With You Font Editor"
ROM_BASE = 0x3D0000
PADDING_LEN = 6
GLYPH_W = 12
GLYPH_H = 12
GLYPH_BYTES = 24
DEFAULT_SCALE = 24
THUMB_SCALE = 2
GRID_COLS = 8
GRID_ROWS = 8
PAGE_SIZE = GRID_COLS * GRID_ROWS
DEFAULT_ROM = os.path.join(os.path.dirname(__file__), "With You - Mitsumete Itai (Japan).wsc")


class FontBank:
    def __init__(self, rom_path: str):
        self.rom_path = rom_path
        with open(rom_path, "rb") as f:
            self.rom = bytearray(f.read())
        if len(self.rom) < ROM_BASE + 2:
            raise ValueError("ROM too small or wrong file.")
        self.count = struct.unpack_from("<H", self.rom, ROM_BASE)[0]
        self.codes = list(struct.unpack_from("<" + "H" * self.count, self.rom, ROM_BASE + 2))
        self.glyph_start = ROM_BASE + 2 + self.count * 2 + PADDING_LEN
        self.glyph_end = self.glyph_start + self.count * GLYPH_BYTES
        if self.glyph_end > len(self.rom):
            raise ValueError("Font bank extends past end of ROM.")
        self.dirty_indices: set[int] = set()

    def glyph_offset(self, index: int) -> int:
        return self.glyph_start + index * GLYPH_BYTES

    def get_glyph_bytes(self, index: int) -> bytes:
        off = self.glyph_offset(index)
        return bytes(self.rom[off:off + GLYPH_BYTES])

    def get_glyph_pixels(self, index: int) -> List[List[int]]:
        data = self.get_glyph_bytes(index)
        rows = [[0] * GLYPH_W for _ in range(GLYPH_H)]
        left = data[:12]
        right = data[12:]
        for y in range(GLYPH_H):
            b0 = left[y]
            b1 = right[y]
            for x in range(8):
                rows[y][x] = 1 if (b0 & (0x80 >> x)) else 0
            for x in range(4):
                rows[y][8 + x] = 1 if (b1 & (0x80 >> x)) else 0
        return rows

    def set_glyph_pixels(self, index: int, pixels: List[List[int]]) -> None:
        if len(pixels) != GLYPH_H or any(len(row) != GLYPH_W for row in pixels):
            raise ValueError("Bad glyph size.")
        off = self.glyph_offset(index)
        old = self.get_glyph_bytes(index)
        out = bytearray(GLYPH_BYTES)
        # preserve low nibble padding from original right strip just in case
        for y in range(GLYPH_H):
            b0 = 0
            b1 = old[12 + y] & 0x0F
            for x in range(8):
                if pixels[y][x]:
                    b0 |= (0x80 >> x)
            for x in range(4):
                if pixels[y][8 + x]:
                    b1 |= (0x80 >> x)
            out[y] = b0
            out[12 + y] = b1
        self.rom[off:off + GLYPH_BYTES] = out
        self.dirty_indices.add(index)

    def save(self, out_path: Optional[str] = None, make_backup: bool = True) -> str:
        target = out_path or self.rom_path
        if make_backup and os.path.abspath(target) == os.path.abspath(self.rom_path):
            bak = self.rom_path + ".fontedit.bak"
            if not os.path.exists(bak):
                shutil.copy2(self.rom_path, bak)
        with open(target, "wb") as f:
            f.write(self.rom)
        if out_path is None:
            self.rom_path = target
        self.dirty_indices.clear()
        return target


class PixelEditor(tk.Canvas):
    def __init__(self, master, app, **kwargs):
        super().__init__(master, width=GLYPH_W * DEFAULT_SCALE, height=GLYPH_H * DEFAULT_SCALE,
                         bg="#f0f0f0", highlightthickness=1, highlightbackground="#666", **kwargs)
        self.app = app
        self.scale = DEFAULT_SCALE
        self.mode = "draw"
        self.bind("<Button-1>", self.on_left)
        self.bind("<B1-Motion>", self.on_left)
        self.bind("<Button-3>", self.on_right)
        self.bind("<B3-Motion>", self.on_right)
        self.bind("<Configure>", lambda e: self.redraw())

    def set_mode(self, mode: str) -> None:
        self.mode = mode

    def coord_to_pixel(self, event) -> Optional[Tuple[int, int]]:
        x = int(event.x // self.scale)
        y = int(event.y // self.scale)
        if 0 <= x < GLYPH_W and 0 <= y < GLYPH_H:
            return x, y
        return None

    def on_left(self, event) -> None:
        p = self.coord_to_pixel(event)
        if p is None:
            return
        x, y = p
        if self.mode == "toggle":
            self.app.current_pixels[y][x] ^= 1
        else:
            self.app.current_pixels[y][x] = 1
        self.app.mark_dirty_current()
        self.redraw()
        self.app.refresh_thumb_for_current()

    def on_right(self, event) -> None:
        p = self.coord_to_pixel(event)
        if p is None:
            return
        x, y = p
        self.app.current_pixels[y][x] = 0
        self.app.mark_dirty_current()
        self.redraw()
        self.app.refresh_thumb_for_current()

    def redraw(self) -> None:
        self.delete("all")
        px = self.app.current_pixels
        for y in range(GLYPH_H):
            for x in range(GLYPH_W):
                x0 = x * self.scale
                y0 = y * self.scale
                x1 = x0 + self.scale
                y1 = y0 + self.scale
                fill = "#111" if px[y][x] else "#fff"
                self.create_rectangle(x0, y0, x1, y1, fill=fill, outline="#cfcfcf")
        for x in range(GLYPH_W + 1):
            color = "#808080" if x in (0, 8, 12) else "#d8d8d8"
            xx = x * self.scale
            self.create_line(xx, 0, xx, GLYPH_H * self.scale, fill=color)
        for y in range(GLYPH_H + 1):
            color = "#808080" if y in (0, 12) else "#d8d8d8"
            yy = y * self.scale
            self.create_line(0, yy, GLYPH_W * self.scale, yy, fill=color)
        # label right-strip boundary
        self.create_text((8 * self.scale) + 6, 8, anchor="nw", text="8+4", fill="#4c6", font=("Segoe UI", 9, "bold"))


class FontEditorApp:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1260x920")
        self.bank: Optional[FontBank] = None
        self.current_index = 0
        self.current_page = 0
        self.current_pixels: List[List[int]] = [[0] * GLYPH_W for _ in range(GLYPH_H)]
        self.thumb_canvases: List[tk.Canvas] = []
        self.thumb_labels: List[tk.Label] = []
        self.thumb_index_map: List[int] = []
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Open a ROM to begin.")
        self.info_var = tk.StringVar(value="")
        self.rom_var = tk.StringVar(value="")
        self.mode_var = tk.StringVar(value="draw")
        self._build_ui()
        if os.path.exists(DEFAULT_ROM):
            try:
                self.load_rom(DEFAULT_ROM)
            except Exception as exc:
                self.status(f"Default ROM load failed: {exc}")

    def _build_ui(self) -> None:
        top = ttk.Frame(self.root, padding=8)
        top.pack(fill="x")

        ttk.Label(top, text="ROM:").pack(side="left")
        ttk.Entry(top, textvariable=self.rom_var, width=70).pack(side="left", padx=(4, 6), fill="x", expand=True)
        ttk.Button(top, text="Open ROM", command=self.choose_rom).pack(side="left", padx=2)
        ttk.Button(top, text="Save", command=self.save_rom).pack(side="left", padx=2)
        ttk.Button(top, text="Save As", command=self.save_rom_as).pack(side="left", padx=2)
        ttk.Button(top, text="Revert Glyph", command=self.reload_current_glyph).pack(side="left", padx=2)

        tools = ttk.Frame(self.root, padding=(8, 0, 8, 8))
        tools.pack(fill="x")
        ttk.Label(tools, text="Find code/index:").pack(side="left")
        entry = ttk.Entry(tools, textvariable=self.search_var, width=20)
        entry.pack(side="left", padx=(4, 6))
        entry.bind("<Return>", lambda e: self.jump_to_search())
        ttk.Button(tools, text="Go", command=self.jump_to_search).pack(side="left")
        ttk.Button(tools, text="Prev Page", command=lambda: self.change_page(-1)).pack(side="left", padx=2)
        ttk.Button(tools, text="Next Page", command=lambda: self.change_page(1)).pack(side="left", padx=2)
        ttk.Button(tools, text="Copy ←", command=self.copy_from_prev).pack(side="left", padx=8)
        ttk.Button(tools, text="Copy →", command=self.copy_from_next).pack(side="left", padx=2)
        ttk.Button(tools, text="Flip H", command=self.flip_h).pack(side="left", padx=8)
        ttk.Button(tools, text="Shift ←", command=lambda: self.shift(-1, 0)).pack(side="left", padx=2)
        ttk.Button(tools, text="Shift →", command=lambda: self.shift(1, 0)).pack(side="left", padx=2)
        ttk.Button(tools, text="Shift ↑", command=lambda: self.shift(0, -1)).pack(side="left", padx=2)
        ttk.Button(tools, text="Shift ↓", command=lambda: self.shift(0, 1)).pack(side="left", padx=2)
        ttk.Button(tools, text="Clear", command=self.clear_current).pack(side="left", padx=8)

        mode_frame = ttk.LabelFrame(self.root, text="Tool", padding=8)
        mode_frame.pack(fill="x", padx=8)
        ttk.Radiobutton(mode_frame, text="Pencil", value="draw", variable=self.mode_var,
                        command=lambda: self.editor.set_mode(self.mode_var.get())).pack(side="left")
        ttk.Radiobutton(mode_frame, text="Toggle", value="toggle", variable=self.mode_var,
                        command=lambda: self.editor.set_mode(self.mode_var.get())).pack(side="left", padx=8)
        ttk.Label(mode_frame, text="Left = draw/toggle, Right = erase").pack(side="left", padx=12)

        main = ttk.Panedwindow(self.root, orient="horizontal")
        main.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(main)
        right = ttk.Frame(main)
        main.add(left, weight=3)
        main.add(right, weight=2)

        # Editor panel
        editor_wrap = ttk.LabelFrame(left, text="Glyph Editor", padding=8)
        editor_wrap.pack(fill="both", expand=True)
        self.editor = PixelEditor(editor_wrap, self)
        self.editor.pack(side="left", padx=(0, 12), pady=4)

        side = ttk.Frame(editor_wrap)
        side.pack(side="left", fill="y")
        ttk.Label(side, textvariable=self.info_var, justify="left").pack(anchor="nw")
        ttk.Separator(side, orient="horizontal").pack(fill="x", pady=8)
        ttk.Label(side, text="Notes", font=("Segoe UI", 10, "bold")).pack(anchor="nw")
        notes = (
            "Font format:\n"
            "• 12x12 pixels\n"
            "• 24 bytes per glyph\n"
            "• first 12 bytes = left 8 pixels\n"
            "• second 12 bytes = right 4 pixels in high nibble\n"
            "• low nibble is preserved as padding\n"
        )
        ttk.Label(side, text=notes, justify="left").pack(anchor="nw")

        # Grid panel
        grid_wrap = ttk.LabelFrame(right, text="Font Grid", padding=8)
        grid_wrap.pack(fill="both", expand=True)
        self.grid_inner = ttk.Frame(grid_wrap)
        self.grid_inner.pack(fill="both", expand=True)
        for n in range(PAGE_SIZE):
            cell = ttk.Frame(self.grid_inner, padding=2)
            r, c = divmod(n, GRID_COLS)
            cell.grid(row=r, column=c, sticky="nsew")
            cv = tk.Canvas(cell, width=GLYPH_W * THUMB_SCALE + 2, height=GLYPH_H * THUMB_SCALE + 2,
                           bg="#ffffff", highlightthickness=1, highlightbackground="#999")
            cv.pack()
            lab = ttk.Label(cell, text="", justify="center")
            lab.pack()
            cv.bind("<Button-1>", lambda e, i=n: self.select_thumb(i))
            lab.bind("<Button-1>", lambda e, i=n: self.select_thumb(i))
            self.thumb_canvases.append(cv)
            self.thumb_labels.append(lab)
            self.thumb_index_map.append(-1)
        for c in range(GRID_COLS):
            self.grid_inner.columnconfigure(c, weight=1)
        for r in range(GRID_ROWS):
            self.grid_inner.rowconfigure(r, weight=1)

        status = ttk.Label(self.root, textvariable=self.status_var, anchor="w", relief="sunken", padding=6)
        status.pack(fill="x")

    def status(self, msg: str) -> None:
        self.status_var.set(msg)
        self.root.update_idletasks()

    def choose_rom(self) -> None:
        path = filedialog.askopenfilename(
            title="Open WonderSwan ROM",
            filetypes=[("WonderSwan ROM", "*.wsc *.ws"), ("All files", "*.*")],
        )
        if path:
            self.load_rom(path)

    def load_rom(self, path: str) -> None:
        self.bank = FontBank(path)
        self.rom_var.set(path)
        self.current_page = 0
        self.current_index = 0
        self.load_current_glyph()
        self.refresh_grid()
        self.status(f"Loaded {os.path.basename(path)} | glyphs: {self.bank.count} | font @ 0x{ROM_BASE:06X}")

    def select_thumb(self, local_idx: int) -> None:
        index = self.current_page * PAGE_SIZE + local_idx
        if not self.bank or index >= self.bank.count:
            return
        self.current_index = index
        self.load_current_glyph()
        self.refresh_grid()

    def load_current_glyph(self) -> None:
        if not self.bank:
            return
        self.current_pixels = self.bank.get_glyph_pixels(self.current_index)
        code = self.bank.codes[self.current_index]
        off = self.bank.glyph_offset(self.current_index)
        dirty = " *dirty*" if self.current_index in self.bank.dirty_indices else ""
        self.info_var.set(
            f"Index: {self.current_index}\n"
            f"Code: 0x{code:04X}\n"
            f"ROM offset: 0x{off:06X}\n"
            f"Page: {self.current_page + 1}/{max(1, (self.bank.count + PAGE_SIZE - 1)//PAGE_SIZE)}{dirty}"
        )
        self.editor.redraw()

    def mark_dirty_current(self) -> None:
        if not self.bank:
            return
        self.bank.set_glyph_pixels(self.current_index, self.current_pixels)
        self.load_current_glyph()

    def refresh_thumb_for_current(self) -> None:
        if not self.bank:
            return
        if self.current_index < self.current_page * PAGE_SIZE or self.current_index >= (self.current_page + 1) * PAGE_SIZE:
            return
        self.refresh_grid()

    def draw_thumb(self, canvas: tk.Canvas, pixels: List[List[int]], selected: bool) -> None:
        canvas.delete("all")
        bg = "#fff7d6" if selected else "#ffffff"
        canvas.configure(bg=bg, highlightbackground="#d18a00" if selected else "#999")
        scale = THUMB_SCALE
        for y in range(GLYPH_H):
            for x in range(GLYPH_W):
                x0 = 1 + x * scale
                y0 = 1 + y * scale
                x1 = x0 + scale
                y1 = y0 + scale
                fill = "#111" if pixels[y][x] else bg
                canvas.create_rectangle(x0, y0, x1, y1, fill=fill, outline=fill)

    def refresh_grid(self) -> None:
        if not self.bank:
            return
        start = self.current_page * PAGE_SIZE
        for n in range(PAGE_SIZE):
            idx = start + n
            cv = self.thumb_canvases[n]
            lab = self.thumb_labels[n]
            self.thumb_index_map[n] = idx
            if idx < self.bank.count:
                pixels = self.bank.get_glyph_pixels(idx)
                self.draw_thumb(cv, pixels, idx == self.current_index)
                code = self.bank.codes[idx]
                marker = "*" if idx in self.bank.dirty_indices else ""
                lab.configure(text=f"{idx}\n{code:04X}{marker}")
            else:
                cv.delete("all")
                cv.configure(bg="#f0f0f0")
                lab.configure(text="")
        self.load_current_glyph()

    def change_page(self, delta: int) -> None:
        if not self.bank:
            return
        max_page = max(0, (self.bank.count - 1) // PAGE_SIZE)
        self.current_page = min(max(self.current_page + delta, 0), max_page)
        start = self.current_page * PAGE_SIZE
        if not (start <= self.current_index < start + PAGE_SIZE):
            self.current_index = start
        self.refresh_grid()

    def jump_to_search(self) -> None:
        if not self.bank:
            return
        text = self.search_var.get().strip()
        if not text:
            return
        idx = None
        try:
            if text.lower().startswith("0x"):
                code = int(text, 16)
                idx = self.bank.codes.index(code)
            elif len(text) == 4 and all(ch in "0123456789abcdefABCDEF" for ch in text):
                code = int(text, 16)
                idx = self.bank.codes.index(code)
            else:
                idx = int(text)
                if not (0 <= idx < self.bank.count):
                    raise ValueError
        except ValueError:
            messagebox.showerror(APP_TITLE, "Enter a glyph index or a 4-digit code like 829F or 0x829F.")
            return
        except Exception:
            messagebox.showerror(APP_TITLE, f"Not found: {text}")
            return
        self.current_index = idx
        self.current_page = idx // PAGE_SIZE
        self.refresh_grid()

    def reload_current_glyph(self) -> None:
        if not self.bank:
            return
        # reload from current ROM buffer is same as current memory; to truly revert, reload from file.
        path = self.bank.rom_path
        idx = self.current_index
        page = self.current_page
        self.bank = FontBank(path)
        self.current_index = idx
        self.current_page = page
        self.load_current_glyph()
        self.refresh_grid()
        self.status("Reloaded current ROM from disk.")

    def clear_current(self) -> None:
        self.current_pixels = [[0] * GLYPH_W for _ in range(GLYPH_H)]
        self.mark_dirty_current()
        self.refresh_grid()

    def copy_from_prev(self) -> None:
        if not self.bank or self.current_index <= 0:
            return
        self.current_pixels = self.bank.get_glyph_pixels(self.current_index - 1)
        self.mark_dirty_current()
        self.refresh_grid()

    def copy_from_next(self) -> None:
        if not self.bank or self.current_index + 1 >= self.bank.count:
            return
        self.current_pixels = self.bank.get_glyph_pixels(self.current_index + 1)
        self.mark_dirty_current()
        self.refresh_grid()

    def flip_h(self) -> None:
        self.current_pixels = [list(reversed(row)) for row in self.current_pixels]
        self.mark_dirty_current()
        self.refresh_grid()

    def shift(self, dx: int, dy: int) -> None:
        out = [[0] * GLYPH_W for _ in range(GLYPH_H)]
        for y in range(GLYPH_H):
            for x in range(GLYPH_W):
                sx = x - dx
                sy = y - dy
                if 0 <= sx < GLYPH_W and 0 <= sy < GLYPH_H:
                    out[y][x] = self.current_pixels[sy][sx]
        self.current_pixels = out
        self.mark_dirty_current()
        self.refresh_grid()

    def save_rom(self) -> None:
        if not self.bank:
            return
        try:
            target = self.bank.save(make_backup=True)
            self.status(f"Saved ROM: {target} (backup created once as .fontedit.bak)")
            self.refresh_grid()
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Save failed:\n{exc}")

    def save_rom_as(self) -> None:
        if not self.bank:
            return
        path = filedialog.asksaveasfilename(
            title="Save ROM As",
            defaultextension=".wsc",
            filetypes=[("WonderSwan ROM", "*.wsc *.ws"), ("All files", "*.*")],
            initialfile=os.path.basename(self.bank.rom_path).replace(".wsc", "_fontedit.wsc"),
        )
        if not path:
            return
        try:
            self.bank.save(out_path=path, make_backup=False)
            self.status(f"Saved ROM copy: {path}")
        except Exception as exc:
            messagebox.showerror(APP_TITLE, f"Save As failed:\n{exc}")


def main() -> None:
    root = tk.Tk()
    try:
        root.iconname(APP_TITLE)
    except Exception:
        pass
    app = FontEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
