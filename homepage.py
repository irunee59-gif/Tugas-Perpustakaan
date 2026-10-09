import tkinter as tk
from config import (
    APP_NAME, COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK, COLOR_BG, COLOR_CARD,
    COLOR_TEXT, COLOR_MUTED, FONT_TITLE, FONT_SUBTITLE,
    FONT_CARD_TITLE, FONT_CARD_BODY, ARTIKEL_PERPUSTAKAAN,
    HoverButton, bind_group_hover, lerp_color, run_animation,
)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=COLOR_BG)
        self.controller = controller
        self._cards = []

        hero = tk.Frame(self, bg=COLOR_ACCENT, height=180)
        hero.pack(fill="x")
        hero.pack_propagate(False)

        hero_inner = tk.Frame(hero, bg=COLOR_ACCENT)
        hero_inner.pack(expand=True)

        tk.Label(
            hero_inner, text=f"Selamat Datang di {APP_NAME}",
            bg=COLOR_ACCENT, fg="white", font=FONT_TITLE
        ).pack(pady=(30, 5))

        tk.Label(
            hero_inner,
            text="Jelajahi koleksi buku, baca artikel terbaru, dan kelola peminjamanmu di sini.",
            bg=COLOR_ACCENT, fg="#eaf2f8", font=FONT_SUBTITLE,
            wraplength=760, justify="center",
        ).pack()

        self.guest_actions = tk.Frame(hero_inner, bg=COLOR_ACCENT)
        HoverButton(
            self.guest_actions, bg_normal=COLOR_PRIMARY, bg_hover="#34495e",
            text="Login", fg="white", bd=0, padx=18, pady=7,
            cursor="hand2",
            command=lambda: controller.show_frame("SignInPage"),
        ).pack(side="left", padx=5)
        HoverButton(
            self.guest_actions, bg_normal="#ffffff", bg_hover="#eaf2f8",
            text="Sign Up", fg=COLOR_ACCENT_DARK, bd=0, padx=18, pady=7,
            cursor="hand2",
            command=lambda: controller.show_frame("SignUpPage"),
        ).pack(side="left", padx=5)

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
            footer, text=f"© 2026 {APP_NAME} — Semua hak cipta dilindungi.",
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
            font=FONT_CARD_BODY, wraplength=420, justify="left"
        ).pack(anchor="w", padx=18, pady=(6, 18))

        self._bind_card_hover(card)
        self._cards.append(card)

    def _bind_card_hover(self, card):
        normal = "#dfe6e9"
        hover = COLOR_ACCENT
        state = {"cancel": None, "color": normal}

        def go(target):
            if state["cancel"]:
                state["cancel"]()
            start = state["color"]

            def on_frame(t):
                state["color"] = lerp_color(start, target, t)
                card.configure(highlightbackground=state["color"])

            state["cancel"] = run_animation(card, 180, on_frame)

        bind_group_hover(card, lambda: go(hover), lambda: go(normal))

    def on_show(self):
        if self.controller.current_user:
            self.guest_actions.pack_forget()
        elif not self.guest_actions.winfo_manager():
            self.guest_actions.pack(pady=(12, 0))
