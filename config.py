import tkinter as tk
import json
import os
import hashlib


APP_WIDTH = 1280
APP_HEIGHT = 720
APP_NAME = "D-Book"

USERS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "users.json")
BOOKS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "books.json")
BORROWINGS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "borrowings.json")


COLOR_PRIMARY = "#2c3e50"
COLOR_ACCENT = "#2980b9"
COLOR_ACCENT_DARK = "#1c5980"
COLOR_BG = "#f4f6f7"
COLOR_CARD = "#ffffff"
COLOR_TEXT = "#2c3e50"
COLOR_MUTED = "#7f8c8d"
COLOR_SUCCESS = "#27ae60"
COLOR_DANGER = "#c0392b"


FONT_TITLE = ("Segoe UI", 26, "bold")
FONT_SUBTITLE = ("Segoe UI", 12)
FONT_NAV = ("Segoe UI", 11, "bold")
FONT_CARD_TITLE = ("Segoe UI", 14, "bold")
FONT_CARD_BODY = ("Segoe UI", 10)
FONT_LABEL = ("Segoe UI", 11)
FONT_BUTTON = ("Segoe UI", 11, "bold")


ARTIKEL_PERPUSTAKAAN = [
    {
        "judul": "5 Rekomendasi Buku Fiksi Bulan Ini",
        "ringkasan": "Temukan lima judul fiksi terbaru yang tersedia di rak perpustakaan "
                     "kami, mulai dari novel misteri hingga fantasi epik.",
        "kategori": "Rekomendasi",
    },
    {
        "judul": "Tips Efektif Membaca Cepat",
        "ringkasan": "Pelajari teknik speed reading sederhana agar kamu bisa menyelesaikan "
                     "lebih banyak buku tanpa kehilangan pemahaman isi bacaan.",
        "kategori": "Tips & Trik",
    },
    {
        "judul": "Jadwal Kunjungan & Jam Operasional",
        "ringkasan": "Perpustakaan buka setiap hari Senin-Sabtu pukul 08.00-16.00. "
                     "Cek jadwal lengkap dan agenda kegiatan bulanan di sini.",
        "kategori": "Pengumuman",
    },
    {
        "judul": "Cara Meminjam Buku Secara Online",
        "ringkasan": "Setelah login, anggota dapat memesan buku secara online dan "
                     "mengambilnya langsung di meja sirkulasi perpustakaan.",
        "kategori": "Panduan",
    },
]


DEFAULT_BOOKS = [
    {"id": 1, "judul": "Laskar Pelangi", "penulis": "Andrea Hirata", "tahun": "2005", "stok": 5},
    {"id": 2, "judul": "Bumi", "penulis": "Tere Liye", "tahun": "2014", "stok": 3},
    {"id": 3, "judul": "Atomic Habits", "penulis": "James Clear", "tahun": "2018", "stok": 4},
]


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def load_users() -> dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_users(users: dict) -> None:
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=2, ensure_ascii=False)


