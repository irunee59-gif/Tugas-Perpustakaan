import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUCCESS, COLOR_DANGER,
    FONT_NAV, FONT_LABEL, FONT_BUTTON, HoverButton,
    load_books, add_book, update_book, delete_book,
)


class BookManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_id = None

        navbar = tk.Frame(self, bg=COLOR_PRIMARY, height=60)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        tk.Label(
            navbar, text="Perpustakaan Digital",
            bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 14, "bold")
        ).pack(side="left", padx=20)

        nav_left = tk.Frame(navbar, bg=COLOR_PRIMARY)
        nav_left.pack(side="left", padx=10)

        HoverButton(
            nav_left, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Buku", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BookManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Peminjaman", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BorrowingManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Users", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("UsersManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Beranda", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("HomePage")
        ).pack(side="left", padx=4)

        self.nav_right = tk.Frame(navbar, bg=COLOR_PRIMARY)
        self.nav_right.pack(side="right", padx=20)

        self.user_label = tk.Label(
            self.nav_right, text="", bg=COLOR_PRIMARY, fg="white", font=FONT_NAV
        )
        self.user_label.pack(side="left", padx=(0, 12))

        HoverButton(
            self.nav_right, bg_normal="#c0392b", bg_hover="#a93226",
            text="Logout", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2", command=controller.logout
        ).pack(side="left")

        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=25, pady=18)

        tk.Label(
            content, text="Manajemen Buku",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        form = tk.Frame(body, bg=COLOR_CARD, padx=22, pady=20,
                        highlightthickness=1, highlightbackground="#dfe6e9")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 16))

        tk.Label(form, text="Form Buku", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        tk.Label(form, text="Judul", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=1, column=0, columnspan=2, sticky="w")
        self.entry_judul = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_judul.grid(row=2, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Penulis", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=3, column=0, columnspan=2, sticky="w")
        self.entry_penulis = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_penulis.grid(row=4, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Tahun", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=5, column=0, columnspan=2, sticky="w")
        self.entry_tahun = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_tahun.grid(row=6, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Stok", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=7, column=0, columnspan=2, sticky="w")
        self.entry_stok = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_stok.grid(row=8, column=0, columnspan=2, pady=(4, 16), ipady=4)

        HoverButton(
            form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Tambah", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_add
        ).grid(row=9, column=0, sticky="ew", ipady=7, padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_SUCCESS, bg_hover="#1e8449",
            text="Update", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_update
        ).grid(row=9, column=1, sticky="ew", ipady=7, padx=(5, 0))

        HoverButton(
            form, bg_normal=COLOR_DANGER, bg_hover="#a93226",
            text="Hapus", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_delete
        ).grid(row=10, column=0, sticky="ew", ipady=7, pady=(8, 0), padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_MUTED, bg_hover="#707b7c",
            text="Clear", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.clear_fields
        ).grid(row=10, column=1, sticky="ew", ipady=7, pady=(8, 0), padx=(5, 0))

        right = tk.Frame(body, bg=COLOR_CARD,
                         highlightthickness=1, highlightbackground="#dfe6e9")
        right.grid(row=0, column=1, sticky="nsew")
        body.grid_rowconfigure(0, weight=1)

        search_frame = tk.Frame(right, bg=COLOR_CARD)
        search_frame.pack(fill="x", padx=16, pady=(14, 8))

        tk.Label(search_frame, text="Cari:", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).pack(side="left")
        self.entry_search = tk.Entry(search_frame, font=FONT_LABEL, width=28, relief="solid", bd=1)
        self.entry_search.pack(side="left", padx=(8, 8), ipady=3)
        self.entry_search.bind("<KeyRelease>", lambda e: self.refresh_table())

        columns = ("id", "judul", "penulis", "tahun", "stok")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("judul", text="Judul")
        self.tree.heading("penulis", text="Penulis")
        self.tree.heading("tahun", text="Tahun")
        self.tree.heading("stok", text="Stok")
        self.tree.column("id", width=50, anchor="center")
        self.tree.column("judul", width=300)
        self.tree.column("penulis", width=200)
        self.tree.column("tahun", width=80, anchor="center")
        self.tree.column("stok", width=70, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_show(self):
        if not self.controller.current_user:
            self.controller.show_frame("SignInPage")
            return
        self.user_label.config(text="".join(["\U0001F464 ", str(self.controller.current_user)]))
        self.clear_fields()
        self.entry_search.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        keyword = self.entry_search.get().strip().lower()
        for b in load_books():
            judul = str(b.get("judul", ""))
            penulis = str(b.get("penulis", ""))
            if keyword and keyword not in judul.lower() and keyword not in penulis.lower():
                continue
            self.tree.insert("", "end", values=(
                b.get("id", ""),
                b.get("judul", ""),
                b.get("penulis", ""),
                b.get("tahun", ""),
                b.get("stok", ""),
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return
        self.selected_id = values[0]
        self.entry_judul.delete(0, tk.END)
        self.entry_judul.insert(0, values[1])
        self.entry_penulis.delete(0, tk.END)
        self.entry_penulis.insert(0, values[2])
        self.entry_tahun.delete(0, tk.END)
        self.entry_tahun.insert(0, values[3])
        self.entry_stok.delete(0, tk.END)
        self.entry_stok.insert(0, values[4])

    def read_form(self):
        judul = self.entry_judul.get().strip()
        penulis = self.entry_penulis.get().strip()
        tahun = self.entry_tahun.get().strip()
        stok_text = self.entry_stok.get().strip()
        return judul, penulis, tahun, stok_text

    def handle_add(self):
        judul, penulis, tahun, stok_text = self.read_form()
        if not judul or not penulis or not tahun or not stok_text:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom buku.")
            return
        try:
            stok = int(stok_text)
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Stok tidak valid", "Stok harus berupa angka >= 0.")
            return
        success, message = add_book(judul, penulis, tahun, stok)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_update(self):
        if self.selected_id is None:
            messagebox.showwarning("Belum dipilih", "Pilih buku pada tabel terlebih dahulu.")
            return
        judul, penulis, tahun, stok_text = self.read_form()
        if not judul or not penulis or not tahun or not stok_text:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom buku.")
            return
        try:
            stok = int(stok_text)
            if stok < 0:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Stok tidak valid", "Stok harus berupa angka >= 0.")
            return
        success, message = update_book(self.selected_id, judul, penulis, tahun, stok)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Belum dipilih", "Pilih buku pada tabel terlebih dahulu.")
            return
        confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus buku ini?")
        if not confirm:
            return
        success, message = delete_book(self.selected_id)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def clear_fields(self):
        self.selected_id = None
        self.entry_judul.delete(0, tk.END)
        self.entry_penulis.delete(0, tk.END)
        self.entry_tahun.delete(0, tk.END)
        self.entry_stok.delete(0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)