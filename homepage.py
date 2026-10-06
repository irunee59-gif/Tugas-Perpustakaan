import tkinter as tk
from config import (
    COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, FONT_TITLE, FONT_SUBTITLE, FONT_NAV,
    FONT_CARD_TITLE, FONT_CARD_BODY, ARTIKEL_PERPUSTAKAAN, HoverButton,
)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller

        navbar = tk.Frame(self, bg=COLOR_PRIMARY, height=70)
        navbar.pack(fill="x", side="top")
        navbar.pack_propagate(False)

        logo_label = tk.Label(
            navbar, text="Perpustakaan Digital",
            bg=COLOR_PRIMARY, fg="white", font=("Segoe UI", 16, "bold")
        )
        logo_label.pack(side="left", padx=30)

        self.nav_right = tk.Frame(navbar, bg=COLOR_PRIMARY)
        self.nav_right.pack(side="right", padx=30)


        hero = tk.Frame(self, bg=COLOR_ACCENT, height=180)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_inner = tk.Frame(hero, bg=COLOR_ACCENT)
        hero_inner.pack(expand=True)

        tk.Label(
            hero_inner, text="Selamat Datang di Perpustakaan Digital",
            bg=COLOR_ACCENT, fg="white", font=FONT_TITLE
        ).pack(pady=(30, 5))

        tk.Label(
            hero_inner,
            text="Jelajahi koleksi buku, baca artikel terbaru, dan kelola peminjamanmu di sini.",
            bg=COLOR_ACCENT, fg="#eaf2f8", font=FONT_SUBTITLE
        ).pack()

        content_area = tk.Frame(self, bg=COLOR_BG)
        content_area.pack(fill="both", expand=True, padx=40, pady=25)

        tk.Label(
            content_area, text="Artikel & Informasi Terbaru",
            bg=COLOR_BG, fg=COLOR_TEXT, font=("Segoe UI", 16, "bold")
        ).pack(anchor="w", pady=(0, 15))

        cards_frame = tk.Frame(content_area, bg=COLOR_BG)
        cards_frame.pack(fill="both", expand=True)
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)

        for idx, artikel in enumerate(ARTIKEL_PERPUSTAKAAN):
            row, col = divmod(idx, 2)
            self._build_article_card(cards_frame, artikel, row, col)

        footer = tk.Frame(self, bg=COLOR_PRIMARY, height=36)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        tk.Label(
            footer, text="© 2026 Perpustakaan Digital — Semua hak cipta dilindungi.",
            bg=COLOR_PRIMARY, fg="#bdc3c7", font=("Segoe UI", 9)
        ).pack(pady=8)

    def _build_article_card(self, parent, artikel, row, col):
        card = tk.Frame(parent, bg=COLOR_CARD, bd=0, highlightthickness=1,
                         highlightbackground="#dfe6e9")
        card.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

        badge = tk.Label(
            card, text=artikel["kategori"], bg="#eaf2f8", fg=COLOR_ACCENT,
            font=("Segoe UI", 9, "bold"), padx=10, pady=3
        )
        badge.pack(anchor="w", padx=18, pady=(16, 8))

        tk.Label(
            card, text=artikel["judul"], bg=COLOR_CARD, fg=COLOR_TEXT,
            font=FONT_CARD_TITLE, wraplength=480, justify="left"
        ).pack(anchor="w", padx=18)

        tk.Label(
            card, text=artikel["ringkasan"], bg=COLOR_CARD, fg=COLOR_MUTED,
            font=FONT_CARD_BODY, wraplength=480, justify="left"
        ).pack(anchor="w", padx=18, pady=(6, 18))

    def on_show(self):
        for widget in self.nav_right.winfo_children():
            widget.destroy()

        if self.controller.current_user:
            tk.Label(
                self.nav_right, text=f"👤 {self.controller.current_user}",
                bg=COLOR_PRIMARY, fg="white", font=FONT_NAV
            ).pack(side="left", padx=(0, 15))

            HoverButton(
                self.nav_right, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
                text="Dashboard", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("BookManagementPage")
            ).pack(side="left", padx=(0, 10))

            HoverButton(
                self.nav_right, bg_normal="#c0392b", bg_hover="#a93226",
                text="Logout", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2", command=self.controller.logout
            ).pack(side="left")
        else:
            HoverButton(
                self.nav_right, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
                text="Login", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("SignInPage")
            ).pack(side="left", padx=(0, 10))

            HoverButton(
                self.nav_right, bg_normal=COLOR_ACCENT, bg_hover=COLOR_ACCENT_DARK,
                text="Sign Up", fg="white", font=FONT_NAV, bd=0, padx=18, pady=8,
                cursor="hand2",
                command=lambda: self.controller.show_frame("SignUpPage")
            ).pack(side="left")