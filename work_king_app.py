# the tkinter imports the gui toolkit
# the messege box is for pop-ups for errors 
# the PIL image imports and loads and resizes the image
# the json reads and loads the data into json and the import os checks if file exists.
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import json
import os

from dashboard_page import DashboardPage
from profile_page import ProfilePage
from workout_page import WorkoutPage
from diet_page import DietPage
from motivation_page import MotivationPage

#this below is the defination of class workingapp
#it is a main window (subclass of tk,Tk)
class WorkKingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Work-King: Your Personalized Fitness Companion")
        self.geometry("1100x700")
        self.minsize(950, 600)

        # these are the definations of colors
        self.bg = "white"
        self.fg = "black"
        self.nav_bg = "#f5f5f5"
        self.nav_fg = "#2E8B57"

        # checking color compactibility
        self.light_bg = self.bg
        self.light_fg = self.fg
        self.soft_bg = "#f0e6d2"
        self.soft_fg = "#3e3e3e"
        self.comfort_mode = False  # some pages may check this

        # these are the app data
        self.users = {} #dictonary of user and password from json file
        self.current_user = None #username of the person logged in
        self.profile = {} #profile information on 3rd page
        self.body_type_choice = "Ectomorph"
        self.goal_choice = "Gain Weight"
        #these are the numbers of dashboard
        self.stats = {"steps": 0, "calories": 0, "water_ml": 0, "streak": 1}


        # these are the refrence of image 
        self.login_frame = None
        self.welcome_frame = None
        self.setup_frame = None
        self.main_frame = None
        self.nav_frame = None
        self.page_container = None
        self.pages = {}

        # images
        self.logo_img1 = None
        self.logo_img2 = None
        self.body_img = None

        # this loads the initial start of program
        self.load_users()
        self.show_login_page()

    # this loads and save the user in json file

    def load_users(self):
        if os.path.exists("users.json"):
            try:
                with open("users.json", "r", encoding="utf-8") as f:
                    self.users = json.load(f)
            except (OSError, json.JSONDecodeError):
                self.users = {}
        else:
            self.users = {}

    def save_users(self):
        try:
            with open("users.json", "w", encoding="utf-8") as f:
                json.dump(self.users, f)
        except OSError:
            messagebox.showerror("Error", "Could not save user data.")

    def clear_frames(self):
        for f in [self.login_frame, self.welcome_frame, self.setup_frame, self.main_frame]:
            if f is not None:
                f.destroy()
        self.login_frame = self.welcome_frame = self.setup_frame = self.main_frame = None

    #this is login page 
    def show_login_page(self):
        self.clear_frames()
        self.login_frame = tk.Frame(self, bg=self.bg) #login
        self.login_frame.pack(fill="both", expand=True) #create account

        title = tk.Label(
            self.login_frame,
            text="Work-King Login",
            font=("Arial", 24, "bold"),
            bg=self.bg,
            fg=self.nav_fg,
        )
        title.pack(pady=(40, 10))

        subtitle = tk.Label(
            self.login_frame,
            text="Log in to continue, or create a new account.",
            font=("Arial", 12),
            bg=self.bg,
            fg=self.fg,
        )
        subtitle.pack(pady=(0, 20))

        form = tk.Frame(self.login_frame, bg=self.bg)
        form.pack(pady=10)

        tk.Label(form, text="Username:", font=("Arial", 11), bg=self.bg).grid(
            row=0, column=0, sticky="e", padx=5, pady=5
        )
        tk.Label(form, text="Password:", font=("Arial", 11), bg=self.bg).grid(
            row=1, column=0, sticky="e", padx=5, pady=5
        )

        self.username_entry = tk.Entry(form, width=25, font=("Arial", 11))
        self.username_entry.grid(row=0, column=1, padx=5, pady=5)

        self.password_entry = tk.Entry(form, width=25, show="*", font=("Arial", 11))
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        btn_frame = tk.Frame(self.login_frame, bg=self.bg)
        btn_frame.pack(pady=15)

        tk.Button(
            btn_frame,
            text="Log In",
            font=("Arial", 12, "bold"),
            bg="#4682B4",
            fg="white",
            padx=18,
            pady=6,
            command=self.handle_login,
        ).grid(row=0, column=0, padx=8)

        tk.Button(
            btn_frame,
            text="Create Account",
            font=("Arial", 12, "bold"),
            bg="#2E8B57",
            fg="white",
            padx=18,
            pady=6,
            command=self.handle_create_account,
        ).grid(row=0, column=1, padx=8)

    #here below are the login check for example checking entries of both feilds
    # if everything is correct it moves forward and sets current_user
    def handle_login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Login Failed", "Please enter both username and password.")
            return

        if username not in self.users or self.users[username] != password:
            messagebox.showerror("Login Failed", "Incorrect username or password.")
            return

        self.current_user = username
        self.show_welcome_page()

    # this creates the account and enters to welcome page
    def handle_create_account(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Create Account", "Username and password cannot be empty.")
            return

        if username in self.users:
            messagebox.showerror("Create Account", "That username is already taken.")
            return

        if len(password) < 3:
            messagebox.showerror("Create Account", "Use a password with at least 3 characters.")
            return

        self.users[username] = password
        self.save_users()
        messagebox.showinfo("Create Account", "Account created. You are now logged in.")
        self.current_user = username
        self.show_welcome_page()

    # this below is the welcome page
    #we have title logo and start in the page after login.

    def show_welcome_page(self):
        self.clear_frames()
        self.welcome_frame = tk.Frame(self, bg=self.bg)
        self.welcome_frame.pack(fill="both", expand=True)

        self.welcome_frame.rowconfigure(0, weight=2)
        self.welcome_frame.rowconfigure(1, weight=4)
        self.welcome_frame.rowconfigure(2, weight=1)
        self.welcome_frame.columnconfigure(0, weight=1)

        welcome_label = tk.Label(
            self.welcome_frame,
            text="Welcome to Work-King\nYour Personalized Fitness Companion",
            font=("Arial", 26, "bold"),
            fg="#2E8B57",
            bg=self.bg,
            justify="center",
        )
        welcome_label.grid(row=0, column=0, pady=(25, 10))

        logo_frame = tk.Frame(self.welcome_frame, bg=self.bg)
        logo_frame.grid(row=1, column=0, pady=10)
        logo_frame.columnconfigure(0, weight=1)
        logo_frame.columnconfigure(1, weight=1)

        try:
            img1 = Image.open("applogo.jpg").resize((220, 220), Image.LANCZOS)
            img2 = Image.open("applogo2.jpg").resize((220, 220), Image.LANCZOS)
            self.logo_img1 = ImageTk.PhotoImage(img1)
            self.logo_img2 = ImageTk.PhotoImage(img2)

            tk.Label(logo_frame, image=self.logo_img1, bg=self.bg).grid(row=0, column=0, padx=25)
            tk.Label(logo_frame, image=self.logo_img2, bg=self.bg).grid(row=0, column=1, padx=25)
        except Exception:
            tk.Label(
                logo_frame,
                text="(Add applogo.jpg and applogo2.jpg)",
                bg=self.bg,
                fg="#aa0000",
            ).grid(row=0, column=0, columnspan=2, pady=10)

        start_btn = tk.Button(
            self.welcome_frame,
            text="Start",
            font=("Arial", 16, "bold"),
            bg="#4682B4",
            fg="white",
            padx=26,
            pady=8,
            command=self.show_setup_page,
        )
        start_btn.grid(row=2, column=0, pady=(15, 25))

    # this is the third page (setup) page to enter weight height and body type

    def show_setup_page(self):
        self.clear_frames()
        self.setup_frame = tk.Frame(self, bg=self.bg)
        self.setup_frame.pack(fill="both", expand=True)

        title = tk.Label(
            self.setup_frame,
            text="Step 1: Enter your details and choose your body type & goal",
            font=("Arial", 20, "bold"),
            bg=self.bg,
            fg="#2E8B57",
            wraplength=900,
            justify="center",
        )
        title.pack(pady=(10, 5))

        # age / weight / height
        info_frame = tk.Frame(self.setup_frame, bg=self.bg)
        info_frame.pack(pady=(0, 5))

        tk.Label(info_frame, text="Age (years):", font=("Arial", 11, "bold"), bg=self.bg).grid(
            row=0, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(info_frame, text="Weight (kg):", font=("Arial", 11, "bold"), bg=self.bg).grid(
            row=1, column=0, sticky="e", padx=5, pady=2
        )
        tk.Label(info_frame, text="Height (cm):", font=("Arial", 11, "bold"), bg=self.bg).grid(
            row=2, column=0, sticky="e", padx=5, pady=2
        )

        self.age_entry = tk.Entry(info_frame, width=15, font=("Arial", 11))
        self.weight_entry = tk.Entry(info_frame, width=15, font=("Arial", 11))
        self.height_entry = tk.Entry(info_frame, width=15, font=("Arial", 11))

        self.age_entry.grid(row=0, column=1, padx=5, pady=2)
        self.weight_entry.grid(row=1, column=1, padx=5, pady=2)
        self.height_entry.grid(row=2, column=1, padx=5, pady=2)

        # body type image (smaller)
        img_frame = tk.Frame(self.setup_frame, bg=self.bg)
        img_frame.pack(pady=(4, 4))

        self.body_img = None
        try:
            try:
                img = Image.open("body_types.webp")
            except Exception:
                img = Image.open("body_types.png")
            img.thumbnail((550, 230), Image.LANCZOS)
            self.body_img = ImageTk.PhotoImage(img)
            tk.Label(img_frame, image=self.body_img, bg=self.bg).pack()
        except Exception:
            tk.Label(
                img_frame,
                text="(Add body_types.webp or body_types.png)",
                bg=self.bg,
                fg="#aa0000",
            ).pack()

        # body type radios
        body_q = tk.Label(
            self.setup_frame,
            text="Which is your current body type?",
            font=("Arial", 13, "bold"),
            bg=self.bg,
            fg=self.fg,
        )
        body_q.pack(pady=(4, 2))

        self.body_type_var = tk.StringVar(value=self.body_type_choice)
        bt_frame = tk.Frame(self.setup_frame, bg=self.bg)
        bt_frame.pack()

        for text in ["Ectomorph", "Mesomorph", "Endomorph"]:
            tk.Radiobutton(
                bt_frame,
                text=text,
                variable=self.body_type_var,
                value=text,
                bg=self.bg,
                fg=self.fg,
                font=("Arial", 11),
            ).pack(side="left", padx=6)

        # goal radios
        goal_q = tk.Label(
            self.setup_frame,
            text="What would you like to do?",
            font=("Arial", 13, "bold"),
            bg=self.bg,
            fg=self.fg,
        )
        goal_q.pack(pady=(6, 2))

        self.goal_var = tk.StringVar(value=self.goal_choice)
        goal_frame = tk.Frame(self.setup_frame, bg=self.bg)
        goal_frame.pack()

        goals = [
            ("Gain Weight", "Gain Weight"),
            ("Reduce weight through workout", "Reduce weight through workout"),
            ("My weight is perfect, just want to maintain", "Maintain current weight"),
        ]
        for text, val in goals:
            tk.Radiobutton(
                goal_frame,
                text=text,
                variable=self.goal_var,
                value=val,
                bg=self.bg,
                fg=self.fg,
                wraplength=400,
                justify="left",
                font=("Arial", 11),
            ).pack(anchor="w")

        continue_btn = tk.Button(
            self.setup_frame,
            text="Continue",
            font=("Arial", 14, "bold"),
            bg="#4682B4",
            fg="white",
            padx=18,
            pady=4,
            command=self.save_profile_and_open_main,
        )
        continue_btn.pack(pady=(10, 8))

    # this is for the continue button
    # reads the value and saves into self.profile
    #calls the show_main_layout to open other pages
    def save_profile_and_open_main(self):
        age = self.age_entry.get().strip()
        weight = self.weight_entry.get().strip()
        height = self.height_entry.get().strip()

        self.body_type_choice = self.body_type_var.get()
        self.goal_choice = self.goal_var.get()
        username = self.current_user or "User"

        self.profile = {
            "name": username,
            "age": age,
            "weight": weight,
            "height": height,
            "body_type": self.body_type_choice,
            "goal": self.goal_choice,
        }

        self.show_main_layout()

    # this is the main layout after entering the app
    # this code has layout of sidebars with interal pages like dashboard, profiles

    def show_main_layout(self):
        self.clear_frames()
        self.main_frame = tk.Frame(self, bg=self.bg)
        self.main_frame.pack(fill="both", expand=True)

        self.main_frame.columnconfigure(0, weight=0)
        self.main_frame.columnconfigure(1, weight=1)
        self.main_frame.rowconfigure(0, weight=1)

        # these below are the codes for sidebar
        self.nav_frame = tk.Frame(self.main_frame, bg=self.nav_bg, width=190)
        self.nav_frame.grid(row=0, column=0, sticky="nsw")

        title_label = tk.Label(
            self.nav_frame,
            text="Work-King",
            font=("Arial", 18, "bold"),
            bg=self.nav_bg,
            fg=self.nav_fg,
        )
        title_label.pack(pady=(15, 10), padx=10, anchor="w")

        buttons = [
            ("Dashboard", "DashboardPage"),
            ("Profile", "ProfilePage"),
            ("Workouts", "WorkoutPage"),
            ("Diet", "DietPage"),
            ("Motivation", "MotivationPage"),
        ]
        for text, page_name in buttons:
            tk.Button(
                self.nav_frame,
                text=text,
                font=("Arial", 11),
                bg="white",
                fg="black",
                relief="raised",
                bd=1,
                command=lambda p=page_name: self.show_page(p),
            ).pack(fill="x", padx=10, pady=4)

        # this below is the main page area
        self.page_container = tk.Frame(self.main_frame, bg=self.bg)
        self.page_container.grid(row=0, column=1, sticky="nsew")
        self.page_container.rowconfigure(0, weight=1)
        self.page_container.columnconfigure(0, weight=1)

        # create pages
        self.pages = {}
        for PageClass in (DashboardPage, ProfilePage, WorkoutPage, DietPage, MotivationPage):
            page_name = PageClass.__name__
            frame = PageClass(self.page_container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.pages[page_name] = frame

        # start on Dashboard
        self.show_page("DashboardPage")

    def show_page(self, page_name):
        page = self.pages.get(page_name)
        if not page:
            return
        page.tkraise()
        if hasattr(page, "on_show"):
            page.on_show()


if __name__ == "__main__":
    app = WorkKingApp()
    app.mainloop()
