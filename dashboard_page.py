import tkinter as tk
from PIL import Image, ImageTk


class DashboardPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.light_bg)
        self.controller = controller

        left = tk.Frame(self, bg=controller.light_bg)
        left.pack(side="left", fill="both", expand=True, padx=20, pady=15)

        self.title_label = tk.Label(
            left,
            text="Your Daily Fitness Snapshot",
            font=("Arial", 20, "bold"),
            bg=controller.light_bg,
            fg="#2E8B57"
        )
        self.title_label.pack(anchor="w")

        self.profile_label = tk.Label(
            left,
            text="Complete your profile to see personalized stats.",
            font=("Arial", 12),
            bg=controller.light_bg,
            fg=controller.light_fg,
            justify="left"
        )
        self.profile_label.pack(anchor="w", pady=(8, 5))

        stats_frame = tk.Frame(left, bg=controller.light_bg)
        stats_frame.pack(pady=10)

        self.streak_var = tk.StringVar()
        self.steps_var = tk.StringVar()
        self.calories_var = tk.StringVar()
        self.water_var = tk.StringVar()

        self.make_stat_card(stats_frame, "Workout Streak", self.streak_var, 0)
        self.make_stat_card(stats_frame, "Today's Steps", self.steps_var, 1)
        self.make_stat_card(stats_frame, "Calories Burned", self.calories_var, 2)
        self.make_stat_card(stats_frame, "Water Today", self.water_var, 3)

        btn_frame = tk.Frame(left, bg=controller.light_bg)
        btn_frame.pack(pady=10, anchor="w")

        tk.Button(
            btn_frame,
            text="+ 1,000 steps",
            command=self.add_steps,
            bg="#e0f7ff",
            fg=controller.light_fg,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=0, padx=4, pady=2)

        tk.Button(
            btn_frame,
            text="+ 50 kcal burned",
            command=self.add_calories,
            bg="#e0ffe0",
            fg=controller.light_fg,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=1, padx=4, pady=2)

        tk.Button(
            btn_frame,
            text="Drink 1 glass water",
            command=self.add_water,
            bg="#e6ddff",
            fg=controller.light_fg,
            font=("Arial", 10, "bold")
        ).grid(row=0, column=2, padx=4, pady=2)

        self.hint_label = tk.Label(
            left,
            text="Tip: Even a 5-minute workout moves you closer to your goal.",
            font=("Arial", 11, "italic"),
            bg=controller.light_bg,
            fg="#555555",
            wraplength=500,
            justify="left"
        )
        self.hint_label.pack(pady=(12, 0), anchor="w")

        right = tk.Frame(self, bg=controller.light_bg)
        right.pack(side="right", fill="y", padx=20, pady=15)

        self.goal_title = tk.Label(
            right,
            text="Your Fitness Goal Vision",
            font=("Arial", 14, "bold"),
            bg=controller.light_bg,
            fg="#2E8B57"
        )
        self.goal_title.pack(pady=(0, 10))

        # show your actual goal image (goal_body.webp) – no red text
        img = Image.open("goal_body.webp")
        img = img.resize((230, 230), Image.LANCZOS)
        self.goal_photo = ImageTk.PhotoImage(img)
        self.goal_label = tk.Label(right, image=self.goal_photo, bg=controller.light_bg)
        self.goal_label.pack()

        self.goal_caption = tk.Label(
            right,
            text="Strong, confident, and healthy.\nYou are working toward your own version of this.",
            font=("Arial", 10),
            bg=controller.light_bg,
            fg=controller.light_fg,
            wraplength=230,
            justify="center"
        )
        self.goal_caption.pack(pady=10)

        self.refresh()

    def make_stat_card(self, parent, title, var, col):
        frame = tk.Frame(parent, bg="#f5f5f5", bd=1, relief="ridge", width=140, height=80)
        frame.grid(row=0, column=col, padx=5, pady=5)
        frame.grid_propagate(False)
        tk.Label(
            frame,
            text=title,
            font=("Arial", 10, "bold"),
            bg="#f5f5f5",
            fg="#333333"
        ).pack(pady=(8, 2))
        tk.Label(
            frame,
            textvariable=var,
            font=("Arial", 11),
            bg="#f5f5f5",
            fg="#000000"
        ).pack()

    def refresh(self):
        profile = self.controller.profile
        if profile:
            name = profile.get("name", "User")
            age = profile.get("age", "?")
            weight = profile.get("weight", "?")
            height = profile.get("height", "?")
            body_type = profile.get("body_type", "")
            goal = profile.get("goal", "Not set")
            text = (
                f"{name}\n"
                f"Age: {age} yrs | Weight: {weight} kg | Height: {height} cm\n"
                f"Body type: {body_type}\n"
                f"Goal: {goal}"
            )
        else:
            text = "Complete your profile to see personalized stats."
        self.profile_label.config(text=text)

        stats = self.controller.stats
        self.streak_var.set(f"{stats['streak']} days")
        self.steps_var.set(f"{stats['steps']} steps")
        self.calories_var.set(f"{stats['calories']} kcal")
        self.water_var.set(f"{stats['water_ml'] // 250} glasses")

    def add_steps(self):
        self.controller.stats["steps"] += 1000
        self.refresh()

    def add_calories(self):
        self.controller.stats["calories"] += 50
        self.refresh()

    def add_water(self):
        self.controller.stats["water_ml"] += 250
        self.refresh()

    def on_show(self):
        self.refresh()

    def update_theme(self, bg, fg):
        self.configure(bg=bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except tk.TclError:
                pass
        self.goal_caption.configure(bg=bg, fg=fg)
        self.hint_label.configure(bg=bg, fg="#555555")
        self.title_label.configure(bg=bg)
        self.profile_label.configure(bg=bg, fg=fg)
