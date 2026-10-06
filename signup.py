import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD, COLOR_TEXT,
    COLOR_MUTED, FONT_SUBTITLE, FONT_LABEL, FONT_BUTTON, HoverButton,
    register_user,
)


class SignUpPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = tk.Frame(self, bg=COLOR_CARD, padx=50, pady=40,
                         highlightthickness=1, highlightbackground="#dfe6e9")
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="📚 Buat Akun Baru", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")

        tk.Label(
            card, text="Daftar untuk mulai meminjam buku secara online",
            bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SUBTITLE
        ).grid(row=1, column=0, columnspan=2, pady=(0, 25), sticky="w")

        tk.Label(card, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=2, column=0, columnspan=2, sticky="w")
        self.entry_username = tk.Entry(card, font=FONT_LABEL, width=35,
                                        relief="solid", bd=1)
        self.entry_username.grid(row=3, column=0, columnspan=2, pady=(4, 15), ipady=6)

        tk.Label(card, text="Email", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
        self.entry_email = tk.Entry(card, font=FONT_LABEL, width=35,
                                     relief="solid", bd=1)
        self.entry_email.grid(row=5, column=0, columnspan=2, pady=(4, 15), ipady=6)

        tk.Label(card, text="Password", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=6, column=0, columnspan=2, sticky="w")
        self.entry_password = tk.Entry(card, font=FONT_LABEL, width=35,
                                        relief="solid", bd=1, show="*")
        self.entry_password.grid(row=7, column=0, columnspan=2, pady=(4, 15), ipady=6)

        tk.Label(card, text="Konfirmasi Password", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=8, column=0, columnspan=2, sticky="w")
        self.entry_confirm = tk.Entry(card, font=FONT_LABEL, width=35,
                                       relief="solid", bd=1, show="*")
        self.entry_confirm.grid(row=9, column=0, columnspan=2, pady=(4, 20), ipady=6)

        HoverButton(
            card, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Daftar Sekarang", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_signup
        ).grid(row=10, column=0, columnspan=2, sticky="ew", ipady=10)

        bottom_frame = tk.Frame(card, bg=COLOR_CARD)
        bottom_frame.grid(row=11, column=0, columnspan=2, pady=(20, 0))
        tk.Label(bottom_frame, text="Sudah punya akun?", bg=COLOR_CARD,
                 fg=COLOR_MUTED, font=FONT_LABEL).pack(side="left")
        link = tk.Label(bottom_frame, text=" Login di sini", bg=COLOR_CARD,
                         fg=COLOR_ACCENT, font=("Segoe UI", 11, "bold", "underline"),
                         cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: controller.show_frame("SignInPage"))

        back_link = tk.Label(card, text="← Kembali ke Beranda", bg=COLOR_CARD,
                              fg=COLOR_MUTED, font=("Segoe UI", 10, "underline"),
                              cursor="hand2")
        back_link.grid(row=12, column=0, columnspan=2, pady=(15, 0))
        back_link.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))

    def handle_signup(self):
        username = self.entry_username.get().strip()
        email = self.entry_email.get().strip()
        password = self.entry_password.get()
        confirm = self.entry_confirm.get()

        if not username or not email or not password or not confirm:
            messagebox.showwarning("Data belum lengkap", "Mohon isi semua kolom.")
            return
        if "@" not in email or "." not in email:
            messagebox.showwarning("Email tidak valid", "Masukkan format email yang benar.")
            return
        if len(password) < 6:
            messagebox.showwarning("Password terlalu pendek",
                                    "Password minimal 6 karakter.")
            return
        if password != confirm:
            messagebox.showwarning("Password tidak cocok",
                                    "Konfirmasi password harus sama dengan password.")
            return

        success, message = register_user(username, email, password)
        if success:
            messagebox.showinfo("Berhasil", message)
            self.clear_fields()
            self.controller.show_frame("SignInPage")
        else:
            messagebox.showerror("Gagal Mendaftar", message)

    def clear_fields(self):
        self.entry_username.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.entry_confirm.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()