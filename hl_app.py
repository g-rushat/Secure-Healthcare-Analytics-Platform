import sqlite3
from pathlib import Path
import base64
import hashlib
import hmac
import secrets
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import math

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# ================= CONFIG =================

PROJECT_DIR = Path(__file__).parent
DATA_DIR = PROJECT_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
DB_PATH = DATA_DIR / "app.db"

HASH_NAME = "sha256"
ITERATIONS = 200_000
SALT_BYTES = 16
KEY_LEN = 32

# ================= DATABASE =================

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password_hash TEXT,
            salt TEXT
        )
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            created_at TEXT,
            bmi REAL,
            ffmi REAL,
            bodyfat REAL,
            vo2max REAL
        )
    """)

    conn.commit()
    conn.close()

# ================= AUTH =================

def _hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac(
        HASH_NAME,
        password.encode(),
        salt,
        ITERATIONS,
        dklen=KEY_LEN
    )


def create_user(username, password):
    salt = secrets.token_bytes(SALT_BYTES)
    pwd_hash = _hash(password, salt)
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password_hash, salt) VALUES (?, ?, ?)",
        (
            username,
            base64.b64encode(pwd_hash).decode(),
            base64.b64encode(salt).decode(),
        ),
    )
    conn.commit()
    conn.close()


def verify_user(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE username = ?", (username,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    salt = base64.b64decode(row["salt"])
    expected = base64.b64decode(row["password_hash"])
    candidate = _hash(password, salt)
    if hmac.compare_digest(expected, candidate):
        return dict(row)
    return None

# ================= CALCULATORS =================

def bmi(weight, height_m):
    return weight / (height_m ** 2)


def bodyfat_us_navy_male(height_cm, neck, waist):
    return 86.01 * math.log10(waist - neck) - 70.041 * math.log10(height_cm) + 36.76


def ffmi(weight, height_m, bodyfat_pct):
    lean = weight * (1 - bodyfat_pct / 100)
    return lean / (height_m ** 2)


def vo2max_cooper(distance_m):
    return (distance_m - 504.9) / 44.73


def bmr_mifflin(weight, height_cm, age, sex):
    s = 5 if sex == "M" else -161
    return 10 * weight + 6.25 * height_cm - 5 * age + s


def tdee(bmr, activity):
    return bmr * activity

# ================= APP =================

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Healthcare App")
        self.geometry("1000x600")
        self.user = None

        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (Login, Register, Dashboard, FitnessCalc, AccessoryCalc, History):
            frame = F(container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("Login")

    def show(self, name):
        self.frames[name].tkraise()

# ================= UI =================

class Login(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Login", font=(None, 18)).pack(pady=10)
        tk.Label(self, text="Username").pack()
        self.u = tk.Entry(self)
        self.u.pack()
        tk.Label(self, text="Password").pack()
        self.p = tk.Entry(self, show="*")
        self.p.pack()

        tk.Button(self, text="Login", command=self.login).pack(pady=6)
        tk.Button(self, text="Register", command=lambda: app.show("Register")).pack()

    def login(self):
        user = verify_user(self.u.get(), self.p.get())
        if user:
            self.app.user = user
            self.app.show("Dashboard")
        else:
            messagebox.showerror("Error", "Invalid credentials")


class Register(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Register", font=(None, 18)).pack(pady=10)
        self.u = tk.Entry(self)
        self.p = tk.Entry(self, show="*")
        self.c = tk.Entry(self, show="*")

        tk.Label(self, text="Username").pack(); self.u.pack()
        tk.Label(self, text="Password").pack(); self.p.pack()
        tk.Label(self, text="Confirm Password").pack(); self.c.pack()

        tk.Button(self, text="Create Account", command=self.register).pack(pady=6)
        tk.Button(self, text="Back", command=lambda: app.show("Login")).pack()

    def register(self):
        if self.p.get() != self.c.get():
            messagebox.showerror("Error", "Passwords do not match")
            return
        try:
            create_user(self.u.get(), self.p.get())
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username exists")
            return
        messagebox.showinfo("Success", "Account created")
        self.app.show("Login")


class Dashboard(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        tk.Label(self, text="Dashboard", font=(None, 18)).pack(pady=10)
        tk.Button(self, text="Fitness Calculators", command=lambda: app.show("FitnessCalc")).pack(pady=4)
        tk.Button(self, text="Accessory Calculators", command=lambda: app.show("AccessoryCalc")).pack(pady=4)
        tk.Button(self, text="Historical Graphs", command=lambda: app.show("History")).pack(pady=4)


class FitnessCalc(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Fitness Calculators", font=(None, 16)).pack(pady=8)

        self.h = tk.DoubleVar()
        self.w = tk.DoubleVar()
        self.neck = tk.DoubleVar()
        self.waist = tk.DoubleVar()
        self.dist = tk.DoubleVar()
        self.sex = tk.StringVar(value="M")

        for lbl, var in [
            ("Height (cm)", self.h),
            ("Weight (kg)", self.w),
            ("Neck (cm)", self.neck),
            ("Waist (cm)", self.waist),
            ("Cooper distance (m)", self.dist),
        ]:
            tk.Label(self, text=lbl).pack()
            tk.Entry(self, textvariable=var).pack()

        ttk.Combobox(self, textvariable=self.sex, values=("M", "F"), state="readonly").pack()
        tk.Button(self, text="Compute & Save", command=self.compute).pack(pady=6)
        tk.Button(self, text="Back", command=lambda: app.show("Dashboard")).pack()

        self.out = tk.Text(self, height=6, width=60, state="disabled")
        self.out.pack(pady=6)

    def compute(self):
        h_m = self.h.get() / 100
        bmi_val = bmi(self.w.get(), h_m)
        bf = bodyfat_us_navy_male(self.h.get(), self.neck.get(), self.waist.get()) if self.sex.get() == "M" else None
        ffmi_val = ffmi(self.w.get(), h_m, bf if bf else 25)
        vo2 = vo2max_cooper(self.dist.get()) if self.dist.get() > 0 else None

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO records (user_id, created_at, bmi, ffmi, bodyfat, vo2max)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                self.app.user["id"],
                datetime.now().isoformat(timespec="seconds"),
                bmi_val,
                ffmi_val,
                bf,
                vo2,
            ),
        )
        conn.commit()
        conn.close()

        self.out.config(state="normal")
        self.out.delete("1.0", tk.END)
        self.out.insert(tk.END, f"BMI: {bmi_val:.2f}\nFFMI: {ffmi_val:.2f}\n")
        self.out.insert(tk.END, f"Body Fat %: {bf:.2f}\n" if bf else "")
        self.out.insert(tk.END, f"VO2max: {vo2:.2f}\n" if vo2 else "")
        self.out.config(state="disabled")


class AccessoryCalc(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.age = tk.IntVar()
        self.h = tk.DoubleVar()
        self.w = tk.DoubleVar()
        self.sex = tk.StringVar(value="M")

        tk.Label(self, text="Accessory Calculators", font=(None, 16)).pack(pady=8)
        for lbl, var in [("Age", self.age), ("Height (cm)", self.h), ("Weight (kg)", self.w)]:
            tk.Label(self, text=lbl).pack()
            tk.Entry(self, textvariable=var).pack()

        ttk.Combobox(self, textvariable=self.sex, values=("M", "F"), state="readonly").pack()
        tk.Button(self, text="Compute", command=self.compute).pack(pady=6)
        self.out = tk.Label(self, text="")
        self.out.pack()
        tk.Button(self, text="Back", command=lambda: app.show("Dashboard")).pack()

    def compute(self):
        b = bmr_mifflin(self.w.get(), self.h.get(), self.age.get(), self.sex.get())
        t = tdee(b, 1.55)
        self.out.config(text=f"BMR: {b:.0f} kcal\nTDEE: {t:.0f} kcal")


class History(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app

        tk.Label(self, text="Progress", font=(None, 16)).pack(pady=8)

        self.metric = tk.StringVar(value="bmi")

        ttk.Combobox(
            self,
            textvariable=self.metric,
            values=("bmi", "ffmi", "bodyfat", "vo2max"),
            state="readonly",
        ).pack(pady=4)

        self.fig = Figure(figsize=(6, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        tk.Button(self, text="Refresh", command=self.plot).pack(pady=4)
        tk.Button(self, text="Back", command=lambda: app.show("Dashboard")).pack()

    def plot(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            f"""
            SELECT {self.metric.get()}
            FROM records
            WHERE user_id = ?
              AND {self.metric.get()} IS NOT NULL
            ORDER BY id
            """,
            (self.app.user['id'],),
        )
        rows = cur.fetchall()
        conn.close()

        values = [r[0] for r in rows]

        self.ax.clear()

        if values:
            x = list(range(1, len(values) + 1))
            self.ax.plot(x, values, marker='o')
            self.ax.set_xlim(1, len(values))
        else:
            self.ax.text(
                0.5, 0.5,
                "No data yet",
                ha='center',
                va='center',
                transform=self.ax.transAxes
            )

        self.ax.set_title(f"{self.metric.get().upper()} Progress")
        self.ax.set_xlabel("Entry")
        self.ax.set_ylabel(self.metric.get())

        self.fig.tight_layout()
        self.canvas.draw_idle()

# ================= RUN =================

if __name__ == "__main__":
    init_db()
    App().mainloop()
