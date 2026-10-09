import tkinter as tk

from config import (
    APP_NAME, APP_WIDTH, APP_HEIGHT, COLOR_ACCENT, COLOR_BG, COLOR_CARD,
    COLOR_DANGER, COLOR_PRIMARY, COLOR_TEXT, FONT_NAV, HoverButton,
    polish_entries, run_animation,
)
from sidebar import SIDEBAR_EXPANDED, SideBar
from homepage import HomePage
from signup import SignUpPage
from signin import SignInPage
from bookmanagement import BookManagementPage
from borrowingmanagement import BorrowingManagementPage
from usersmanagement import UsersManagementPage


class PerpustakaanApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(APP_NAME)
        self.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        self.resizable(False, False)
        self.configure(bg=COLOR_BG)

        self.current_user = None
        self._nav_target = None
        self._current_frame = None
        self._slide_cancel = None

        self.shell = tk.Frame(self, bg=COLOR_BG)
        self.shell.pack(fill="both", expand=True)

        self.sidebar = SideBar(self.shell, self, on_width=self._sync_sidebar_width)

        self.header = tk.Frame(self.shell, bg=COLOR_CARD, height=60)
        self.header.pack_propagate(False)
        self.header_title = tk.Label(
            self.header, text=APP_NAME, bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 15, "bold"),
        )
        self.header_title.pack(side="left", padx=24)
        HoverButton(
            self.header, bg_normal=COLOR_DANGER, bg_hover="#a93226",
            text="Logout", fg="white", font=FONT_NAV, bd=0,
            padx=16, pady=7, cursor="hand2", command=self.logout,
        ).pack(side="right", padx=20, pady=12)
        self.user_label = tk.Label(
            self.header, text="", bg=COLOR_CARD, fg=COLOR_TEXT, font=FONT_NAV,
        )
        self.user_label.pack(side="right", padx=(0, 6))

        self.container = tk.Frame(self.shell, bg=COLOR_BG)
        self.container.place(x=0, y=0, relwidth=1, relheight=1)

        self.frames = {}
        for PageClass in (
            HomePage, SignUpPage, SignInPage,
            BookManagementPage, BorrowingManagementPage, UsersManagementPage,
        ):
            page_name = PageClass.__name__
            frame = PageClass(parent=self.container, controller=self)
            self.frames[page_name] = frame

        polish_entries(self.container)
        self._update_auth_layout()
        self.show_frame("HomePage")

    def _sync_sidebar_width(self, width: int):
        if not self.current_user:
            return
        self.header.place_configure(x=width, relwidth=1, width=-width)
        self.container.place_configure(x=width, relwidth=1, width=-width)

    def _update_auth_layout(self):
        if self.current_user:
            width = self.sidebar._width
            self.sidebar.place(x=0, y=0, width=width, relheight=1)
            self.header.place(x=width, y=0, relwidth=1, width=-width, height=60)
            self.container.place(
                x=width, y=60, relwidth=1, width=-width,
                relheight=1, height=-60,
            )
            self.user_label.config(text=f"Username: {self.current_user}")
            self.sidebar.refresh()
        else:
            self.sidebar.place_forget()
            self.header.place_forget()
            self.container.place(x=0, y=0, relwidth=1, relheight=1, width=0, height=0)

    def show_frame(self, page_name: str):
        self._nav_target = page_name
        frame = self.frames[page_name]
        if hasattr(frame, "on_show"):
            frame.on_show()
        if self._nav_target != page_name:
            return
        self._slide_in(frame)
        if self.current_user:
            self.sidebar.set_active(page_name)

    def _slide_in(self, frame):
        if self._slide_cancel:
            self._slide_cancel()
            self._slide_cancel = None

        if self._current_frame is frame:
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            frame.tkraise()
            return

        start_x = 28
        frame.place(x=start_x, y=0, relwidth=1, relheight=1)
        frame.tkraise()
        self._current_frame = frame

        def on_frame(t):
            frame.place(x=int(round(start_x * (1 - t))), y=0, relwidth=1, relheight=1)

        def done():
            frame.place(x=0, y=0, relwidth=1, relheight=1)
            for other in self.frames.values():
                if other is not frame:
                    other.place_forget()
            self._slide_cancel = None

        self._slide_cancel = run_animation(frame, 220, on_frame, done)

    def set_current_user(self, username: str):
        self.current_user = username
        self._update_auth_layout()

    def login_success(self, username: str):
        self.set_current_user(username)

        welcome = tk.Frame(self.shell, bg=COLOR_PRIMARY)
        welcome.place(x=0, y=0, relwidth=1, relheight=1)
        welcome.tkraise()
        card = tk.Frame(welcome, bg=COLOR_PRIMARY)
        card.place(relx=0.5, rely=0.54, anchor="center")
        tk.Label(
            card, text="Selamat datang kembali,", bg=COLOR_PRIMARY,
            fg="#bdc3c7", font=("Segoe UI", 15),
        ).pack()
        tk.Label(
            card, text=username, bg=COLOR_PRIMARY, fg="white",
            font=("Segoe UI", 30, "bold"),
        ).pack(pady=(4, 0))

        def move_card(t):
            card.place_configure(rely=0.54 - (0.04 * t))

        run_animation(welcome, 420, move_card)

        def finish():
            if welcome.winfo_exists():
                welcome.destroy()
            self.show_frame("HomePage")

        welcome.after(1050, finish)

    def logout(self):
        self.current_user = None
        self._update_auth_layout()
        self.show_frame("HomePage")


if __name__ == "__main__":
    app = PerpustakaanApp()
    app.mainloop()
