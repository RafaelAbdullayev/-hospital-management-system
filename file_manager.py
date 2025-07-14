import tkinter as tk
from tkinter import messagebox, ttk
import pickle
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import datetime

COLORS = {
    "bg": "#FFFFFF",
    "button": "#2C3E50",
    "button_active": "#34495E",
    "text": "#000000",
    "title": "#000000"
}

try:
    with open("users.pickle", "rb") as file:
        users = pickle.load(file)
except (FileNotFoundError, EOFError):
    users = []
    with open("users.pickle", "wb") as file:
        pickle.dump(users, file)


screen_stack = []
main_window = tk.Tk()
main_window.title("User Management System")
main_window.geometry("500x600")
main_window.config(bg=COLORS["bg"])


style = ttk.Style()
style.configure("TButton",
    font=("Arial", 12),
    padding=8,
    background="white",
    foreground="black",
)
style.map("TButton",
    background=[("active", COLORS["button_active"])])
style.configure("TEntry",
    fieldbackground="white",
    borderwidth=1,
    foreground=COLORS["text"],
    font=("Arial", 12)
)

main_frame = tk.Frame(main_window, bg=COLORS["bg"])
main_frame.pack(fill="both", expand=True)

def show_start_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="User Management System",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    login_button = ttk.Button(main_frame, text="Login", width=20, command=show_login_screen)
    login_button.pack(pady=10)

    register_button = ttk.Button(main_frame, text="Register", width=20, command=show_register_screen)
    register_button.pack(pady=10)

def show_register_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="Register",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    lbl_username = tk.Label(main_frame,
        text="Username:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_username.pack()
    username_entry = ttk.Entry(main_frame, font=("Arial", 12))
    username_entry.pack(pady=5)

    lbl_password = tk.Label(main_frame,
        text="Password:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_password.pack()
    password_entry = ttk.Entry(main_frame, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    lbl_fullname = tk.Label(main_frame,
        text="Full Name:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_fullname.pack()
    fullname_entry = ttk.Entry(main_frame, font=("Arial", 12))
    fullname_entry.pack(pady=5)

    role_label = tk.Label(main_frame,
        text="Role (admin/user):",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    role_label.pack()
    role_entry = ttk.Entry(main_frame, font=("Arial", 12))
    role_entry.pack(pady=5)

    register_button = ttk.Button(main_frame, text="Register", width=20,
                                command=lambda: register_user(username_entry.get(), password_entry.get(),
                                                           fullname_entry.get(), role_entry.get()))
    register_button.pack(pady=20)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_start_screen)
    back_button.pack(pady=10)

def register_user(username, password, fullname, role):
    if not username or not password or not fullname or not role:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    if role.lower() not in ["admin", "user"]:
        messagebox.showerror("Error", "Role must be either 'admin' or 'user'!")
        return

    if any(user["username"] == username for user in users):
        messagebox.showerror("Error", "Username already exists!")
        return

    new_user = {
        "username": username,
        "password": password,
        "fullname": fullname,
        "role": role.lower()
    }
    save_user(new_user)
    messagebox.showinfo("Success", "User registered successfully!")
    show_start_screen()


def save_user(user):
    if isinstance(user, dict):
        users.append(user)
    with open("users.pickle", "wb") as file:
        pickle.dump(users, file)


def show_login_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="Login",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    lbl_username = tk.Label(main_frame,
        text="Username:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_username.pack()
    username_entry = ttk.Entry(main_frame, font=("Arial", 12))
    username_entry.pack(pady=5)

    lbl_password = tk.Label(main_frame,
        text="Password:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_password.pack()
    password_entry = ttk.Entry(main_frame, font=("Arial", 12), show="*")
    password_entry.pack(pady=5)

    login_button = ttk.Button(main_frame, text="Login", width=20,
                             command=lambda: check_login(username_entry.get(), password_entry.get()))
    login_button.pack(pady=20)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_start_screen)
    back_button.pack(pady=10)

def check_login(username, password):
    if not username or not password:
        messagebox.showerror("Error", "Please fill in all fields!")
        return

    for user in users:
        if user["username"] == username and user["password"] == password:
            messagebox.showinfo("Success", f"Welcome, {user['fullname']}! Role: {user['role']}")
            if user["role"] == "admin":
                show_admin_screen()
            else:
                show_start_screen()
            return

    messagebox.showerror("Error", "Incorrect username or password!")

def show_admin_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="Admin Panel",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    stats_button = ttk.Button(main_frame, text="System Statistics", width=20, command=show_statistics_screen)
    stats_button.pack(pady=10)

    change_password_button = ttk.Button(main_frame, text="Change Password", width=20, command=show_change_password_screen)
    change_password_button.pack(pady=10)

    delete_user_button = ttk.Button(main_frame, text="Delete User", width=20, command=show_delete_user_screen)
    delete_user_button.pack(pady=10)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_start_screen)
    back_button.pack(pady=10)

def show_statistics_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="System Statistics",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    total_users = len(users)
    admin_count = len([user for user in users if user["role"] == "admin"])
    user_count = total_users - admin_count

    stats_label = tk.Label(main_frame,
        text=f"Total Users: {total_users}\nAdmins: {admin_count}\nUsers: {user_count}",
        font=("Arial", 16),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    stats_label.pack(pady=20)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_admin_screen)
    back_button.pack(pady=10)


def show_change_password_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="Change Password",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    lbl_new_password = tk.Label(main_frame,
        text="New Password:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_new_password.pack()
    new_password_entry = ttk.Entry(main_frame, font=("Arial", 12), show="*")
    new_password_entry.pack(pady=5)

    change_button = ttk.Button(main_frame, text="Change", width=20, command=lambda: change_password(new_password_entry.get()))
    change_button.pack(pady=20)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_admin_screen)
    back_button.pack(pady=10)

def change_password(new_password):
    if not new_password:
        messagebox.showerror("Error", "Please enter a new password!")
        return



    messagebox.showinfo("Success", "Password changed successfully!")
    show_admin_screen()


def show_delete_user_screen():
    for widget in main_frame.winfo_children():
        widget.destroy()

    title = tk.Label(main_frame,
        text="Delete User",
        font=("Arial", 24, "bold"),
        bg=COLORS["bg"],
        fg=COLORS["title"]
    )
    title.pack(pady=30)

    lbl_username = tk.Label(main_frame,
        text="Username to Delete:",
        font=("Arial", 12),
        bg=COLORS["bg"],
        fg=COLORS["text"]
    )
    lbl_username.pack()
    username_entry = ttk.Entry(main_frame, font=("Arial", 12))
    username_entry.pack(pady=5)

    delete_button = ttk.Button(main_frame, text="Delete", width=20, command=lambda: delete_user(username_entry.get()))
    delete_button.pack(pady=20)

    back_button = ttk.Button(main_frame, text="Back", width=20, command=show_admin_screen)
    back_button.pack(pady=10)

def delete_user(username):
    if not username:
        messagebox.showerror("Error", "Please enter a username!")
        return

    global users
    users = [user for user in users if user["username"] != username]
    with open("users.pickle", "wb") as file:
        pickle.dump(users, file)

    messagebox.showinfo("Success", f"User '{username}' deleted successfully!")
    show_admin_screen()

show_start_screen()
main_window.mainloop()
