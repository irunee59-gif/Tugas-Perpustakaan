import tkinter as tk
from tkinter import messagebox
from config import (
    APP_NAME, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD, COLOR_TEXT,
    COLOR_MUTED, FONT_SUBTITLE, FONT_LABEL, FONT_BUTTON, HoverButton,
    bind_hover_option, verify_login,
)


class SignInPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        card = tk.Frame(self, bg=COLOR_CARD, padx=50, pady=45,
                         highlightthickness=1, highlightbackground="#dfe6e9")
        card.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(
            card, text=f"Masuk ke {APP_NAME}", bg=COLOR_CARD, fg=COLOR_TEXT,
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

        self.btn_login = HoverButton(
            card, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
            text="Masuk", fg="white", font=FONT_BUTTON, bd=0,
            cursor="hand2", command=self.handle_signin,
            disabledforeground="#bdc3c7",
        )
        self.btn_login.grid(row=6, column=0, columnspan=2, sticky="ew", ipady=10)
        for entry in (self.entry_username, self.entry_password):
            entry.bind("<KeyRelease>", lambda _e: self.update_button_state(), add="+")
        self.update_button_state()

        bottom_frame = tk.Frame(card, bg=COLOR_CARD)
        bottom_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        tk.Label(bottom_frame, text="Belum punya akun?", bg=COLOR_CARD,
                 fg=COLOR_MUTED, font=FONT_LABEL).pack(side="left")
        link = tk.Label(bottom_frame, text=" Daftar di sini", bg=COLOR_CARD,
                         fg=COLOR_ACCENT, font=("Segoe UI", 11, "bold", "underline"),
                         cursor="hand2")
        link.pack(side="left")
        link.bind("<Button-1>", lambda e: controller.show_frame("SignUpPage"))
        bind_hover_option(link, "fg", COLOR_ACCENT, COLOR_ACCENT_DARK)

        back_link = tk.Label(card, text="← Kembali ke Beranda", bg=COLOR_CARD,
                              fg=COLOR_MUTED, font=("Segoe UI", 10, "underline"),
                              cursor="hand2")
        back_link.grid(row=8, column=0, columnspan=2, pady=(15, 0))
        back_link.bind("<Button-1>", lambda e: controller.show_frame("HomePage"))
        bind_hover_option(back_link, "fg", COLOR_MUTED, COLOR_TEXT)

    def handle_signin(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get()

        if not username or not password:
            messagebox.showwarning("Data belum lengkap", "Mohon isi username dan password.")
            return

        success, message = verify_login(username, password)
        if success:
            self.clear_fields()
            self.controller.login_success(username)
        else:
            messagebox.showerror("Login Gagal", message)

    def update_button_state(self):
        complete = bool(self.entry_username.get().strip() and self.entry_password.get())
        self.btn_login.config(state="normal" if complete else "disabled")

    def clear_fields(self):
        self.entry_username.delete(0, tk.END)
        self.entry_password.delete(0, tk.END)
        self.update_button_state()

    def on_show(self):
        self.clear_fields()
