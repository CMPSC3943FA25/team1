import tkinter as tk
from tkinter import messagebox


class DietPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.light_bg)
        self.controller = controller
        self.entries = []

        title = tk.Label(
            self,
            text="Diet & Snack Tracking",
            font=("Arial", 20, "bold"),
            bg=controller.light_bg,
            fg="#2E8B57"
        )
        title.grid(row=0, column=0, columnspan=3, pady=(15, 5), padx=20, sticky="w")

        subtitle = tk.Label(
            self,
            text="Log what you eat and see your daily calories.",
            font=("Arial", 11),
            bg=controller.light_bg,
            fg=controller.light_fg
        )
        subtitle.grid(row=1, column=0, columnspan=3, padx=20, sticky="w")

        tk.Label(self, text="Meal / Snack:", font=("Arial", 11), bg=controller.light_bg, fg=controller.light_fg).grid(row=2, column=0, sticky="e", padx=10, pady=5)
        tk.Label(self, text="Calories:", font=("Arial", 11), bg=controller.light_bg, fg=controller.light_fg).grid(row=3, column=0, sticky="e", padx=10, pady=5)

        self.meal_entry = tk.Entry(self, width=30, font=("Arial", 11))
        self.meal_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
        self.cal_entry = tk.Entry(self, width=10, font=("Arial", 11))
        self.cal_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        add_btn = tk.Button(
            self,
            text="Add Entry",
            command=self.add_entry,
            bg="#2E8B57",
            fg="white",
            font=("Arial", 11, "bold")
        )
        add_btn.grid(row=2, column=2, rowspan=2, padx=10, pady=5)

        self.listbox = tk.Listbox(self, width=60, height=8, font=("Arial", 10))
        self.listbox.grid(row=4, column=0, columnspan=3, padx=20, pady=10, sticky="w")

        self.total_var = tk.StringVar(value="Total today: 0 kcal")
        total_label = tk.Label(self, textvariable=self.total_var, font=("Arial", 11, "bold"), bg=controller.light_bg, fg=controller.light_fg)
        total_label.grid(row=5, column=0, columnspan=3, padx=20, sticky="w")

        self.snack_label = tk.Label(
            self,
            text="Healthy snack ideas: apple slices with peanut butter, Greek yogurt, handful of nuts.",
            font=("Arial", 10),
            bg=controller.light_bg,
            fg="#555555",
            wraplength=550,
            justify="left"
        )
        self.snack_label.grid(row=6, column=0, columnspan=3, padx=20, pady=(5, 10), sticky="w")

        self.grid_columnconfigure(1, weight=1)

    def add_entry(self):
        meal = self.meal_entry.get().strip()
        if not meal:
            messagebox.showerror("Missing Meal", "Enter a meal or snack name.")
            return
        try:
            calories = int(self.cal_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Calories", "Calories should be a whole number.")
            return
        self.entries.append((meal, calories))
        self.listbox.insert(tk.END, f"{meal} – {calories} kcal")
        total = sum(c for _, c in self.entries)
        self.total_var.set(f"Total today: {total} kcal")
        self.meal_entry.delete(0, tk.END)
        self.cal_entry.delete(0, tk.END)

    def update_theme(self, bg, fg):
        self.configure(bg=bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except tk.TclError:
                pass
        self.listbox.configure(bg="white", fg=fg)
