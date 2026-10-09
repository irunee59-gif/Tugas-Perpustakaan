import tkinter as tk

from config import (
    APP_NAME, COLOR_PRIMARY, COLOR_ACCENT, COLOR_ACCENT_DARK,
    FONT_NAV, bind_group_hover, lerp_color, run_animation,
)


SIDEBAR_EXPANDED = 236
SIDEBAR_COLLAPSED = 72


class Glyph(tk.Canvas):
    def __init__(self, parent, kind: str, bg: str, fg: str = "white"):
        super().__init__(
            parent, width=24, height=24, bg=bg, highlightthickness=0, bd=0,
        )
        self.kind = kind
        self._fg = fg
        self._draw()

    def set_bg(self, bg: str):
        self.configure(bg=bg)

    def _draw(self):
        c = self
        fg = self._fg
        if self.kind == "menu":
            for y in (6, 12, 18):
                c.create_line(4, y, 20, y, fill=fg, width=2, capstyle="round")
        elif self.kind == "home":
            c.create_polygon(
                12, 3, 22, 12, 18, 12, 18, 21, 6, 21, 6, 12, 2, 12,
                fill=fg, outline=fg,
            )
        elif self.kind == "book":
            c.create_line(12, 4, 12, 20, fill=fg, width=2)
            c.create_line(12, 4, 4, 7, 4, 20, 12, 17, fill=fg, width=2)
            c.create_line(12, 4, 20, 7, 20, 20, 12, 17, fill=fg, width=2)
        elif self.kind == "borrow":
            c.create_line(5, 8, 16, 8, fill=fg, width=2, arrow="last", capstyle="round")
            c.create_line(19, 16, 8, 16, fill=fg, width=2, arrow="last", capstyle="round")
        elif self.kind == "users":
            c.create_oval(8, 3, 16, 11, outline=fg, width=2)
            c.create_arc(4, 12, 20, 26, start=0, extent=180, style="arc", outline=fg, width=2)
        elif self.kind == "login":
            c.create_rectangle(3, 4, 13, 20, outline=fg, width=2)
            c.create_line(11, 12, 21, 12, fill=fg, width=2, arrow="last")
        elif self.kind == "signup":
            c.create_oval(3, 3, 11, 11, outline=fg, width=2)
            c.create_line(15, 7, 22, 7, fill=fg, width=2)
            c.create_line(19, 4, 19, 10, fill=fg, width=2)
            c.create_arc(2, 12, 14, 24, start=0, extent=180, style="arc", outline=fg, width=2)
        elif self.kind == "logout":
            c.create_rectangle(11, 4, 21, 20, outline=fg, width=2)
            c.create_line(13, 12, 3, 12, fill=fg, width=2, arrow="last")


