import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUCCESS, COLOR_DANGER,
    FONT_NAV, FONT_LABEL, FONT_BUTTON, HoverButton,
    load_books, load_borrowings, add_borrowing, update_borrowing, delete_borrowing,
)


class BorrowingManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_id = None
        self.book_map = {}

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
            nav_left, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Buku", fg="white", font=FONT_NAV, bd=0, padx=14, pady=6,
            cursor="hand2",
            command=lambda: controller.show_frame("BookManagementPage")
        ).pack(side="left", padx=4)

        HoverButton(
            nav_left, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
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
            content, text="Manajemen Peminjaman",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        form = tk.Frame(body, bg=COLOR_CARD, padx=22, pady=20,
                        highlightthickness=1, highlightbackground="#dfe6e9")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 16))

        tk.Label(form, text="Form Peminjaman", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        tk.Label(form, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=1, column=0, columnspan=2, sticky="w")
        self.entry_username = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_username.grid(row=2, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Buku", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=3, column=0, columnspan=2, sticky="w")
        self.combo_book = ttk.Combobox(form, font=FONT_LABEL, width=28, state="readonly")
        self.combo_book.grid(row=4, column=0, columnspan=2, pady=(4, 10), ipady=2)

        tk.Label(form, text="Tanggal Pinjam (YYYY-MM-DD)", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=5, column=0, columnspan=2, sticky="w")
        self.entry_pinjam = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_pinjam.grid(row=6, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Tanggal Kembali (YYYY-MM-DD)", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=7, column=0, columnspan=2, sticky="w")
        self.entry_kembali = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_kembali.grid(row=8, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Status", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=9, column=0, columnspan=2, sticky="w")
        self.combo_status = ttk.Combobox(form, font=FONT_LABEL, width=28, state="readonly",
                                         values=["Dipinjam", "Kembali"])
        self.combo_status.grid(row=10, column=0, columnspan=2, pady=(4, 16), ipady=2)
        self.combo_status.set("Dipinjam")

        HoverButton(
            form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Tambah", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_add
        ).grid(row=11, column=0, sticky="ew", ipady=7, padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_SUCCESS, bg_hover="#1e8449",
            text="Update", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_update
        ).grid(row=11, column=1, sticky="ew", ipady=7, padx=(5, 0))

        HoverButton(
            form, bg_normal=COLOR_DANGER, bg_hover="#a93226",
            text="Hapus", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_delete
        ).grid(row=12, column=0, sticky="ew", ipady=7, pady=(8, 0), padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_MUTED, bg_hover="#707b7c",
            text="Clear", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.clear_fields
        ).grid(row=12, column=1, sticky="ew", ipady=7, pady=(8, 0), padx=(5, 0))

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

        columns = ("id", "username", "judul", "pinjam", "kembali", "status")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=18)
        self.tree.heading("id", text="ID")
        self.tree.heading("username", text="Username")
        self.tree.heading("judul", text="Judul Buku")
        self.tree.heading("pinjam", text="Tgl Pinjam")
        self.tree.heading("kembali", text="Tgl Kembali")
        self.tree.heading("status", text="Status")
        self.tree.column("id", width=40, anchor="center")
        self.tree.column("username", width=120)
        self.tree.column("judul", width=220)
        self.tree.column("pinjam", width=110, anchor="center")
        self.tree.column("kembali", width=110, anchor="center")
        self.tree.column("status", width=90, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_show(self):
        if not self.controller.current_user:
            self.controller.show_frame("SignInPage")
            return
        self.user_label.config(text="".join(["\U0001F464 ", str(self.controller.current_user)]))
        self.refresh_books()
        self.entry_search.delete(0, tk.END)
        self.clear_fields()
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, str(self.controller.current_user))
        self.refresh_table()

    def refresh_books(self):
        books = load_books()
        labels = []
        self.book_map = {}
        for b in books:
            label = "".join([str(b.get("id", "")), " - ", str(b.get("judul", "")), " (stok:", str(b.get("stok", 0)), ")"])
            labels.append(label)
            self.book_map[label] = int(b.get("id", 0))
        self.combo_book["values"] = labels
        if labels and not self.combo_book.get():
            self.combo_book.set(labels[0])

    def get_selected_book_id(self):
        label = self.combo_book.get()
        return self.book_map.get(label)

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        keyword = self.entry_search.get().strip().lower()
        for p in load_borrowings():
            username = str(p.get("username", ""))
            judul = str(p.get("judul", ""))
            if keyword and keyword not in username.lower() and keyword not in judul.lower():
                continue
            self.tree.insert("", "end", values=(
                p.get("id", ""),
                p.get("username", ""),
                p.get("judul", ""),
                p.get("tanggal_pinjam", ""),
                p.get("tanggal_kembali", ""),
                p.get("status", ""),
            ))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return
        self.selected_id = values[0]
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, values[1])
        for label, bid in self.book_map.items():
            if values[2] in label:
                self.combo_book.set(label)
                break
        self.entry_pinjam.delete(0, tk.END)
        self.entry_pinjam.insert(0, values[3])
        self.entry_kembali.delete(0, tk.END)
        self.entry_kembali.insert(0, values[4])
        self.combo_status.set(values[5])

    def handle_add(self):
        username = self.entry_username.get().strip()
        book_id = self.get_selected_book_id()
        tgl_pinjam = self.entry_pinjam.get().strip()
        tgl_kembali = self.entry_kembali.get().strip()
        if not username or book_id is None or not tgl_pinjam or not tgl_kembali:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom peminjaman.")
            return
        success, message = add_borrowing(username, book_id, tgl_pinjam, tgl_kembali)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.refresh_books()
            self.clear_fields()
            self.entry_username.delete(0, tk.END)
            self.entry_username.insert(0, username)
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_update(self):
        if self.selected_id is None:
            messagebox.showwarning("Belum dipilih", "Pilih data pada tabel terlebih dahulu.")
            return
        username = self.entry_username.get().strip()
        book_id = self.get_selected_book_id()
        tgl_pinjam = self.entry_pinjam.get().strip()
        tgl_kembali = self.entry_kembali.get().strip()
        status = self.combo_status.get().strip()
        if not username or book_id is None or not tgl_pinjam or not tgl_kembali or not status:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom peminjaman.")
            return
        success, message = update_borrowing(self.selected_id, username, book_id, tgl_pinjam, tgl_kembali, status)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.refresh_books()
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Belum dipilih", "Pilih data pada tabel terlebih dahulu.")
            return
        confirm = messagebox.askyesno("Konfirmasi", "Yakin ingin menghapus data ini?")
        if not confirm:
            return
        success, message = delete_borrowing(self.selected_id)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.refresh_books()
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def clear_fields(self):
        self.selected_id = None
        self.entry_pinjam.delete(0, tk.END)
        self.entry_kembali.delete(0, tk.END)
        self.combo_status.set("Dipinjam")
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)