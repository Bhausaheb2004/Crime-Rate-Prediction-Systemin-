import tkinter as tk
from tkinter import messagebox as ms
import subprocess, sys, os, re
from PIL import Image, ImageTk
from db import init_db, get_db_connection

init_db()

# ---------------- WINDOW ---------------- #
root = tk.Tk()
root.title("Register")
root.geometry("900x600")
root.resizable(False, False)

# ---------------- BACKGROUND IMAGE ---------------- #
try:
    img = Image.open(rf"E:/Crime rate Prediction Project  F/Crime rate Prediction Project/assets/registration img.jpeg")
    img = img.resize((800, 500))
    bg = ImageTk.PhotoImage(img)

    bg_label = tk.Label(root, image=bg)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except:
    root.configure(bg="#F0F2F5")

# ---------------- PLACEHOLDER FUNCTION ---------------- #
def placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="gray")

    def on_focus_in(e):
        if entry.get() == text:
            entry.delete(0, tk.END)
            entry.config(fg="black")

    def on_focus_out(e):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="gray")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# ---------------- VARIABLES ---------------- #
fullname = tk.StringVar()
username = tk.StringVar()
email = tk.StringVar()
phone = tk.StringVar()
password = tk.StringVar()
confirm = tk.StringVar()

# 🔥 FIXED GENDER VARIABLE
gender = tk.StringVar(master=root)

password_visible = False

# ---------------- VALIDATION ---------------- #
def validate_email(mail):
    return re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", mail)

def show_error(label, message):
    label.config(text=message)

def clear_error(label):
    label.config(text="")

# ---------------- REGISTER FUNCTION ---------------- #
def register_user():
    valid = True

    for lbl in error_labels:
        clear_error(lbl)

    # READ VALUES FROM ENTRY
    full = fullname_entry.get().strip()
    user = username_entry.get().strip()
    mail = email_entry.get().strip()
    ph = phone_entry.get().strip()
    pwd = pass_entry.get().strip()
    conf = confirm_entry.get().strip()
    gen = gender.get()

    print("Gender value:", gen)  # DEBUG

    if full == "" or full == "Full Name":
        show_error(error_fullname, "Required")
        valid = False

    if user == "" or user == "Username":
        show_error(error_username, "Required")
        valid = False

    if mail == "" or mail == "Email" or not validate_email(mail):
        show_error(error_email, "Invalid email")
        valid = False

    if ph == "" or ph == "Phone Number" or not ph.isdigit() or len(ph) != 10:
        show_error(error_phone, "Invalid phone")
        valid = False

    if pwd == "" or pwd == "Password":
        show_error(error_pass, "Required")
        valid = False

    if conf == "" or conf == "Confirm Password":
        show_error(error_confirm, "Required")
        valid = False
    elif pwd != conf:
        show_error(error_confirm, "Passwords mismatch")
        valid = False

    if gen not in ["Male", "Female"]:
        show_error(error_gender, "Select gender")
        valid = False

    if not valid:
        return

    # ---------------- DATABASE ---------------- #
    try:
        conn = get_db_connection()

        if conn is None:
            ms.showerror("Error", "Database not connected")
            return

        cursor = conn.cursor()

        cursor.execute(
            "INSERT INTO registration (fullname, username, email, phone, gender, password) VALUES (%s,%s,%s,%s,%s,%s)",
            (full, user, mail, ph, gen, pwd)
        )

        conn.commit()

        ms.showinfo("Success", "Registered Successfully")

        root.destroy()
        subprocess.Popen([sys.executable, "login.py"])

    except Exception as e:
        ms.showerror("Error", str(e))

    finally:
        if conn:
            conn.close()

# ---------------- PASSWORD TOGGLE ---------------- #
def toggle_password(event=None):
    global password_visible
    password_visible = not password_visible

    if password_visible:
        pass_entry.config(show="")
        confirm_entry.config(show="")
    else:
        pass_entry.config(show="*")
        confirm_entry.config(show="*")

# ---------------- CARD FRAME ---------------- #
card = tk.Frame(root, bg="white")
card.place(relx=0.5, rely=0.5, anchor="center", width=500, height=400)

tk.Label(card, text="Create Account",
         font=("Segoe UI", 22, "bold"),
         bg="white").grid(row=0, column=0, columnspan=2, pady=15)

entry_style = {"font": ("Segoe UI", 11), "bd": 2, "relief": "groove", "width": 25}

# ---------------- ROW 1 ---------------- #
fullname_entry = tk.Entry(card, textvariable=fullname, **entry_style)
fullname_entry.grid(row=1, column=0, padx=20, pady=5)
placeholder(fullname_entry, "Full Name")

username_entry = tk.Entry(card, textvariable=username, **entry_style)
username_entry.grid(row=1, column=1, padx=20, pady=5)
placeholder(username_entry, "Username")

error_fullname = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_fullname.grid(row=2, column=0)

error_username = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_username.grid(row=2, column=1)

# ---------------- ROW 2 ---------------- #
email_entry = tk.Entry(card, textvariable=email, **entry_style)
email_entry.grid(row=3, column=0, padx=20, pady=5)
placeholder(email_entry, "Email")

phone_entry = tk.Entry(card, textvariable=phone, **entry_style)
phone_entry.grid(row=3, column=1, padx=20, pady=5)
placeholder(phone_entry, "Phone Number")

error_email = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_email.grid(row=4, column=0)

error_phone = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_phone.grid(row=4, column=1)

# ---------------- PASSWORD ---------------- #
pass_entry = tk.Entry(card, textvariable=password, show="*", **entry_style)
pass_entry.grid(row=5, column=0, padx=20, pady=5)
placeholder(pass_entry, "Password")

confirm_entry = tk.Entry(card, textvariable=confirm, show="*", **entry_style)
confirm_entry.grid(row=5, column=1, padx=20, pady=5)
placeholder(confirm_entry, "Confirm Password")

pass_entry.bind("<Double-Button-1>", toggle_password)
confirm_entry.bind("<Double-Button-1>", toggle_password)

error_pass = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_pass.grid(row=6, column=0)

error_confirm = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_confirm.grid(row=6, column=1)

# ---------------- GENDER ---------------- #
tk.Label(card, text="Gender", bg="white").grid(row=7, column=0, pady=10)

gender_frame = tk.Frame(card, bg="white")
gender_frame.grid(row=7, column=1)

tk.Radiobutton(gender_frame, text="Male",
               variable=gender, value="Male",
               bg="white").pack(side="left", padx=10)

tk.Radiobutton(gender_frame, text="Female",
               variable=gender, value="Female",
               bg="white").pack(side="left", padx=10)

error_gender = tk.Label(card, text="", fg="red", bg="white", font=("Arial", 8))
error_gender.grid(row=8, column=1)

# ---------------- BUTTON ---------------- #
tk.Button(card,
          text="Register",
          command=register_user,
          bg="#4CAF50",
          fg="white",
          font=("Segoe UI", 11, "bold"),
          width=20).grid(row=9, column=0, columnspan=2, pady=20)

error_labels = [
    error_fullname, error_username,
    error_email, error_phone,
    error_pass, error_confirm,
    error_gender
]

root.mainloop()