class NavButton(tk.Frame):
    def __init__(
        self, parent, text: str, kind: str, command, page: str | None = None,
        normal: str = COLOR_PRIMARY, hover: str = "#34495e",
        active: str = COLOR_ACCENT, active_hover: str = COLOR_ACCENT_DARK,
    ):
        super().__init__(parent, bg=normal, cursor="hand2")
        self.page = page
        self.command = command
        self.normal = normal
        self.hover = hover
        self.active_color = active
        self.active_hover = active_hover
        self.is_active = False
        self._bg = normal
        self._cancel = None
        self._collapsed = False
        self._tip_after = None

        self.icon = Glyph(self, kind, normal)
        self.icon.pack(side="left", padx=(12, 10), pady=10)
        self.label = tk.Label(
            self, text=text, bg=normal, fg="white", font=FONT_NAV, anchor="w",
        )
        self.label.pack(side="left", fill="x", expand=True, pady=10, padx=(0, 12))

        self.pack(fill="x", padx=10, pady=3)
        self._bind_tree(self)
        bind_group_hover(self, self._on_enter, self._on_leave)
        self.bind("<Destroy>", self._on_destroy, add="+")

    def _bind_tree(self, node):
        node.bind("<Button-1>", self._activate, add="+")
        try:
            node.configure(cursor="hand2")
        except tk.TclError:
            pass
        for child in node.winfo_children():
            self._bind_tree(child)

    def _on_destroy(self, _event=None):
        if self._cancel:
            self._cancel()
            self._cancel = None
        self._hide_tip()

    def _activate(self, _event=None):
        self._hide_tip()
        if self.command:
            self.command()

    def _target(self, hovering: bool) -> str:
        if self.is_active:
            return self.active_hover if hovering else self.active_color
        return self.hover if hovering else self.normal

    def _on_enter(self):
        self._tween(self._target(True))
        self._schedule_tip()

    def _on_leave(self):
        self._tween(self._target(False))
        self._hide_tip()

    def set_active(self, active: bool, animate: bool = True):
        self.is_active = active
        self._tween(self._target(False), animate=animate)

    def set_collapsed(self, collapsed: bool):
        self._collapsed = collapsed
        if collapsed:
            self.label.pack_forget()
            self.icon.pack_forget()
            self.icon.pack(pady=10)
            self.pack_configure(padx=8)
        else:
            self.icon.pack_forget()
            self.icon.pack(side="left", padx=(12, 10), pady=10)
            if not self.label.winfo_manager():
                self.label.pack(side="left", fill="x", expand=True, pady=10, padx=(0, 12))
            self.pack_configure(padx=10)
        self._hide_tip()

    def set_bg(self, color: str):
        self._bg = color
        self.configure(bg=color)
        self.label.configure(bg=color)
        self.icon.set_bg(color)

    def _tween(self, target: str, animate: bool = True):
        if self._cancel:
            self._cancel()
            self._cancel = None
        start = self._bg
        if not animate or start == target:
            self.set_bg(target)
            return

        def on_frame(t):
            self.set_bg(lerp_safe(start, target, t))

        self._cancel = run_animation(self, 160, on_frame)

    def _schedule_tip(self):
        self._hide_tip()
        if not self._collapsed:
            return
        try:
            self._tip_after = self.after(380, self._show_tip)
        except tk.TclError:
            pass

    def _show_tip(self):
        self._tip_after = None
        if not self._collapsed or not self.winfo_exists():
            return
        tip = tk.Toplevel(self)
        tip.overrideredirect(True)
        tip.attributes("-topmost", True)
        tk.Label(
            tip, text=self.label.cget("text"), bg=COLOR_PRIMARY, fg="white",
            font=FONT_NAV, padx=10, pady=6,
        ).pack()
        tip.update_idletasks()
        x = self.winfo_rootx() + self.winfo_width() + 8
        y = self.winfo_rooty() + (self.winfo_height() - tip.winfo_height()) // 2
        tip.geometry(f"+{x}+{y}")
        self._tip = tip

    def _hide_tip(self):
        if self._tip_after is not None:
            try:
                self.after_cancel(self._tip_after)
            except tk.TclError:
                pass
            self._tip_after = None
        tip = getattr(self, "_tip", None)
        if tip is not None:
            try:
                tip.destroy()
            except tk.TclError:
                pass
            self._tip = None


def lerp_safe(start: str, end: str, t: float) -> str:
    return lerp_color(start, end, t)


