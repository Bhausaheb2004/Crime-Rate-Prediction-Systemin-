import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from PIL import Image, ImageTk
from db import get_db_connection
from db import init_db
init_db()
# ---------------- FILE PATH ---------------- #
DATA_PATH = r"E:/Crime rate Prediction Project  F/Crime rate Prediction Project/data/crime_data_india.csv"

# ---------------- SAVE TO DB ---------------- #
def save_prediction(state, year, value):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        with open("session.txt", "r") as f:
            user_id = int(f.read())
    except:
        user_id = None

    cursor.execute(
        "INSERT INTO predictions (user_id, state, year, predicted_crime) VALUES (%s,%s,%s,%s)",
        (user_id, state, year, int(value))
    )

    conn.commit()
    conn.close()

# ---------------- MAIN APP ---------------- #
class CrimePredictionApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Crime Prediction Dashboard")
        self.root.geometry("900x600")

        # Background
        try:
            img = Image.open(rf"E:/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/crime rate pred.jpg")
            img = img.resize((1500, 1200))
            self.bg = ImageTk.PhotoImage(img)

            bg_label = tk.Label(self.root, image=self.bg)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            bg_label.lower()
        except:
            self.root.configure(bg="#1e1e2f")

        # Title
        tk.Label(root,
                 text="Crime Rate Prediction Dashboard",
                 font=("Arial", 20, "bold"),
                 bg="#1e1e2f",
                 fg="white").pack(pady=10)

        # Load CSV
        try:
            self.df = pd.read_csv(DATA_PATH)
        except Exception as e:
            messagebox.showerror("Error", str(e))
            root.destroy()
            return

        self.states = sorted(self.df["STATE/UT"].dropna().unique())

        # Top Frame
        top_frame = tk.Frame(root, bg="#2c2c3e")
        top_frame.pack(fill="x", pady=10)

        tk.Label(top_frame, text="Select State:",
                 bg="#2c2c3e", fg="white").pack(side="left", padx=10)

        self.combo = ttk.Combobox(top_frame,
                                  values=self.states,
                                  state="readonly",
                                  width=30)
        self.combo.pack(side="left", padx=25)

        tk.Button(top_frame,
                  text="Predict",
                  bg="#4CAF50",
                  fg="white",
                  command=self.run_prediction).pack(side="left", padx=25)

        tk.Button(top_frame,
                  text="Exit",
                  bg="red",
                  fg="white",
                  command=root.destroy).pack(side="left", padx=25)

        # Output
        self.output = tk.Text(root, height=10, width=100)
        self.output.pack(pady=10)

        # Graph Frame
        self.graph_frame = tk.Frame(root)
        self.graph_frame.pack(fill="both", expand=True)

    # ---------------- PREDICTION ---------------- #
    def run_prediction(self):

        state = self.combo.get()

        if not state:
            messagebox.showerror("Error", "Select a state")
            return

        data = self.df[self.df["STATE/UT"] == state].sort_values("YEAR")

        years = data["YEAR"].tolist()
        values = data["TOTAL IPC CRIMES"].values

        last_year = years[-1]
        last_value = values[-1]

        # ✅ 5 YEAR PREDICTION (FIXED)
        future_years = []
        future_values = []

        for i in range(1, 6):
            year = last_year + i
            value = int(last_value + (i * 1000))  # simple growth

            future_years.append(year)
            future_values.append(value)

        # Output
        self.output.delete("1.0", tk.END)

        self.output.insert(tk.END, f"\n📊 {state} Data\n")
        self.output.insert(tk.END, "-"*40 + "\n")

        for y, v in zip(years, values):
            self.output.insert(tk.END, f"{y} - {int(v)} crimes\n")

        self.output.insert(tk.END, "\n🔮 Next 5 Years Prediction\n")
        self.output.insert(tk.END, "-"*40 + "\n")

        for y, v in zip(future_years, future_values):
            self.output.insert(tk.END, f"{y} - {v} crimes\n")
            save_prediction(state, y, v)

        # ---------------- GRAPH ---------------- #
        for widget in self.graph_frame.winfo_children():
            widget.destroy()

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.plot(years, values, marker='o', label="Past Data")
        ax.plot(future_years, future_values, marker='o', linestyle='--', label="Future Prediction")

        ax.set_title(f"Crime Trend - {state}")
        ax.set_xlabel("Year")
        ax.set_ylabel("Crimes")
        ax.legend()
        ax.grid(True)

        canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

# ---------------- MAIN ---------------- #
def main(root):
    app = CrimePredictionApp(root)

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    root = tk.Tk()
    main(root)
    root.mainloop()