import tkinter as tk
import datetime
import random


class MotivationPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=controller.light_bg)
        self.controller = controller
        self.mood_log = []

        title = tk.Label(
            self,
            text="Motivation, Breathing, and Mood",
            font=("Arial", 20, "bold"),
            bg=controller.light_bg,
            fg="#2E8B57"
        )
        title.pack(pady=(15, 5))

        self.quote_label = tk.Label(
            self,
            text="Tap the button to see a motivational quote.",
            font=("Arial", 12),
            bg=controller.light_bg,
            fg=controller.light_fg,
            wraplength=600,
            justify="center"
        )
        self.quote_label.pack(pady=5)

        tk.Button(
            self,
            text="Show Quote",
            command=self.show_quote,
            bg="#2E8B57",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=4
        ).pack(pady=4)

        self.breath_label = tk.Label(
            self,
            text="Tap the button for a quick breathing tip.",
            font=("Arial", 12),
            bg=controller.light_bg,
            fg=controller.light_fg,
            wraplength=600,
            justify="center"
        )
        self.breath_label.pack(pady=5)

        tk.Button(
            self,
            text="Breathing Tip",
            command=self.show_breath_tip,
            bg="#4682B4",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=10,
            pady=4
        ).pack(pady=4)

        mood_frame = tk.Frame(self, bg=controller.light_bg)
        mood_frame.pack(pady=10)

        mood_title = tk.Label(
            mood_frame,
            text="How do you feel today?",
            font=("Arial", 12, "bold"),
            bg=controller.light_bg,
            fg=controller.light_fg
        )
        mood_title.grid(row=0, column=0, columnspan=4, pady=(0, 5))

        moods = ["Relaxed", "Tired", "Stressed", "Proud"]
        for i, mood in enumerate(moods):
            tk.Button(
                mood_frame,
                text=mood,
                command=lambda m=mood: self.log_mood(m),
                bg="#f5f5f5",
                fg=controller.light_fg,
                font=("Arial", 10),
                width=10
            ).grid(row=1, column=i, padx=4, pady=3)

        self.mood_history_label = tk.Label(
            self,
            text="Your recent moods will appear here.",
            font=("Arial", 10),
            bg=controller.light_bg,
            fg="#555555",
            wraplength=600,
            justify="center"
        )
        self.mood_history_label.pack(pady=8)

        self.small_win_label = tk.Label(
            self,
            text="Small wins matter. Opening this app today is already progress.",
            font=("Arial", 11, "italic"),
            bg=controller.light_bg,
            fg="#555555",
            wraplength=600,
            justify="center"
        )
        self.small_win_label.pack(pady=10)

        self.quotes = [
            "Small steps every day lead to big changes.",
            "You do not have to be perfect, just consistent.",
            "Showing up for yourself today is a victory.",
            "Your body is your lifelong home. Treat it with kindness.",
            "Progress happens quietly, one choice at a time."
        ]

        self.breath_tips = [
            "Inhale through your nose for 4 seconds, hold for 4, exhale for 6.",
            "Close your eyes, relax your shoulders, and take 5 slow deep breaths.",
            "Breathe in for 3 seconds and out for 5, ten times.",
            "Try box breathing: inhale 4, hold 4, exhale 4, hold 4.",
            "Place a hand on your belly and breathe so it gently rises and falls."
        ]

    def show_quote(self):
        self.quote_label.config(text=random.choice(self.quotes))

    def show_breath_tip(self):
        self.breath_label.config(text=random.choice(self.breath_tips))

    def log_mood(self, mood):
        today = datetime.date.today().strftime("%b %d")
        self.mood_log.append((today, mood))
        last = self.mood_log[-5:]
        text = "Recent moods:\n"
        for d, m in last:
            text += f"{d}: {m}\n"
        self.mood_history_label.config(text=text)

    def update_theme(self, bg, fg):
        self.configure(bg=bg)
        for child in self.winfo_children():
            try:
                child.configure(bg=bg, fg=fg)
            except tk.TclError:
                pass
        self.small_win_label.configure(bg=bg, fg="#555555")
        self.mood_history_label.configure(bg=bg, fg="#555555")
