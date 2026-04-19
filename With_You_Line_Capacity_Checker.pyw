#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
With You Line Capacity Checker

Load an extracted CSV and inspect how much script space each line has.
The app shows:
- offset and length from the CSV
- Japanese source text (decoded/visible)
- an editable translation field
- a live estimate of how many bytes/pairs your translation will consume
- remaining space versus the original line budget

CSV format expected (case-insensitive):
offset_hex,length_hex,raw_hex,decoded,visible,controls,unknown

Optional columns are accepted and ignored.
"""

from __future__ import annotations

import csv
import os
import re
import tkinter as tk
from dataclasses import dataclass
from pathlib import Path
from tkinter import filedialog, messagebox, ttk
from typing import Any, Dict, List, Optional, Tuple


SPECIAL_TOKENS = ("...", ".", ",", "!")


def _safe_int_hex(value: str) -> int:
    value = (value or "").strip()
    if not value:
        return 0
    value = value.lower().replace("0x", "")
    return int(value, 16)


def _normalize_ws(s: str) -> str:
    # Preserve meaning, but show tabs/newlines as spaces in previews.
    return s.replace("\r\n", "\n").replace("\r", "\n")


def tokenize_for_bigram_estimate(text: str, append_trailing_space: bool = True) -> List[str]:
    """
    Estimate the tokenization used by the bigram encoder:
    - special punctuation tokens first
    - remaining text is split into 2-char chunks
    - odd-length lines can be padded with a trailing space
    This is a budget estimator, not a ROM patcher.
    """
    text = _normalize_ws(text)
    tokens: List[str] = []

    for line in text.split("\n"):
        work = line
        i = 0
        line_tokens: List[str] = []
        while i < len(work):
            matched = False
            for tok in SPECIAL_TOKENS:
                if work.startswith(tok, i):
                    line_tokens.append(tok)
                    i += len(tok)
                    matched = True
                    break
            if matched:
                continue

            if i + 1 < len(work):
                line_tokens.append(work[i:i + 2])
                i += 2
            else:
                if append_trailing_space:
                    line_tokens.append(work[i] + " ")
                else:
                    line_tokens.append(work[i])
                i += 1

        tokens.extend(line_tokens)
        # newline is not encoded as a visible token in the original scripts;
        # each line is handled independently by the game text engine.

    return tokens


def estimate_encoded_bytes(text: str, append_trailing_space: bool = True) -> Tuple[int, List[str]]:
    tokens = tokenize_for_bigram_estimate(text, append_trailing_space=append_trailing_space)
    # The bigram tilemap uses 2-byte codes per token.
    return len(tokens) * 2, tokens


def strip_controls_preview(value: str) -> str:
    """
    Basic cleanup for display only.
    """
    value = _normalize_ws(value or "")
    value = re.sub(r"【[^】]*】", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def count_visible_chars(value: str) -> int:
    return len(strip_controls_preview(value))


@dataclass
class LineRow:
    row_no: int
    offset_hex: str
    length_hex: str
    raw_hex: str
    decoded: str
    visible: str
    controls: str
    unknown: str

    @property
    def offset(self) -> int:
        return _safe_int_hex(self.offset_hex)

    @property
    def length_bytes(self) -> int:
        return _safe_int_hex(self.length_hex)

    @property
    def raw_bytes(self) -> int:
        raw = re.sub(r"\s+", "", self.raw_hex or "")
        return len(raw) // 2

    @property
    def visible_text(self) -> str:
        return (self.visible or self.decoded or "").strip()

    @property
    def visible_count(self) -> int:
        return count_visible_chars(self.visible_text)

    @property
    def control_count(self) -> int:
        txt = self.controls or ""
        if not txt.strip():
            return 0
        parts = [p for p in re.split(r"[|,; ]+", txt) if p]
        return len(parts)

    @property
    def budget_chars_est(self) -> int:
        # For the paired encoder, 1 input character roughly costs 1 byte.
        # Keep this visible as an estimate, not a hard guarantee.
        return self.length_bytes


class CapacityCheckerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("With You Line Capacity Checker")
        self.geometry("1450x820")
        self.minsize(1180, 680)

        self.csv_path: Optional[Path] = None
        self.rows: List[LineRow] = []
        self.filtered_rows: List[LineRow] = []

        self.append_space_var = tk.BooleanVar(value=True)
        self.search_var = tk.StringVar()
        self.status_var = tk.StringVar(value="Open a CSV to begin.")
        self.budget_var = tk.StringVar(value="Budget: —")
        self.used_var = tk.StringVar(value="Used: —")
        self.remaining_var = tk.StringVar(value="Remaining: —")
        self.tokens_var = tk.StringVar(value="Tokens: —")
        self.offset_var = tk.StringVar(value="Offset: —")
        self.len_var = tk.StringVar(value="Length: —")
        self.visible_var = tk.StringVar(value="Visible chars: —")
        self.controls_var = tk.StringVar(value="Controls: —")
        self.raw_var = tk.StringVar(value="Raw hex: —")

        self._build_ui()
        self.bind_all("<Control-o>", lambda e: self.open_csv())
        self.bind_all("<Control-f>", lambda e: self.search_entry.focus_set())
        self.bind_all("<Control-r>", lambda e: self.refresh_filtered())
        self.bind_all("<Control-c>", lambda e: self.copy_selected_stats())

    def _build_ui(self) -> None:
        top = ttk.Frame(self, padding=8)
        top.pack(fill="x")

        ttk.Button(top, text="Open CSV", command=self.open_csv).pack(side="left")
        ttk.Button(top, text="Refresh", command=self.refresh_filtered).pack(side="left", padx=(8, 0))
        ttk.Checkbutton(
            top,
            text="Pad odd lines with trailing space",
            variable=self.append_space_var,
            command=self._update_selected_estimate,
        ).pack(side="left", padx=(16, 0))

        ttk.Label(top, text="Search:").pack(side="left", padx=(18, 6))
        self.search_entry = ttk.Entry(top, textvariable=self.search_var, width=38)
        self.search_entry.pack(side="left")
        self.search_entry.bind("<Return>", lambda e: self.refresh_filtered())
        ttk.Button(top, text="Go", command=self.refresh_filtered).pack(side="left", padx=(6, 0))
        ttk.Button(top, text="Copy stats", command=self.copy_selected_stats).pack(side="left", padx=(18, 0))

        body = ttk.Panedwindow(self, orient="horizontal")
        body.pack(fill="both", expand=True, padx=8, pady=8)

        left = ttk.Frame(body)
        right = ttk.Frame(body)
        body.add(left, weight=3)
        body.add(right, weight=2)

        # Left: table
        table_frame = ttk.LabelFrame(left, text="Story lines", padding=6)
        table_frame.pack(fill="both", expand=True)

        columns = ("row", "offset", "length", "visible", "controls", "budget", "preview")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=24)
        self.tree.heading("row", text="#")
        self.tree.heading("offset", text="Offset")
        self.tree.heading("length", text="Len (bytes)")
        self.tree.heading("visible", text="Visible")
        self.tree.heading("controls", text="Controls")
        self.tree.heading("budget", text="Est. chars")
        self.tree.heading("preview", text="Japanese / source preview")

        self.tree.column("row", width=60, anchor="e", stretch=False)
        self.tree.column("offset", width=110, anchor="w", stretch=False)
        self.tree.column("length", width=90, anchor="e", stretch=False)
        self.tree.column("visible", width=90, anchor="e", stretch=False)
        self.tree.column("controls", width=90, anchor="e", stretch=False)
        self.tree.column("budget", width=90, anchor="e", stretch=False)
        self.tree.column("preview", width=700, anchor="w", stretch=True)

        yscroll = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        xscroll = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=yscroll.set, xscrollcommand=xscroll.set)
        self.tree.pack(side="top", fill="both", expand=True)
        yscroll.pack(side="right", fill="y")
        xscroll.pack(side="bottom", fill="x")

        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # Right: details + editor
        details = ttk.LabelFrame(right, text="Selected line", padding=8)
        details.pack(fill="x")

        grid = ttk.Frame(details)
        grid.pack(fill="x")

        ttk.Label(grid, textvariable=self.offset_var).grid(row=0, column=0, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.len_var).grid(row=0, column=1, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.visible_var).grid(row=1, column=0, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.controls_var).grid(row=1, column=1, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.budget_var).grid(row=2, column=0, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.used_var).grid(row=2, column=1, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.remaining_var).grid(row=3, column=0, sticky="w", padx=(0, 10), pady=2)
        ttk.Label(grid, textvariable=self.raw_var).grid(row=3, column=1, sticky="w", padx=(0, 10), pady=2)

        source_frame = ttk.LabelFrame(right, text="Japanese / source text", padding=8)
        source_frame.pack(fill="both", expand=False, pady=(8, 0))
        self.source_text = tk.Text(source_frame, height=6, wrap="word", undo=False)
        self.source_text.pack(fill="both", expand=True)
        self.source_text.configure(state="disabled")

        trans_frame = ttk.LabelFrame(right, text="Translation estimate", padding=8)
        trans_frame.pack(fill="both", expand=True, pady=(8, 0))

        self.trans_text = tk.Text(trans_frame, height=10, wrap="word", undo=True)
        self.trans_text.pack(fill="both", expand=True)
        self.trans_text.bind("<<Modified>>", self._on_translation_modified)

        bottom = ttk.Frame(right)
        bottom.pack(fill="x", pady=(8, 0))
        ttk.Label(bottom, textvariable=self.tokens_var, justify="left").pack(anchor="w")

        status = ttk.Label(self, textvariable=self.status_var, anchor="w")
        status.pack(fill="x", padx=8, pady=(0, 8))

        self._set_source_text("")
        self.refresh_filtered()

    def open_csv(self) -> None:
        path = filedialog.askopenfilename(
            title="Open CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
        )
        if not path:
            return
        try:
            self.load_csv(Path(path))
        except Exception as exc:
            messagebox.showerror("CSV load failed", f"Could not open CSV:\n{exc}")

    def load_csv(self, path: Path) -> None:
        self.csv_path = path
        rows: List[LineRow] = []

        with path.open("r", encoding="utf-8-sig", newline="") as f:
            reader = csv.DictReader(f)
            if not reader.fieldnames:
                raise ValueError("CSV has no header row.")

            headers = {h.lower(): h for h in reader.fieldnames}
            required = ["offset_hex", "length_hex", "raw_hex", "decoded", "visible", "controls", "unknown"]
            missing = [col for col in required if col not in headers]
            if missing:
                raise ValueError(
                    "CSV missing expected columns: " + ", ".join(missing)
                )

            for idx, row in enumerate(reader, start=1):
                rows.append(
                    LineRow(
                        row_no=idx,
                        offset_hex=(row.get(headers["offset_hex"], "") or "").strip(),
                        length_hex=(row.get(headers["length_hex"], "") or "").strip(),
                        raw_hex=(row.get(headers["raw_hex"], "") or "").strip(),
                        decoded=(row.get(headers["decoded"], "") or "").replace("\r\n", "\n").replace("\r", "\n"),
                        visible=(row.get(headers["visible"], "") or "").replace("\r\n", "\n").replace("\r", "\n"),
                        controls=(row.get(headers["controls"], "") or "").strip(),
                        unknown=(row.get(headers["unknown"], "") or "").strip(),
                    )
                )

        self.rows = rows
        self.status_var.set(f"Loaded {len(rows)} rows from {path.name}")
        self.refresh_filtered()
        if self.filtered_rows:
            self.tree.selection_set(self.tree.get_children()[0])
            self.tree.focus(self.tree.get_children()[0])
            self.tree.see(self.tree.get_children()[0])
            self.on_select()

    def refresh_filtered(self) -> None:
        query = self.search_var.get().strip().lower()
        if not query:
            self.filtered_rows = list(self.rows)
        else:
            self.filtered_rows = [
                r for r in self.rows
                if query in r.decoded.lower()
                or query in r.visible.lower()
                or query in r.raw_hex.lower()
                or query in r.offset_hex.lower()
            ]

        for item in self.tree.get_children():
            self.tree.delete(item)

        for r in self.filtered_rows:
            preview = strip_controls_preview(r.visible_text or r.decoded)
            if len(preview) > 80:
                preview = preview[:80] + "…"
            self.tree.insert(
                "",
                "end",
                iid=str(r.row_no),
                values=(
                    r.row_no,
                    r.offset_hex,
                    r.length_bytes,
                    r.visible_count,
                    r.control_count,
                    r.budget_chars_est,
                    preview,
                ),
            )

        self.status_var.set(
            f"Showing {len(self.filtered_rows)} of {len(self.rows)} lines"
            + (f" | {self.csv_path.name}" if self.csv_path else "")
        )
        if self.filtered_rows:
            first = self.tree.get_children()[0]
            self.tree.selection_set(first)
            self.tree.focus(first)
            self.tree.see(first)
            self.on_select()
        else:
            self._set_source_text("")
            self._clear_detail_labels()

    def get_selected_row(self) -> Optional[LineRow]:
        sel = self.tree.selection()
        if not sel:
            return None
        iid = sel[0]
        try:
            row_no = int(iid)
        except ValueError:
            return None
        for r in self.rows:
            if r.row_no == row_no:
                return r
        return None

    def on_select(self, event: Optional[tk.Event] = None) -> None:
        row = self.get_selected_row()
        if row is None:
            return
        self._show_row(row)

    def _show_row(self, row: LineRow) -> None:
        self.offset_var.set(f"Offset: {row.offset_hex}")
        self.len_var.set(f"Length: {row.length_hex} ({row.length_bytes} bytes)")
        self.visible_var.set(f"Visible chars: {row.visible_count}")
        self.controls_var.set(f"Controls: {row.control_count}")
        self.budget_var.set(f"Budget: ~{row.budget_chars_est} ASCII chars / {row.length_bytes} bytes")

        preview = row.visible_text or row.decoded
        self._set_source_text(preview)

        self.raw_var.set(f"Raw hex: {row.raw_hex[:120]}{'…' if len(row.raw_hex) > 120 else ''}")

        # Preserve whatever the user typed when switching lines only if box is empty.
        current = self.trans_text.get("1.0", "end-1c")
        if not current.strip():
            self.trans_text.delete("1.0", "end")
            self.trans_text.insert("1.0", preview)
        self._update_selected_estimate()

    def _clear_detail_labels(self) -> None:
        self.offset_var.set("Offset: —")
        self.len_var.set("Length: —")
        self.visible_var.set("Visible chars: —")
        self.controls_var.set("Controls: —")
        self.budget_var.set("Budget: —")
        self.used_var.set("Used: —")
        self.remaining_var.set("Remaining: —")
        self.raw_var.set("Raw hex: —")
        self.tokens_var.set("Tokens: —")

    def _set_source_text(self, value: str) -> None:
        self.source_text.configure(state="normal")
        self.source_text.delete("1.0", "end")
        self.source_text.insert("1.0", value)
        self.source_text.configure(state="disabled")

    def _on_translation_modified(self, event: tk.Event) -> None:
        if self.trans_text.edit_modified():
            self.trans_text.edit_modified(False)
            self._update_selected_estimate()

    def _update_selected_estimate(self) -> None:
        row = self.get_selected_row()
        if row is None:
            return

        text = self.trans_text.get("1.0", "end-1c")
        used_bytes, tokens = estimate_encoded_bytes(
            text,
            append_trailing_space=self.append_space_var.get(),
        )

        remaining = row.length_bytes - used_bytes
        pair_count = (used_bytes // 2)

        self.used_var.set(f"Used: {used_bytes} bytes / {pair_count} tokens")
        if remaining >= 0:
            self.remaining_var.set(f"Remaining: {remaining} bytes")
        else:
            self.remaining_var.set(f"Over budget: {-remaining} bytes")

        token_preview = " | ".join(tokens[:24])
        if len(tokens) > 24:
            token_preview += " | …"
        self.tokens_var.set(f"Tokens: {token_preview if token_preview else '—'}")

    def copy_selected_stats(self) -> None:
        row = self.get_selected_row()
        if row is None:
            return
        text = self.trans_text.get("1.0", "end-1c")
        used_bytes, tokens = estimate_encoded_bytes(text, append_trailing_space=self.append_space_var.get())
        remaining = row.length_bytes - used_bytes
        payload = (
            f"Row: {row.row_no}\n"
            f"Offset: {row.offset_hex}\n"
            f"Budget bytes: {row.length_bytes}\n"
            f"Visible chars: {row.visible_count}\n"
            f"Used bytes: {used_bytes}\n"
            f"Remaining: {remaining}\n"
            f"Translation:\n{text}\n"
            f"Tokens: {' | '.join(tokens)}"
        )
        self.clipboard_clear()
        self.clipboard_append(payload)
        self.status_var.set("Copied stats to clipboard.")

if __name__ == "__main__":
    app = CapacityCheckerApp()
    app.mainloop()