class SideBar(tk.Frame):
    def __init__(self, parent, controller, on_width=None):
        super().__init__(parent, bg=COLOR_PRIMARY, width=SIDEBAR_EXPANDED, height=720)
        self.controller = controller
        self.on_width = on_width
        self.pack_propagate(False)
        self.grid_propagate(False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.expanded = True
        self._width = SIDEBAR_EXPANDED
        self._collapsed_look = False
        self._cancel_width = None
        self.active_page = None
        self._items: list[NavButton] = []
        self.caption = None
        self.user_name = None

        self.header = tk.Frame(self, bg=COLOR_PRIMARY, height=68)
        self.header.grid(row=0, column=0, sticky="ew")
        self.header.pack_propagate(False)
        self.header.grid_propagate(False)

        self.toggle = tk.Frame(self.header, bg=COLOR_PRIMARY, width=40, height=40, cursor="hand2")
        self.toggle.pack(side="left", padx=(14, 4), pady=14)
        self.toggle.pack_propagate(False)
        self.toggle_icon = Glyph(self.toggle, "menu", COLOR_PRIMARY)
        self.toggle_icon.place(relx=0.5, rely=0.5, anchor="center")
        self.toggle_icon.configure(cursor="hand2")
        for node in (self.toggle, self.toggle_icon):
            node.bind("<Button-1>", lambda _e: self.toggle_sidebar())
        bind_group_hover(self.toggle, self._toggle_in, self._toggle_out)
        self._toggle_bg = COLOR_PRIMARY
        self._toggle_cancel = None

        self.logo = tk.Label(
            self.header, text=APP_NAME, bg=COLOR_PRIMARY, fg="white",
            font=("Segoe UI", 16, "bold"),
        )
        self.logo.pack(side="left", padx=(6, 0))

        self.menu = tk.Frame(self, bg=COLOR_PRIMARY)
        self.menu.grid(row=1, column=0, sticky="nsew", pady=(6, 0))

        self.footer = tk.Frame(self, bg=COLOR_PRIMARY)
        self.footer.grid(row=2, column=0, sticky="ew", pady=(0, 12))

        self.refresh()

    def _toggle_in(self):
        self._tween_toggle("#34495e")

    def _toggle_out(self):
        self._tween_toggle(COLOR_PRIMARY)

    def _tween_toggle(self, target: str):
        if self._toggle_cancel:
            self._toggle_cancel()
        start = self._toggle_bg

        def on_frame(t):
            color = lerp_safe(start, target, t)
            self._toggle_bg = color
            self.toggle.configure(bg=color)
            self.toggle_icon.set_bg(color)

        self._toggle_cancel = run_animation(self.toggle, 160, on_frame)

    def toggle_sidebar(self):
        self.expanded = not self.expanded
        target = SIDEBAR_EXPANDED if self.expanded else SIDEBAR_COLLAPSED
        if self._cancel_width:
            self._cancel_width()
            self._cancel_width = None

        if not self.expanded:
            self._set_collapsed_look(True)
        self._apply_sidebar_width(target)
        if self.on_width:
            self.on_width(target)
        if self.expanded:
            self._set_collapsed_look(target == SIDEBAR_COLLAPSED)

    def _apply_sidebar_width(self, width: int):
        self._width = width
        self.configure(width=width)
        self.place_configure(width=width)

    def _set_collapsed_look(self, collapsed: bool):
        if collapsed == self._collapsed_look:
            return
        self._collapsed_look = collapsed
        if collapsed:
            self.logo.pack_forget()
            self.toggle.pack_configure(padx=(16, 16))
        else:
            if not self.logo.winfo_manager():
                self.logo.pack(side="left", padx=(6, 0))
            self.toggle.pack_configure(padx=(14, 4))
        if self.caption is not None:
            if collapsed:
                self.caption.pack_forget()
            elif not self.caption.winfo_manager():
                self._pack_caption()
        for item in self._items:
            item.set_collapsed(collapsed)
        if collapsed:
            if self.user_name is not None and self.user_name.winfo_manager():
                self.user_name.pack_forget()
        elif self.user_name is not None and not self.user_name.winfo_manager():
            self.user_name.pack(side="left")

    def refresh(self):
        for child in self.menu.winfo_children():
            child.destroy()
        for child in self.footer.winfo_children():
            child.destroy()
        self._items = []
        self.caption = None
        self.user_name = None

        self.caption = tk.Label(
            self.menu, text="MENU", bg=COLOR_PRIMARY, fg="#95a5a6",
            font=("Segoe UI", 8, "bold"),
        )

        links = [
            ("Beranda", "home", "HomePage"),
            ("Buku", "book", "BookManagementPage"),
            ("Peminjaman", "borrow", "BorrowingManagementPage"),
            ("Users", "users", "UsersManagementPage"),
        ]

        for text, kind, page in links:
            item = NavButton(
                self.menu, text, kind,
                command=lambda p=page: self.controller.show_frame(p),
                page=page,
            )
            item.set_collapsed(self._collapsed_look)
            self._items.append(item)

        if not self._collapsed_look:
            self._pack_caption()

        if self.active_page:
            self.set_active(self.active_page, animate=False)

    def _pack_caption(self):
        if self.caption is None:
            return
        menu_items = [item for item in self._items if item.master is self.menu]
        if menu_items:
            self.caption.pack(anchor="w", padx=22, pady=(4, 6), before=menu_items[0])
        else:
            self.caption.pack(anchor="w", padx=22, pady=(4, 6))

    def set_active(self, page_name: str, animate: bool = True):
        self.active_page = page_name
        for item in self._items:
            item.set_active(item.page == page_name, animate=animate)
