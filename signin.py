import tkinter as tk
from tkinter import messagebox
from config import (
    COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD, COLOR_TEXT,
    COLOR_MUTED, FONT_SUBTITLE, FONT_LABEL, FONT_BUTTON, HoverButton,
    verify_login,
)


class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = tk.Frame(self, bg=COLOR_CARD, padx=50, pady=45,
                         highlightthickness=1, highlightbackground="#dfe6e9")
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text="📚 Masuk ke Akun Anda", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 20, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 5), sticky="w")

        tk.Label(
            card, text="Login untuk mengakses layanan perpustakaan",
            bg=COLOR_CARD, fg=COLOR_MUTED, font=FONT_SUBTITLE
        ).grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky="w")

        tk.Label(card, text="Username", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=2, column=0, columnspan=2, sticky="w")
        self.entry_username = tk.Entry(card, font=FONT_LABEL, width=35,
                                        relief="solid", bd=1)
        self.entry_username.grid(row=3, column=0, columnspan=2, pady=(4, 15), ipady=6)

        tk.Label(card, text="Password", bg=COLOR_CARD, fg=COLOR_TEXT,
                 font=FONT_LABEL).grid(row=4, column=0, columnspan=2, sticky="w")
        self.entry_password = tk.Entry(card, font=FONT_LABEL, width=35,
                                        relief="solid", bd=1, show="*")
        self.entry_password.grid(row=5, column=0, columnspan=2, pady=(4, 25), ipady=6)

        self.entry_password.bind("<Return>", lambda e: self.handle_signin())

        HoverButton(
            card, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Masuk", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_signin
        ).grid(row=6, column=0, columnspan=2, sticky="ew", ipady=10)

        bottom_frame = tk.Frame(card, bg=COLOR_CARD)
        bottom_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        tk.Label(bottom_frame, text="Belum punya akun?", bg=COLOR_CARD,
                 fg=COLOR_MUTED, font=FONT_LABEL).pack(side="left")
        link = tk.Label(bottom_frame, text=" Daftar di sini", bg=COLOR_CARD,
                         fg=COLOR_ACCENT, font=("Segoe UI", 11, "bold", "underline"),
                         cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: controller.show_frame("SignUpPage"))

        back_link = tk.Label(card, text="← Kembali ke Beranda", bg=COLOR_CARD,
                              fg=COLOR_MUTED, font=("Segoe UI", 10, "underline"),
                              cursor="hand2")
        back_link.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        back_link.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))

    def handle_signin(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Data belum lengkap", "Mohon isi username dan password.")
            return

        success, message = verify_login(username, password)
        if success:
            self.controller.set_current_user(username)
            messagebox.showinfo("Berhasil", f"{message} Selamat datang, {username}!")
            self.clear_fields()
            self.controller.show_frame("BookManagementPage")
        else:
            messagebox.showerror("Login Gagal", message)

    def clear_fields(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)

    def on_show(self):
        self.clear_fields()