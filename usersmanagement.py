import tkinter as tk
from tkinter import ttk, messagebox
from config import (
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, COLOR_SUCCESS, COLOR_DANGER,
    FONT_LABEL, FONT_BUTTON, HoverButton, pulse_highlight,
    load_users, register_user, update_user, delete_user,
)


class UsersManagementPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self.selected_old_username = None

        content = tk.Frame(self, bg=COLOR_BG)
        content.pack(fill="both", expand=True, padx=25, pady=18)

        tk.Label(
            content, text="Manajemen Users",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 18, "bold")
        ).pack(anchor="w", pady=(0, 12))

        body = tk.Frame(content, bg=COLOR_BG)
        body.pack(fill="both", expand=True)
        body.grid_columnconfigure(0, weight=0)
        body.grid_columnconfigure(1, weight=1)

        form = tk.Frame(body, bg=COLOR_CARD, padx=22, pady=20,
                        highlightthickness=1, highlightbackground="#dfe6e9")
        form.grid(row=0, column=0, sticky="ns", padx=(0, 16))
        self.form_card = form

        tk.Label(form, text="Form User", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=("Segoe UI", 13, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 12))

        tk.Label(form, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=1, column=0, columnspan=2, sticky="w")
        self.entry_username = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_username.grid(row=2, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Email", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=3, column=0, columnspan=2, sticky="w")
        self.entry_email = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1)
        self.entry_email.grid(row=4, column=0, columnspan=2, pady=(4, 10), ipady=4)

        tk.Label(form, text="Password (kosongkan jika tidak diubah)", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=5, column=0, columnspan=2, sticky="w")
        self.entry_password = tk.Entry(form, font=FONT_LABEL, width=30, relief="solid", bd=1, show="*")
        self.entry_password.grid(row=6, column=0, columnspan=2, pady=(4, 16), ipady=4)

        HoverButton(
            form, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Tambah", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_add
        ).grid(row=7, column=0, sticky="ew", ipady=7, padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_SUCCESS, bg_hover="#1e8449",
            text="Update", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_update
        ).grid(row=7, column=1, sticky="ew", ipady=7, padx=(5, 0))

        HoverButton(
            form, bg_normal=COLOR_DANGER, bg_hover="#a93226",
            text="Hapus", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_delete
        ).grid(row=8, column=0, sticky="ew", ipady=7, pady=(8, 0), padx=(0, 5))

        HoverButton(
            form, bg_normal=COLOR_MUTED, bg_hover="#707b7c",
            text="Clear", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.clear_fields
        ).grid(row=8, column=1, sticky="ew", ipady=7, pady=(8, 0), padx=(5, 0))

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

        columns = ("username", "email")
        self.tree = ttk.Treeview(right, columns=columns, show="headings", height=18)
        self.tree.heading("username", text="Username")
        self.tree.heading("email", text="Email")
        self.tree.column("username", width=140, stretch=True)
        self.tree.column("email", width=220, stretch=True)
        self.tree.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

    def on_show(self):
        if not self.controller.current_user:
            self.controller.show_frame("SignInPage")
            return
        self.clear_fields()
        self.entry_search.delete(0, tk.END)
        self.refresh_table()

    def refresh_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        keyword = self.entry_search.get().strip().lower()
        users = load_users()
        for username in sorted(users.keys()):
            email = str(users[username].get("email", ""))
            if keyword and keyword not in username.lower() and keyword not in email.lower():
                continue
            self.tree.insert("", "end", values=(username, email))

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        if not values:
            return
        self.selected_old_username = values[0]
        pulse_highlight(self.form_card)
        self.entry_username.delete(0, tk.END)
        self.entry_username.insert(0, values[0])
        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, values[1])
        self.entry_password.delete(0, tk.END)

    def handle_add(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        if not username or not email or not password:
            messagebox.showwarning("Data belum lengkap", "Mohon isi username, email, dan password.")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Email tidak valid", "Masukkan format email yang benar.")
            return
        if len(password) < 6:
            messagebox.showwarning("Password terlalu pendek", "Password minimal 6 karakter.")
            return
        success, message = register_user(username, email, password)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_update(self):
        if self.selected_old_username is None:
            messagebox.showwarning("Belum dipilih", "Pilih user pada tabel terlebih dahulu.")
            return
        new_username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        new_password = self.entry_password.get()
        if not new_username or not email:
            messagebox.showwarning("Data belum lengkap", "Mohon isi username dan email.")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Email tidak valid", "Masukkan format email yang benar.")
            return
        if new_password and len(new_password) < 6:
            messagebox.showwarning("Password terlalu pendek", "Password minimal 6 karakter.")
            return
        success, message = update_user(self.selected_old_username, new_username, email, new_password)
        if success:
            if self.controller.current_user == self.selected_old_username:
                self.controller.set_current_user(new_username)
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def handle_delete(self):
        if self.selected_old_username is None:
            messagebox.showwarning("Belum dipilih", "Pilih user pada tabel terlebih dahulu.")
            return
        if self.selected_old_username == self.controller.current_user:
            messagebox.showwarning("Tidak diizinkan", "Tidak bisa menghapus akun yang sedang login.")
            return
        confirm = messagebox.askyesno("Konfirmasi", "".join(["Yakin ingin menghapus user '", self.selected_old_username, "'?"]))
        if not confirm:
            return
        success, message = delete_user(self.selected_old_username)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.refresh_table()
        else:
            messagebox.showerror("Gagal", message)

    def clear_fields(self):
        self.selected_old_username = None
        self.entry_username.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(selection)
