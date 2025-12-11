import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os


class WorkoutPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.light_bg)
        self.controller = controller

        self.workout_photo = None
        self.meal_photo = None
        self.workout_image_path = None
        self.meal_image_path = None

        title = tk.Label(
            self,
            text="Workout & Meal Plan For Your Goal",
            font=("Arial", 20, "bold"),
            bg=controller.light_bg,
            fg="#2E8B57"
        )
        title.pack(pady=(15, 5))

        self.goal_label = tk.Label(
            self,
            text="Set your goal on the Profile page to see your plan.",
            font=("Arial", 11),
            bg=controller.light_bg,
            fg=controller.light_fg
        )
        self.goal_label.pack(pady=(0, 8))

        img_frame = tk.Frame(self, bg=controller.light_bg)
        img_frame.pack(padx=20, pady=8, fill="both", expand=True)

        left_frame = tk.Frame(img_frame, bg=controller.light_bg)
        left_frame.pack(side="left", expand=True, padx=10, pady=10, fill="both")

        right_frame = tk.Frame(img_frame, bg=controller.light_bg)
        right_frame.pack(side="right", expand=True, padx=10, pady=10, fill="both")

        self.workout_title = tk.Label(
            left_frame,
            text="Workout Plan (click image to zoom)",
            font=("Arial", 13, "bold"),
            bg=controller.light_bg,
            fg="#333333"
        )
        self.workout_title.pack(pady=(0, 5))

        self.workout_label = tk.Label(left_frame, bg=controller.light_bg, cursor="hand2")
        self.workout_label.pack(expand=True)

        self.meal_title = tk.Label(
            right_frame,
            text="Meal Plan (click image to zoom)",
            font=("Arial", 13, "bold"),
            bg=controller.light_bg,
            fg="#333333"
        )
        self.meal_title.pack(pady=(0, 5))

        self.meal_label = tk.Label(right_frame, bg=controller.light_bg, cursor="hand2")
        self.meal_label.pack(expand=True)

        # click to zoom
        self.workout_label.bind("<Button-1>", lambda e: self.open_zoom("workout"))
        self.meal_label.bind("<Button-1>", lambda e: self.open_zoom("meal"))

        btn_frame = tk.Frame(self, bg=controller.light_bg)
        btn_frame.pack(pady=(4, 4))

        tk.Button(
            btn_frame,
            text="Show Detailed Plan",
            command=self.show_detailed_plan,
            bg="#6a5acd",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=4
        ).grid(row=0, column=0, padx=6)

        tk.Button(
            btn_frame,
            text="Quick 5-min Workout",
            command=self.quick_workout,
            bg="#f0a500",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=12,
            pady=4
        ).grid(row=0, column=1, padx=6)

        self.text = tk.Text(
            self,
            width=95,
            height=14,
            wrap="word",
            bg="#f9f9f9",
            fg=controller.light_fg,
            font=("Arial", 11)
        )
        self.text.pack(padx=20, pady=(6, 10))

        tip = tk.Label(
            self,
            text="Tip: Change your goal in the Profile tab. Images and plans will update automatically.",
            font=("Arial", 10, "italic"),
            bg=controller.light_bg,
            fg="#555555",
            wraplength=820,
            justify="center"
        )
        tip.pack(pady=(0, 6))

    # ---------- helpers ----------

    def get_goal_text(self):
        goal = ""
        if self.controller.profile and self.controller.profile.get("goal"):
            goal = self.controller.profile["goal"]
        elif getattr(self.controller, "goal_choice", None):
            goal = self.controller.goal_choice
        return goal.lower()

    def find_image_file(self, stem):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        exts = [".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG", ".PNG", ".WEBP"]
        for ext in exts:
            path = os.path.join(base_dir, stem + ext)
            if os.path.exists(path):
                return path
        return None

    def load_image(self, path, max_width=380, max_height=320):
        img = Image.open(path)
        w, h = img.size
        scale = min(max_width / w, max_height / h)
        new_size = (int(w * scale), int(h * scale))
        img = img.resize(new_size, Image.LANCZOS)
        return ImageTk.PhotoImage(img)

    # ---------- images for goal ----------

    def update_images_for_goal(self):
        goal_text = self.get_goal_text()

        if not goal_text:
            self.goal_label.config(
                text="Set your goal on the Profile page to see your workout and meal plans."
            )
            self.workout_label.config(text="No goal selected", image="")
            self.meal_label.config(text="No goal selected", image="")
            self.workout_photo = None
            self.meal_photo = None
            self.workout_image_path = None
            self.meal_image_path = None
            return

        if "gain" in goal_text:
            goal_key = "gain"
            nice_text = "Current goal: Gain weight and build muscle."
        elif "reduce" in goal_text or "lose" in goal_text:
            goal_key = "loss"
            nice_text = "Current goal: Reduce weight through workouts."
        else:
            goal_key = "remain"
            nice_text = "Current goal: Maintain your current weight and fitness."

        self.goal_label.config(text=nice_text)

        workout_stem = f"{goal_key}_workout"
        meal_stem = f"{goal_key}_meal"

        workout_path = self.find_image_file(workout_stem)
        meal_path = self.find_image_file(meal_stem)

        self.workout_image_path = workout_path
        self.meal_image_path = meal_path

        if workout_path:
            self.workout_photo = self.load_image(workout_path)
            self.workout_label.config(image=self.workout_photo, text="")
        else:
            self.workout_label.config(text=f"Image not found: {workout_stem}", image="")
            self.workout_photo = None

        if meal_path:
            self.meal_photo = self.load_image(meal_path)
            self.meal_label.config(image=self.meal_photo, text="")
        else:
            self.meal_label.config(text=f"Image not found: {meal_stem}", image="")
            self.meal_photo = None

    # ---------- zoom window ----------

    def open_zoom(self, kind):
        if kind == "workout":
            path = self.workout_image_path
            title = "Workout Plan – Zoom"
        else:
            path = self.meal_image_path
            title = "Meal Plan – Zoom"

        if not path:
            messagebox.showinfo("No image", "No image available to zoom for this section.")
            return

        try:
            img = Image.open(path)
        except Exception:
            messagebox.showerror("Error", "Could not open image.")
            return

        top = tk.Toplevel(self)
        top.title(title)
        top.geometry("900x700")

        canvas = tk.Canvas(top, bg="black")
        hbar = tk.Scrollbar(top, orient="horizontal", command=canvas.xview)
        vbar = tk.Scrollbar(top, orient="vertical", command=canvas.yview)
        canvas.configure(xscrollcommand=hbar.set, yscrollcommand=vbar.set)

        hbar.pack(side="bottom", fill="x")
        vbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        photo = ImageTk.PhotoImage(img)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo
        canvas.config(scrollregion=canvas.bbox("all"))

    # ---------- detailed text plans ----------

    def show_detailed_plan(self):
        goal_text = self.get_goal_text()
        if not goal_text:
            messagebox.showerror(
                "Profile Needed",
                "Please fill out your profile or select a goal on the welcome screen first."
            )
            return

        self.text.delete("1.0", tk.END)

        if "gain" in goal_text:
            self.text.insert(tk.END, "Full Gain-Weight Plan\n")
            self.text.insert(tk.END, "======================\n\n")
            self.text.insert(tk.END, "Workout Focus:\n")
            self.text.insert(tk.END, " • 3–5 days/week strength training (squats, presses, rows, deadlifts).\n")
            self.text.insert(tk.END, " • Use weights that feel challenging but safe.\n")
            self.text.insert(tk.END, " • Rest 60–90 seconds between sets.\n\n")
            self.text.insert(tk.END, "Eating Guide:\n")
            self.text.insert(tk.END, " • Eat 300–500 calories above your usual intake.\n")
            self.text.insert(tk.END, " • Eat 3 main meals + 2–3 snacks every day.\n")
            self.text.insert(tk.END, " • Include protein at every meal (eggs, yogurt, milk,\n")
            self.text.insert(tk.END, "   beans, lentils, chicken, fish).\n")
            self.text.insert(tk.END, " • Add calorie-dense foods: nuts, peanut butter, cheese,\n")
            self.text.insert(tk.END, "   avocado, olive oil.\n\n")
            self.text.insert(tk.END, "Simple Day of Eating:\n")
            self.text.insert(tk.END, " • Breakfast: eggs + toast + banana + milk\n")
            self.text.insert(tk.END, " • Snack: yogurt with nuts or smoothie\n")
            self.text.insert(tk.END, " • Lunch: rice/pasta + protein + vegetables\n")
            self.text.insert(tk.END, " • Snack: peanut butter sandwich or fruit + nuts\n")
            self.text.insert(tk.END, " • Dinner: potatoes or rice + protein + vegetables\n\n")
            self.text.insert(tk.END, "Progress Tips:\n")
            self.text.insert(tk.END, " • Aim to gain around 0.25–0.5 kg per week.\n")
            self.text.insert(tk.END, " • If weight is stuck for 2–3 weeks, increase portions a little.\n")
            self.text.insert(tk.END, " • Sleep 7–9 hours to help your body recover.\n")

        elif "reduce" in goal_text or "lose" in goal_text:
            self.text.insert(tk.END, "Full Fat-Loss Plan\n")
            self.text.insert(tk.END, "==================\n\n")
            self.text.insert(tk.END, "Workout Focus:\n")
            self.text.insert(tk.END, " • 3–4 days of cardio (walking, jogging, cycling, dance).\n")
            self.text.insert(tk.END, " • 2–3 days of strength training (can be on the same days).\n")
            self.text.insert(tk.END, " • Example strength block:\n")
            self.text.insert(tk.END, "   • Squats or sit-to-stands – 10–12 reps\n")
            self.text.insert(tk.END, "   • Lunges or step-ups – 8–10 reps each leg\n")
            self.text.insert(tk.END, "   • Push-ups (wall, knee, or full) – 8–12 reps\n")
            self.text.insert(tk.END, "   • Band or dumbbell rows – 10–12 reps\n")
            self.text.insert(tk.END, "   • Plank – 20–40 seconds\n\n")
            self.text.insert(tk.END, "Eating Guide for Fat Loss:\n")
            self.text.insert(tk.END, " • Eat a little less than usual (300–500 fewer calories per day).\n")
            self.text.insert(tk.END, " • Fill half your plate with vegetables.\n")
            self.text.insert(tk.END, " • Keep protein high to feel full (eggs, yogurt, beans,\n")
            self.text.insert(tk.END, "   lentils, chicken, fish).\n")
            self.text.insert(tk.END, " • Choose whole carbs (oats, rice, potatoes,\n")
            self.text.insert(tk.END, "   whole-grain bread, fruits).\n")
            self.text.insert(tk.END, " • Limit sugary drinks, sweets, and fried food.\n\n")
            self.text.insert(tk.END, "Simple Day of Eating:\n")
            self.text.insert(tk.END, " • Breakfast: oats with milk or yogurt + fruit\n")
            self.text.insert(tk.END, " • Snack: handful of nuts or yogurt\n")
            self.text.insert(tk.END, " • Lunch: rice/potatoes + protein + vegetables\n")
            self.text.insert(tk.END, " • Snack: fruit or veggie sticks with hummus\n")
            self.text.insert(tk.END, " • Dinner: protein + vegetables + small carb portion\n\n")
            self.text.insert(tk.END, "Progress Tips:\n")
            self.text.insert(tk.END, " • Aim to lose about 0.25–0.5 kg per week.\n")
            self.text.insert(tk.END, " • Track waist, hips, and how clothes fit, not just the scale.\n")
            self.text.insert(tk.END, " • Be patient and consistent; small daily efforts matter.\n")

        else:
            self.text.insert(tk.END, "Maintenance Plan\n")
            self.text.insert(tk.END, "================\n\n")
            self.text.insert(tk.END, "Workout Focus:\n")
            self.text.insert(tk.END, " • 2–3 full-body strength days per week.\n")
            self.text.insert(tk.END, " • 1–3 light cardio days (walking, cycling, sports).\n\n")
            self.text.insert(tk.END, "Balanced Eating:\n")
            self.text.insert(tk.END, " • Eat until comfortably satisfied, not stuffed.\n")
            self.text.insert(tk.END, " • Base meals on whole foods most of the time.\n")
            self.text.insert(tk.END, " • Enjoy treats in moderation without guilt.\n\n")
            self.text.insert(tk.END, "Example Day of Eating:\n")
            self.text.insert(tk.END, " • Breakfast: eggs + toast + fruit\n")
            self.text.insert(tk.END, " • Lunch: grain bowl with beans/chicken and vegetables\n")
            self.text.insert(tk.END, " • Snack: nuts, yogurt, or fruit\n")
            self.text.insert(tk.END, " • Dinner: protein + vegetables + potatoes/rice or bread\n\n")
            self.text.insert(tk.END, "Long-Term Tips:\n")
            self.text.insert(tk.END, " • Check your weight or how clothes fit every few weeks.\n")
            self.text.insert(tk.END, " • Adjust portions slightly if weight drifts up or down.\n")

    def quick_workout(self):
        self.text.delete("1.0", tk.END)
        self.text.insert(tk.END, "Quick 5-Minute Workout\n")
        self.text.insert(tk.END, "======================\n\n")
        self.text.insert(tk.END, "1 min – March or jog in place\n")
        self.text.insert(tk.END, "1 min – Bodyweight squats\n")
        self.text.insert(tk.END, "1 min – Wall push-ups\n")
        self.text.insert(tk.END, "1 min – Alternating lunges or step-ups\n")
        self.text.insert(tk.END, "1 min – Deep breathing and stretching\n")

    def on_show(self):
        self.update_images_for_goal()

    def update_theme(self, bg, fg):
        self.configure(bg=bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except tk.TclError:
                pass
        self.goal_label.configure(bg=bg, fg=fg)
        self.workout_title.configure(bg=bg, fg="#333333")
        self.meal_title.configure(bg=bg, fg="#333333")
        self.workout_label.configure(bg=bg)
        self.meal_label.configure(bg=bg)
        self.text.configure(bg="#f9f9f9", fg=fg)