def register_user(username: str, email: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username in users:
        return False, "Username sudah terdaftar. Silakan gunakan username lain."
    for data in users.values():
        if data.get("email", "").lower() == email.lower():
            return False, "Email sudah terdaftar. Silakan gunakan email lain."
    users[username] = {
        "email": email,
        "password": hash_password(password),
    }
    save_users(users)
    return True, "Pendaftaran berhasil! Silakan login."


def verify_login(username: str, password: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "Username tidak ditemukan."
    if users[username]["password"] != hash_password(password):
        return False, "Password salah."
    return True, "Login berhasil!"


def delete_user(username: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "User tidak ditemukan."
    del users[username]
    save_users(users)
    return True, "User berhasil dihapus."


def update_user(old_username: str, new_username: str, email: str, new_password: str = "") -> tuple[bool, str]:
    users = load_users()
    if old_username not in users:
        return False, "User tidak ditemukan."
    if new_username != old_username and new_username in users:
        return False, "Username baru sudah dipakai user lain."
    for uname, data in users.items():
        if uname != old_username and data.get("email", "").lower() == email.lower():
            return False, "Email sudah dipakai user lain."
    record = users.pop(old_username)
    record["email"] = email
    if new_password:
        record["password"] = hash_password(new_password)
    users[new_username] = record
    save_users(users)
    return True, "User berhasil diperbarui."


def load_books() -> list:
    if not os.path.exists(BOOKS_FILE):
        save_books(DEFAULT_BOOKS)
        return list(DEFAULT_BOOKS)
    try:
        with open(BOOKS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_books(books: list) -> None:
    with open(BOOKS_FILE, "w", encoding="utf-8") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)


def get_next_book_id(books: list) -> int:
    if not books:
        return 1
    return max(int(b.get("id", 0)) for b in books) + 1


def add_book(judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    new_id = get_next_book_id(books)
    books.append({"id": new_id, "judul": judul, "penulis": penulis, "tahun": tahun, "stok": stok})
    save_books(books)
    return True, "Buku berhasil ditambahkan."


def update_book(book_id: int, judul: str, penulis: str, tahun: str, stok: int) -> tuple[bool, str]:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["judul"] = judul
            b["penulis"] = penulis
            b["tahun"] = tahun
            b["stok"] = stok
            save_books(books)
            return True, "Buku berhasil diperbarui."
    return False, "Buku tidak ditemukan."


def delete_book(book_id: int) -> tuple[bool, str]:
    books = load_books()
    borrowings = load_borrowings()
    for p in borrowings:
        if int(p.get("book_id", 0)) == int(book_id) and p.get("status") == "Dipinjam":
            return False, "Buku tidak bisa dihapus karena sedang dipinjam."
    filtered = [b for b in books if int(b.get("id", 0)) != int(book_id)]
    if len(filtered) == len(books):
        return False, "Buku tidak ditemukan."
    save_books(filtered)
    return True, "Buku berhasil dihapus."


def find_book(book_id: int):
    for b in load_books():
        if int(b.get("id", 0)) == int(book_id):
            return b
    return None


def adjust_book_stock(book_id: int, delta: int) -> bool:
    books = load_books()
    for b in books:
        if int(b.get("id", 0)) == int(book_id):
            b["stok"] = int(b.get("stok", 0)) + delta
            if b["stok"] < 0:
                return False
            save_books(books)
            return True
    return False


def load_borrowings() -> list:
    if not os.path.exists(BORROWINGS_FILE):
        return []
    try:
        with open(BORROWINGS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
            return []
    except (json.JSONDecodeError, OSError):
        return []


def save_borrowings(borrowings: list) -> None:
    with open(BORROWINGS_FILE, "w", encoding="utf-8") as f:
        json.dump(borrowings, f, indent=2, ensure_ascii=False)


def get_next_borrowing_id(borrowings: list) -> int:
    if not borrowings:
        return 1
    return max(int(p.get("id", 0)) for p in borrowings) + 1


def add_borrowing(username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str) -> tuple[bool, str]:
    users = load_users()
    if username not in users:
        return False, "Username tidak terdaftar."
    book = find_book(book_id)
    if book is None:
        return False, "Buku tidak ditemukan."
    if int(book.get("stok", 0)) <= 0:
        return False, "Stok buku habis."
    borrowings = load_borrowings()
    new_id = get_next_borrowing_id(borrowings)
    borrowings.append({
        "id": new_id,
        "username": username,
        "book_id": int(book_id),
        "judul": book.get("judul", ""),
        "tanggal_pinjam": tanggal_pinjam,
        "tanggal_kembali": tanggal_kembali,
        "status": "Dipinjam",
    })
    save_borrowings(borrowings)
    adjust_book_stock(book_id, -1)
    return True, "Peminjaman berhasil ditambahkan."


def update_borrowing(borrow_id: int, username: str, book_id: int, tanggal_pinjam: str, tanggal_kembali: str, status: str) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Data peminjaman tidak ditemukan."
    old_status = target.get("status")
    old_book_id = int(target.get("book_id", 0))
    new_book_id = int(book_id)
    if old_status == "Dipinjam" and status == "Kembali" and old_book_id == new_book_id:
        adjust_book_stock(old_book_id, 1)
    elif old_status == "Kembali" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None:
            return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0:
            return False, "Stok buku habis."
        adjust_book_stock(new_book_id, -1)
    elif old_book_id != new_book_id and old_status == "Dipinjam" and status == "Dipinjam":
        book = find_book(new_book_id)
        if book is None:
            return False, "Buku tidak ditemukan."
        if int(book.get("stok", 0)) <= 0:
            return False, "Stok buku habis."
        adjust_book_stock(old_book_id, 1)
        adjust_book_stock(new_book_id, -1)
    target["username"] = username
    target["book_id"] = new_book_id
    book_now = find_book(new_book_id)
    if book_now is not None:
        target["judul"] = book_now.get("judul", target.get("judul", ""))
    target["tanggal_pinjam"] = tanggal_pinjam
    target["tanggal_kembali"] = tanggal_kembali
    target["status"] = status
    save_borrowings(borrowings)
    return True, "Data peminjaman berhasil diperbarui."


def delete_borrowing(borrow_id: int) -> tuple[bool, str]:
    borrowings = load_borrowings()
    target = None
    for p in borrowings:
        if int(p.get("id", 0)) == int(borrow_id):
            target = p
            break
    if target is None:
        return False, "Data peminjaman tidak ditemukan."
    if target.get("status") == "Dipinjam":
        adjust_book_stock(int(target.get("book_id", 0)), 1)
    filtered = [p for p in borrowings if int(p.get("id", 0)) != int(borrow_id)]
    save_borrowings(filtered)
    return True, "Data peminjaman berhasil dihapus."


def ease_out_cubic(t: float) -> float:
    t = max(0.0, min(1.0, t))
    return 1 - (1 - t) ** 3


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(
        max(0, min(255, int(rgb[0]))),
        max(0, min(255, int(rgb[1]))),
        max(0, min(255, int(rgb[2]))),
    )


def lerp_color(start: str, end: str, t: float) -> str:
    sr, sg, sb = hex_to_rgb(start)
    er, eg, eb = hex_to_rgb(end)
    t = max(0.0, min(1.0, t))
    return rgb_to_hex((sr + (er - sr) * t, sg + (eg - sg) * t, sb + (eb - sb) * t))


_REDUCED_MOTION = None


def prefers_reduced_motion() -> bool:
    global _REDUCED_MOTION
    if _REDUCED_MOTION is not None:
        return _REDUCED_MOTION
    _REDUCED_MOTION = False
    try:
        import ctypes
        enabled = ctypes.c_int()
        ok = ctypes.windll.user32.SystemParametersInfoW(0x1042, 0, ctypes.byref(enabled), 0)
        if ok:
            _REDUCED_MOTION = not bool(enabled.value)
    except (AttributeError, OSError):
        _REDUCED_MOTION = False
    return _REDUCED_MOTION


def run_animation(widget, duration_ms: int, on_frame, on_done=None):
    """Jalankan animasi ~60fps. Mengembalikan fungsi untuk membatalkan."""
    if prefers_reduced_motion() or duration_ms <= 0:
        try:
            on_frame(1)
            if on_done:
                on_done()
        except tk.TclError:
            pass
        return lambda: None

    token = {"id": None, "cancelled": False, "step": 0}
    steps = max(1, round(duration_ms / 16))

    def tick():
        if token["cancelled"]:
            return
        try:
            if not widget.winfo_exists():
                return
            token["step"] += 1
            t = ease_out_cubic(token["step"] / steps)
            on_frame(t)
            if token["cancelled"]:
                return
            if token["step"] < steps:
                token["id"] = widget.after(16, tick)
            elif on_done:
                on_done()
        except tk.TclError:
            return

    tick()

    def cancel():
        token["cancelled"] = True
        if token["id"] is not None:
            try:
                widget.after_cancel(token["id"])
            except tk.TclError:
                pass
        token["id"] = None

    return cancel


def pointer_inside(widget) -> bool:
    try:
        x, y = widget.winfo_pointerxy()
        target = widget.winfo_containing(x, y)
    except tk.TclError:
        return False
    while target is not None:
        if target is widget:
            return True
        target = getattr(target, "master", None)
    return False


def bind_group_hover(widget, on_enter, on_leave):
    """Hover yang tidak berkedip saat kursor pindah ke widget anak."""
    state = {"inside": False, "after_id": None}

    def enter(_event=None):
        if state["after_id"] is not None:
            try:
                widget.after_cancel(state["after_id"])
            except tk.TclError:
                pass
            state["after_id"] = None
        if not state["inside"]:
            state["inside"] = True
            on_enter()

    def leave(_event=None):
        def check():
            state["after_id"] = None
            if pointer_inside(widget):
                return
            if state["inside"]:
                state["inside"] = False
                on_leave()

        if state["after_id"] is not None:
            try:
                widget.after_cancel(state["after_id"])
            except tk.TclError:
                pass
        try:
            state["after_id"] = widget.after(20, check)
        except tk.TclError:
            pass

    def walk(node):
        node.bind("<Enter>", enter, add="+")
        node.bind("<Leave>", leave, add="+")
        for child in node.winfo_children():
            walk(child)

    walk(widget)


def bind_hover_option(widget, option: str, normal: str, hover: str, duration: int = 160):
    state = {"cancel": None, "value": 0.0}

    def go(target):
        if state["cancel"]:
            state["cancel"]()
        start_t = state["value"]

        def on_frame(t):
            state["value"] = start_t + (target - start_t) * t
            widget.configure(**{option: lerp_color(normal, hover, state["value"])})

        state["cancel"] = run_animation(widget, duration, on_frame)

    widget.bind("<Enter>", lambda _e: go(1), add="+")
    widget.bind("<Leave>", lambda _e: go(0), add="+")

    def _cleanup(_e=None):
        if state["cancel"]:
            state["cancel"]()

    widget.bind("<Destroy>", _cleanup, add="+")


def attach_entry_motion(entry: tk.Entry, base: str = "#dfe6e9", focus: str = COLOR_ACCENT):
    entry.configure(
        highlightthickness=1, highlightbackground=base, highlightcolor=base,
        bd=0, relief="flat", insertbackground=COLOR_TEXT,
    )
    state = {"cancel": None, "color": base}

    def paint(color: str):
        state["color"] = color
        entry.configure(highlightbackground=color, highlightcolor=color)

    def go(target: str):
        if state["cancel"]:
            state["cancel"]()
        start = state["color"]

        def on_frame(t):
            paint(lerp_color(start, target, t))

        state["cancel"] = run_animation(entry, 160, on_frame)

    entry.bind("<FocusIn>", lambda _e: go(focus), add="+")
    entry.bind("<FocusOut>", lambda _e: go(base), add="+")
    entry.bind("<Destroy>", lambda _e: state["cancel"] and state["cancel"](), add="+")


def polish_entries(root):
    if root.winfo_class() == "Entry":
        attach_entry_motion(root)
    for child in root.winfo_children():
        polish_entries(child)


def pulse_highlight(widget, color=COLOR_ACCENT, base="#dfe6e9", duration: int = 320):
    def on_frame(t):
        import math
        peak = math.sin(max(0.0, min(1.0, t)) * math.pi)
        widget.configure(highlightbackground=lerp_color(base, color, peak))

    return run_animation(widget, duration, on_frame)


class HoverButton(tk.Button):
    def __init__(self, master, bg_normal, bg_hover, **kwargs):
        super().__init__(master, bg=bg_normal, activebackground=bg_hover, **kwargs)
        self.bg_normal = bg_normal
        self.bg_hover = bg_hover
        self._hover_value = 0.0
        self._hover_cancel = None
        self.bind("<Enter>", self._hover_in, add="+")
        self.bind("<Leave>", self._hover_out, add="+")
        self.bind("<Destroy>", self._cancel_hover, add="+")

    def _cancel_hover(self, _event=None):
        if self._hover_cancel:
            self._hover_cancel()
            self._hover_cancel = None

    def _animate_hover(self, target: float):
        self._cancel_hover()
        start = self._hover_value

        def on_frame(t):
            self._hover_value = start + (target - start) * t
            self.configure(bg=lerp_color(self.bg_normal, self.bg_hover, self._hover_value))

        self._hover_cancel = run_animation(self, 160, on_frame)

    def _hover_in(self, _event=None):
        if str(self.cget("state")) == "disabled":
            return
        self._animate_hover(1)

    def _hover_out(self, _event=None):
        if str(self.cget("state")) == "disabled":
            return
        self._animate_hover(0)
