#these lines below is for import.
#tinker imports for gui (buttons, labels, textbooks)
#the messegebox is for displaying popup errors such as (at least 3 characters for password)
#json imports for saving or loading data and import os for checking if the file exists
import tkinter as tk
from tkinter import messagebox
import json
import os

PROFILE_FILE = "profile_data.json"

#this below code is creating the profilepage class. the controller is for the workking application which can be used to access user+profile data

class ProfilePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller
        #this code below is for the page title 
        tk.Label(
            self,
            text="Profile & Body Details",
            font=("Arial", 22, "bold"),
            fg="#2E8B57",
            bg="white"
        ).grid(row=0, column=0, columnspan=2, pady=20)

        # these below are the variables for creating tinker
        self.name_var = tk.StringVar()
        self.age_var = tk.StringVar()
        self.weight_var = tk.StringVar()
        self.height_var = tk.StringVar()
        self.body_type_var = tk.StringVar(value="Ectomorph")
        self.goal_var = tk.StringVar(value="Gain Weight")

        # these codes below are for the input feilds in the profile page
        fields = [
            ("Name:", self.name_var),
            ("Age (years):", self.age_var),
            ("Weight (kg):", self.weight_var),
            ("Height (cm):", self.height_var),
        ]

        # this code below lopps through the feilds +
        row = 1
        for label, var in fields:
            tk.Label(self, text=label, font=("Arial", 12), bg="white").grid(
                row=row, column=0, sticky="e", padx=10, pady=8
            )
            tk.Entry(self, textvariable=var, width=30).grid(
                row=row, column=1, padx=10, pady=8
            )
            row += 1

        # this option creates the dropdown menu while user can chose the body type
        tk.Label(self, text="Body Type:", font=("Arial", 12), bg="white").grid(
            row=row, column=0, sticky="e", padx=10, pady=8
        )
        tk.OptionMenu(self, self.body_type_var, "Ectomorph", "Mesomorph", "Endomorph").grid(
            row=row, column=1, pady=8, sticky="w"
        )
        row += 1

        # These are the options buttons for selecting goal 
        tk.Label(self, text="Goal:", font=("Arial", 12), bg="white").grid(
            row=row, column=0, sticky="ne", padx=10, pady=8
        )

        goals = [
            "Gain Weight",
            "Reduce weight through workout",
            "My weight is perfect, just want to maintain",
        ]

        goal_frame = tk.Frame(self, bg="white")
        goal_frame.grid(row=row, column=1, sticky="w")
        for g in goals:
            tk.Radiobutton(
                goal_frame,
                text=g,
                variable=self.goal_var,
                value=g,
                bg="white"
            ).pack(anchor="w")

        row += 1

        # this displays the bmi result 
        self.bmi_label = tk.Label(
            self,
            text="",
            font=("Arial", 14, "bold"),
            bg="white",
            fg="#2E8B57"
        )
        self.bmi_label.grid(row=row, column=0, columnspan=2, pady=10)

        # this code calculates the bmi
        row += 1
        tk.Button(
            self,
            text="Calculate BMI",
            font=("Arial", 14, "bold"),
            bg="#2E8B57",
            fg="white",
            width=15,
            command=self.calculate_bmi
        ).grid(row=row, column=0, columnspan=2, pady=20)

        # the self load loads data from the 3rd page 
        self.load_profile()

    # process of loading the data from jason file from the data entered from 3rd page 
    def load_profile(self):
        """
        1) Start with data from the 3rd page (controller.profile)
        2) If profile_data.json exists, merge it
           (3rd page values override older JSON)
        3) Fill the input fields
        """
        # collects the data from first page for name
        data = dict(getattr(self.controller, "profile", {}))

        # 2) collects the data from json
        if os.path.exists(PROFILE_FILE):
            try:
                with open(PROFILE_FILE, "r") as f:
                    json_data = json.load(f)
                # JSON first, then override with current profile
                data = {**json_data, **data}
            except Exception:
                pass

        # 3) this data fills the informations
        default_name = getattr(self.controller, "current_user", "") or "User"

        self.name_var.set(data.get("name", default_name))
        self.age_var.set(data.get("age", ""))
        self.weight_var.set(data.get("weight", ""))
        self.height_var.set(data.get("height", ""))
        self.body_type_var.set(data.get("body_type", "Ectomorph"))
        self.goal_var.set(data.get("goal", "Gain Weight"))

    # these codes are for the calculations of bmi
    def calculate_bmi(self):
        try:
            weight = float(self.weight_var.get())
            height_cm = float(self.height_var.get())
            height_m = height_cm / 100.0

            bmi = weight / (height_m ** 2)
            bmi = round(bmi, 2)

            if bmi < 18.5:
                status = "Underweight"
            elif bmi < 25:
                status = "Normal"
            elif bmi < 30:
                status = "Overweight"
            else:
                status = "Obese"

            self.bmi_label.config(text=f"BMI: {bmi}  ({status})")

            # this code save updated profile 
            self.save_profile()

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numeric weight and height.")

    # this code is for saving informations on json file
    def save_profile(self):
        data = {
            "name": self.name_var.get(),
            "age": self.age_var.get(),
            "weight": self.weight_var.get(),
            "height": self.height_var.get(),
            "body_type": self.body_type_var.get(),
            "goal": self.goal_var.get(),
        }

        # this code keeps the controller copy updated so Dashboard can use it
        self.controller.profile = data

        try:
            with open(PROFILE_FILE, "w") as f:
                json.dump(data, f)
        except Exception:
            pass
