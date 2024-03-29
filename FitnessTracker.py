from calendar import c
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import datetime
import os
import math
from turtle import st
import pandas as pd
import matplotlib.pyplot as plt
import time

def CalculateWeightLoss(BodyFatPercent, BodyFatPercentGoal, BodyFatPercentLossPerWeek, Weight):
    # Calculate body fat in pounds
    BodyFatInPounds = round(Weight * (BodyFatPercent / 100),1)
    
    # Calculate Lean Body Mass
    LeanBodyMass = round(Weight * (1 - BodyFatPercent / 100),1)
    
    # Calculate the percentage of body fat to lose
    BodyFatPercentToLose = round(BodyFatPercent - BodyFatPercentGoal,1)
    
    # Calculate total weight to loose
    TotalWeightToLose = round(Weight * (BodyFatPercentToLose / 100),1)
    
    # Calculate target weight
    TargetWeight = round(Weight - TotalWeightToLose,1)
    
    # Calculate body fat pounds loss per week
    BodyFatPoundsLossPerWeek = math.floor(Weight * (BodyFatPercentLossPerWeek / 100))
    
    # Calculate how many weeks it will take to loose that weight
    WeeksToGoal = math.ceil(TotalWeightToLose / BodyFatPoundsLossPerWeek)
    
    # Return the results
    return {'Fat lbs': [BodyFatInPounds, 'lbs'], 
            'Lean lbs': [LeanBodyMass, 'lbs'], 
            'Fat % to Loose': [BodyFatPercentToLose, '%'], 
            'Lbs to loose': [TotalWeightToLose, 'lbs'], 
            'Target lbs': [TargetWeight, 'lbs'],
            'Fat lbs per week': [BodyFatPoundsLossPerWeek, 'lbs/week'], 
            'Weeks': [WeeksToGoal, 'weeks']}
    
def CalculateActivityMultiplier(DaysOfTrainingPerWeek):
    # Nodays of training per week
    if DaysOfTrainingPerWeek == 0:
        return 1.2
    
    # Light activity
    elif 1 <= DaysOfTrainingPerWeek <= 3:
        return 1.375
    
    # Moderate activity
    elif 4 <= DaysOfTrainingPerWeek <= 5:
        return 1.55
    
    # Heavy activity
    elif 6 <= DaysOfTrainingPerWeek <= 7:
        return 1.725
    
    # Athlete
    else:
        return 1.95

def CalculateMaintenanceCalories(Age, Weight, Height, DaysOfTrainingPerWeek, Gender):
    # Variables
    BMR = 0

    # Convert weight from pounds to kilograms
    Weight_kg = Weight / 2.20462
    
    # Convert height from inches to centimeters
    Height_cm = Height * 2.54
    
    # Calculate BMR
    if Gender.lower() == 'male':
        BMR = math.floor(10 * Weight_kg + 6.25 * Height_cm - 5 * Age + 5)
    elif Gender.lower() == 'female':
        BMR = math.floor(10 * Weight_kg + 6.25 * Height_cm - 5 * Age - 161)
        
    # Calculate BMI
    bmi = round(Weight_kg / ((Height_cm / 100) ** 2),1)
    
    # Calculate Activity Multiplier
    ActivityMultiplier = CalculateActivityMultiplier(DaysOfTrainingPerWeek)
    
    # Calculate Maintenance Calories
    MaintenanceCalories = math.floor(BMR * ActivityMultiplier)
    
    # Return the results
    return {'BMI':[bmi,'kg/m^2'],
            'BMR': [BMR, 'calories/day'],
            'Multiplier': [ActivityMultiplier, 'x'],
            'Maintenace cal': [MaintenanceCalories, 'calories/day']}

def CalculateCaloricDeficit(MaintenanceCalories, PoundsToLosePerWeek, ProteinPercentage, CarbsPercentage, FatPercentage):    
    # Calculate the caloric deficit
    CaloriesToLosePerPound = 3500
    TargetCaloricDeficit = math.floor(PoundsToLosePerWeek * CaloriesToLosePerPound / 7)
    
    # Calculate calories per day
    CaloriesPerDay = math.floor(MaintenanceCalories - TargetCaloricDeficit)

    ProteinGrams = math.floor((CaloriesPerDay * (ProteinPercentage / 100)) / 4)
    CarbsGrams = math.floor((CaloriesPerDay * (CarbsPercentage / 100)) / 4)
    FatGrams = math.floor((CaloriesPerDay * (FatPercentage / 100)) / 9)

    # Return the results
    return {'Target deficit': [TargetCaloricDeficit, 'calories/day'],
            'Calories/Day': [CaloriesPerDay, 'calories/day'],
            'Protein': [ProteinGrams, 'g/day'],
            'Carbs': [CarbsGrams, 'g/day'],
            'Fats': [FatGrams, 'g/day']}
    
def GetEntries():
    Entries = {}
    try:
        Entries['Name'] = [NameEntry.get().strip(), '']
        if not Entries['Name'][0]:
            raise ValueError("Name is required.")
        Entries['Gender'] = [GenderVar.get().lower(), '']
        if Entries['Gender'][0] not in ['male', 'female']:
            raise ValueError("Gender must be 'Male' or 'Female'.")
        try:
            Entries['Age'] = [int(AgeEntry.get()), 'years']
        except ValueError:
            raise ValueError("Invalid input for Age.")
        try:
            Entries['Weight'] = [float(WeightEntry.get()), 'lbs']
        except ValueError:
            raise ValueError("Invalid input for Weight.")
        try:
            Entries['Height'] = [int(HeightEntry.get()), 'inches']
        except ValueError:
            raise ValueError("Invalid input for Height.")
        try:
            Entries['Days Of Training Per Week'] = [int(DaysOfTrainingEntry.get()), 'days']
        except ValueError:
            raise ValueError("Invalid input for Days of Training Per Week.")
        try:
            Entries['Body Fat Percent'] = [float(BodyFatPercentEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Body Fat Percent.")
        try:
            Entries['Body Fat Percent Goal'] = [float(BodyFatPercentGoalEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Body Fat Percent Goal.")
        try:
            Entries['Body Fat Percent Loss Per Week'] = [float(BodyFatPercentLossPerWeekEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Body Fat Percent Loss Per Week.")
        try:
            Entries['Protein Percent'] = [float(ProteinPercentEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Protein Percent.")
        try:
            Entries['Carbs Percent'] = [float(CarbsPercentEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Carbs Percent.")
        try:
            Entries['Fats Percent'] = [float(FatsPercentEntry.get().rstrip('%')), '%']
        except ValueError:
            raise ValueError("Invalid input for Fats Percent.")

        # Perform validations
        if Entries['Age'][0] <= 0:
            raise ValueError("Age must be a positive integer.")
        if Entries['Weight'][0] <= 0:
            raise ValueError("Weight must be a positive number.")
        if Entries['Height'][0] <= 0:
            raise ValueError("Height must be a positive number.")
        if not 0 <= Entries['Body Fat Percent'][0] <= 100:
            raise ValueError("Body Fat Percentage must be between 0 and 100.")
        if not 0 <= Entries['Body Fat Percent Goal'][0] <= 100:
            raise ValueError("Body Fat Percent Goal must be between 0 and 100.")
        if Entries['Body Fat Percent Loss Per Week'][0] <= 0:
            raise ValueError("Body Fat Percent Loss Per Week must be a positive number.")
        if not 0 <= Entries['Days Of Training Per Week'][0] <= 7:
            raise ValueError("Days of Training Per Week must be between 0 and 7.")
        if not 0 <= Entries['Protein Percent'][0] <= 100:
            raise ValueError("Protein Percent must be between 0 and 100.")
        if not 0 <= Entries['Carbs Percent'][0] <= 100:
            raise ValueError("Carbs Percent must be between 0 and 100.")
        if not 0 <= Entries['Fats Percent'][0] <= 100:
            raise ValueError("Fats Percent must be between 0 and 100.")
        total_percent = Entries['Protein Percent'][0] + Entries['Carbs Percent'][0] + Entries['Fats Percent'][0]
        if total_percent != 100:
            raise ValueError("The sum of Protein Percent, Carbs Percent, and Fats Percent must be 100.")

    except ValueError as e:
        messagebox.showerror("Input Error", str(e))
        Entries = {}
        
    # Return the results
    return Entries

def UpdateCalculations():
    # Get values from entry fields
    Entries = GetEntries()
    
    # Check if Entries is empty
    if not Entries:
        return
    
    # Get current date
    CurrentDate = {'Date':[datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), '']}
    
    # Perform calculations
    WeightLoss = CalculateWeightLoss(Entries['Body Fat Percent'][0], Entries['Body Fat Percent Goal'][0], Entries['Body Fat Percent Loss Per Week'][0], Entries['Weight'][0])
    MaintenenceCalories = CalculateMaintenanceCalories(Entries['Age'][0], Entries['Weight'][0], Entries['Height'][0], Entries['Days Of Training Per Week'][0], Entries['Gender'][0])
    CaloricDeficit = CalculateCaloricDeficit(MaintenenceCalories['Maintenace cal'][0], WeightLoss['Fat lbs per week'][0],Entries['Protein Percent'][0],Entries['Carbs Percent'][0],Entries['Fats Percent'][0]
)    
    # Create a new dictionary and update it with the other dictionaries
    Data.update(CurrentDate)
    Data.update(Entries)
    Data.update(WeightLoss)
    Data.update(MaintenenceCalories)
    Data.update(CaloricDeficit)
    
    # Update the results text box
    UpdateResultsText()
    
    # Enable the Macros and Foods tabs if Name is not empty
    if Data['Name'][0]:
        notebook.tab(MacrosFrame, state='normal')
        notebook.tab(FoodsFrame, state='normal')
        notebook.tab(DashboardFrame, state="normal")
    else:
        notebook.tab(MacrosFrame, state='disabled')
        notebook.tab(FoodsFrame, state='disabled')
        notebook.tab(DashboardFrame, state="disabled")

def SaveResults():
    # Check if Data is empty
    if not Data:
        messagebox.showerror("Error", "Data is empty.")
        return
    
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Calculation.csv"
    
    # Check if 'Results' directory exists, if not, create it
    if not os.path.exists('Results'):
        os.makedirs('Results')

    # Check if file exists, if not, create it and write headers
    if not os.path.isfile(FileName):
        with open(FileName, 'w') as file:
            file.write("Date,"
                        "Name,"
                        "Gender,"
                        "Age,"
                        "Weight,"
                        "Height,"
                        "Days Of Training Per Week,"
                        "Body Fat Percent,"
                        "Body Fat Percent Goal,"
                        "Body Fat Percent Loss Per Week,"
                        "Protein Percent,"
                        "Carbs Percent,"
                        "Fats Percent,"
                        "Fat Percent to Loose,"
                        "Fat lbs,"
                        "Lean lbs,"
                        "Fat lbs per week,"
                        "Lbs to loose,"
                        "Target lbs,"
                        "Weeks,"
                        "BMI,"
                        "BMR,"
                        "Multiplier,"
                        "Maintenace cal,"
                        "Target deficit,"
                        "Calories/Day,"
                        "Protein,"
                        "Carbs,"
                        "Fats\n")
    
    # Write results to the file
    with open(FileName, 'a') as file:
        file.write((f"{Data['Date'][0]},"
                    f"{Data['Name'][0]},"
                    f"{Data['Gender'][0]},"
                    f"{Data['Age'][0]},"
                    f"{Data['Weight'][0]},"
                    f"{Data['Height'][0]},"
                    f"{Data['Days Of Training Per Week'][0]},"
                    f"{Data['Body Fat Percent'][0]},"
                    f"{Data['Body Fat Percent Goal'][0]},"
                    f"{Data['Body Fat Percent Loss Per Week'][0]},"
                    f"{Data['Protein Percent'][0]},"
                    f"{Data['Carbs Percent'][0]},"
                    f"{Data['Fats Percent'][0]},"
                    f"{Data['Fat % to Loose'][0]},"
                    f"{Data['Fat lbs'][0]},"
                    f"{Data['Lean lbs'][0]},"
                    f"{Data['Fat lbs per week'][0]},"
                    f"{Data['Lbs to loose'][0]},"
                    f"{Data['Target lbs'][0]},"
                    f"{Data['Weeks'][0]},"
                    f"{Data['BMI'][0]},"
                    f"{Data['BMR'][0]},"
                    f"{Data['Multiplier'][0]},"
                    f"{Data['Maintenace cal'][0]},"
                    f"{Data['Target deficit'][0]},"
                    f"{Data['Calories/Day'][0]},"
                    f"{Data['Protein'][0]},"
                    f"{Data['Carbs'][0]},"
                    f"{Data['Fats'][0]}\n"))

    # Show message box
    messagebox.showinfo("Saved", "Results and table image saved successfully!")
    
def CheckExistingData():
    # Check if 'Results' directory exists and has files
    if os.path.exists('Results') and os.listdir('Results'):
        response = messagebox.askyesno("Open File", "Existing data files found. Do you want to open an existing file?")
        if response:
            # Open file dialog to select a file
            file_path = filedialog.askopenfilename(initialdir='Results', title='Select file', filetypes=[("CSV files", "*-Calculation.csv")])
            if file_path:
                # Read the CSV file
                df = pd.read_csv(file_path)

                # Check if the DataFrame is not empty
                if not df.empty:
                    # Extract the last row
                    last_row = df.iloc[-1]

                    # Update the UI fields
                    NameEntry.set(str(last_row['Name']))
                    GenderVar.set(str(last_row['Gender']))
                    AgeEntry.set(str(last_row['Age']))
                    WeightEntry.set(str(last_row['Weight']))
                    HeightEntry.set(str(last_row['Height']))
                    DaysOfTrainingEntry.set(str(last_row['Days Of Training Per Week']))
                    BodyFatPercentEntry.set(f"{last_row['Body Fat Percent']}%")
                    BodyFatPercentGoalEntry.set(f"{last_row['Body Fat Percent Goal']}%")
                    BodyFatPercentLossPerWeekEntry.set(f"{last_row['Body Fat Percent Loss Per Week']}%")
                    ProteinPercentEntry.set(f"{last_row['Protein Percent']}%")
                    CarbsPercentEntry.set(f"{last_row['Carbs Percent']}%")
                    FatsPercentEntry.set(f"{last_row['Fats Percent']}%")
                    
                    # Force A calculation
                    UpdateCalculations()
                
                # Load and Populate Foods Data
                foods_file = file_path.replace('Calculation.csv', 'Foods.csv')
                if os.path.isfile(foods_file):
                    load_and_populate_foods(foods_file)
                    update_food_type_entry()
                    
                # Load and Populate Macros Data
                macros_file = file_path.replace('Calculation.csv', 'Macros.csv')
                if os.path.isfile(macros_file):
                    load_and_populate_macros(macros_file)

def load_and_populate_foods(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        food_table.insert('', 'end', values=list(row))
    alternate_row_colors()
    
def load_and_populate_macros(file_path):
    df = pd.read_csv(file_path)
    for _, row in df.iterrows():
        macros_table.insert('', 'end', values=list(row))

def UpdateResultsText():
    # Temporarily enable the widget to modify its content
    ResultsText.config(state=tk.NORMAL)

    # Clear the text box
    ResultsText.delete('1.0', tk.END)

    # Define the order of keys
    KeysOrder = ['Date', 'Weight', 'Height', 'Body Fat Percent', 'Fat % to Loose', 'Fat lbs', 
                 'Lean lbs', 'Fat lbs per week', 'Lbs to loose', 'Target lbs', 
                 'Days Of Training Per Week', 'Weeks', 'BMI', 'BMR', 'Multiplier', 'Maintenace cal', 
                 'Target deficit', 'Calories/Day', 'Protein', 'Carbs', 'Fats']

    # Convert all values to strings and append the unit of measure
    StrValues = []
    for key in KeysOrder:
        value = Data.get(key, ['N/A', ''])
        if isinstance(value, list):
            str_value = str(value[0]) + ' ' + value[1]
        else:
            str_value = str(value)
        StrValues.append(str_value)

    # Determine the maximum key length
    MaxKeyLength = max(len(key) for key in KeysOrder)

    # Iterate over the keys in the specified order and format each key-value pair
    for key, value in zip(KeysOrder, StrValues):
        line = f"{key.ljust(MaxKeyLength)}  -> {value}\n"
        
        # Insert the formatted line into the text box
        ResultsText.insert(tk.END, line)

    # Disable the widget to prevent user editing
    ResultsText.config(state=tk.DISABLED)
        
def AddPercent(*args, var):
        text = var.get()
        if len(text) > 0 and text[-1] != '%':
            var.set(text + '%')
            
def save_table_to_csv():
    # Create a list to hold the data
    data_to_save = []
    for item in food_table.get_children():
        data_to_save.append(food_table.item(item)['values'])
    
    # Convert the list to a DataFrame and save as CSV
    df = pd.DataFrame(data_to_save, columns=["name", "unit", "quantity", "calories", "protein", "carbs", "fats"])
    
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Foods.csv"
    df.to_csv(FileName, index=False)

def sort_table():
    # Retrieve all the items in the table
    data = [(food_table.item(item_id)["values"]) for item_id in food_table.get_children('')]
    # Sort the data by the food name (1st column)
    data.sort(key=lambda x: x[0].lower())

    # Clear current items in the table
    for item in food_table.get_children():
        food_table.delete(item)

    # Reinsert the sorted items
    for item in data:
        food_table.insert('', 'end', values=list(item))

def add_food():
    # Extract values from entry fields
    food_name = FoodNameVar.get().strip()
    food_unit = FoodUnitVar.get().strip()
    food_measurement = FoodMeasurementVar.get().strip()
    food_calories = FoodCaloriesVar.get().strip()
    food_protein = FoodProteinVar.get().strip()
    food_carbs = FoodCarbsVar.get().strip()
    food_fats = FoodFatsVar.get().strip()

    # Check if any field is empty
    if not all([food_name, food_unit, food_measurement, food_calories, food_protein, food_carbs, food_fats]):
        messagebox.showwarning("Warning", "Please fill in all fields before adding a food item.")
        return

    # If all fields are filled, add the food item to the table
    food_data = {
        "name": food_name,
        "unit": food_unit,
        "quantity": food_measurement,
        "calories": food_calories,
        "protein": food_protein,
        "carbs": food_carbs,
        "fats": food_fats
    }

    # Add the food data to the table
    food_table.insert('', 'end', values=list(food_data.values()))

    # Sort the table and save it to a CSV file
    sort_table()
    save_table_to_csv()
    alternate_row_colors()
    update_food_type_entry()

    # Clear input fields or reset them to default values
    FoodNameVar.set("")
    FoodUnitVar.set("")
    FoodMeasurementVar.set("")
    FoodCaloriesVar.set("")
    FoodProteinVar.set("")
    FoodCarbsVar.set("")
    FoodFatsVar.set("")

def remove_selected_food():
    selected_items = food_table.selection()
    if selected_items:
        for item_id in selected_items:
            food_table.delete(item_id)
        sort_table()
        save_table_to_csv()
        alternate_row_colors()
        update_food_type_entry()
        
def alternate_row_colors():
    for index, item in enumerate(food_table.get_children()):
        if index % 2 == 0:
            food_table.item(item, tags=('evenrow',))
        else:
            food_table.item(item, tags=('oddrow',))
            
def update_food_type_entry():
    food_names = [food_table.item(item_id)['values'][0] for item_id in food_table.get_children()]
    FoodTypeEntry['values'] = food_names
    
def add_to_macros():
    time = TimeVar.get()
    food_name = FoodTypeVar.get()
    quantity = QuantityVar.get()

    if not all([time, food_name, quantity]):
        messagebox.showwarning("Warning", "Please fill in all fields")
        return

    # Find the selected food in the Foods table
    for item_id in food_table.get_children():
        if food_table.item(item_id)['values'][0] == food_name:
            food_data = food_table.item(item_id)['values']
            break
    else:
        messagebox.showerror("Error", "Selected food not found in Foods table")
        return

    try:
        quantity = float(quantity)  # Convert quantity to a number
    except ValueError:
        messagebox.showerror("Error", "Invalid quantity")
        return

    # Calculate nutritional values
    measurement, calories, protein, carbs, fats = food_data[2:]  # Skip name and unit columns
    # Calculate nutritional values and format them to one decimal place
    calories = round((float(calories) * quantity) / float(measurement), 1)
    protein = round((float(protein) * quantity) / float(measurement), 1)
    carbs = round((float(carbs) * quantity) / float(measurement), 1)
    fats = round((float(fats) * quantity) / float(measurement), 1)


    # Add data to macros table (including the unit)
    unit = food_data[1]  # Get the unit from the selected food
    macros_table.insert('', 'end', values=(time, food_name, unit, quantity, calories, protein, carbs, fats), tags=('evenrow', 'oddrow')[(len(macros_table.get_children()) % 2)])
    
    # Clear input fields or reset them to default values
    TimeVar.set("")
    FoodTypeVar.set("")
    QuantityVar.set("")

    # Update the preview labels
    PreviewCaloriesVar.set(f"Calories  ")
    PreviewProteinVar.set(f"Protein   ")
    PreviewCarbsVar.set(f"Carbs     ")
    PreviewFatsVar.set(f"Fats      ")

    # Update the summary table
    sort_macros_table()
    update_summary_table()
    save_macros_to_csv()
    
def on_food_select(event):
    # Get the selected food name
    food_name = FoodTypeVar.get()

    # Find the unit for the selected food
    for item_id in food_table.get_children():
        if food_table.item(item_id)['values'][0] == food_name:
            unit = food_table.item(item_id)['values'][1]
            UnitLabel.config(text=f"{unit}")
            break
    else:
        UnitLabel.config(text="Unit not found")
    update_nutritional_preview()

def update_nutritional_preview(*args):
    food_name = FoodTypeVar.get()
    quantity = QuantityVar.get()

    if not food_name or not quantity:
        return  # Exit if food is not selected or quantity is empty

    try:
        quantity = float(quantity)
    except ValueError:
        return  # Exit if quantity is not a number

    # Find the selected food in the Foods table
    for item_id in food_table.get_children():
        if food_table.item(item_id)['values'][0] == food_name:
            measurement, calories, protein, carbs, fats = food_table.item(item_id)['values'][2:]
            break
    else:
        return  # Exit if selected food not found

    # Calculate nutritional values
    calories = (float(calories) * quantity) / float(measurement)
    protein = (float(protein) * quantity) / float(measurement)
    carbs = (float(carbs) * quantity) / float(measurement)
    fats = (float(fats) * quantity) / float(measurement)

    # Update the preview labels
    PreviewCaloriesVar.set(f"Calories  {calories:.2f}g")
    PreviewProteinVar.set(f"Protein   {protein:.2f}g")
    PreviewCarbsVar.set(f"Carbs     {carbs:.2f}g")
    PreviewFatsVar.set(f"Fats      {fats:.2f}g")
        
def delete_selected_from_macros():
    selected_items = macros_table.selection()
    if selected_items:
        for item in selected_items:
            macros_table.delete(item)
    else:
        messagebox.showwarning("Warning", "No item selected")
    sort_macros_table()
    update_summary_table()
    save_macros_to_csv()
        
def get_target_values():
    targets = {
        'Calories': Data.get('Calories/Day', [0])[0],
        'Proteins (g)': Data.get('Protein', [0])[0],
        'Carbs (g)': Data.get('Carbs', [0])[0],
        'Fats (g)': Data.get('Fats', [0])[0]
    }
    return targets

def calculate_actuals():
    actuals = {'Calories': 0.0, 'Proteins (g)': 0.0, 'Carbs (g)': 0.0, 'Fats (g)': 0.0}
    for item in macros_table.get_children():
        values = macros_table.item(item, 'values')
        actuals['Calories'] += float(values[4])
        actuals['Proteins (g)'] += float(values[5])
        actuals['Carbs (g)'] += float(values[6])
        actuals['Fats (g)'] += float(values[7])
    return actuals

def calculate_left(target, actuals):
    left = {
        'Calories': target['Calories'] - actuals['Calories'],
        'Proteins (g)': target['Proteins (g)'] - actuals['Proteins (g)'],
        'Carbs (g)': target['Carbs (g)'] - actuals['Carbs (g)'],
        'Fats (g)': target['Fats (g)'] - actuals['Fats (g)']
    }
    return left

def update_summary_table():
    targets = get_target_values()
    actuals = calculate_actuals()
    left = calculate_left(targets, actuals)

    # Non-local variable to store the total grams
    total_grams = 0

    # Function to calculate percentages
    def calculate_percentages(row_name, values):
        nonlocal total_grams
        protein = values['Proteins (g)'] * 4
        carbs = values['Carbs (g)'] * 4
        fats = values['Fats (g)'] * 9

        if row_name == "Target":
            total_grams = protein + carbs + fats

        if total_grams > 0:
            protein_percentage = 100 * protein / total_grams
            carbs_percentage = 100 * carbs / total_grams
            fats_percentage = 100 * fats / total_grams
        else:
            protein_percentage, carbs_percentage, fats_percentage = 0, 0, 0

        # Rounding the percentages to one decimal place
        protein_percentage = round(protein_percentage, 1)
        carbs_percentage = round(carbs_percentage, 1)
        fats_percentage = round(fats_percentage, 1)

        return protein_percentage, carbs_percentage, fats_percentage

    # Inside the update_summary_table function, when setting the values for each row
    for row_name, values in [("Target", targets), ("Actuals", actuals), ("Left", left)]:
        protein_percentage, carbs_percentage, fats_percentage = calculate_percentages(row_name, values)
        summary_table.item(summary_row_ids[row_name], values=(
            row_name,
            round(values['Calories'], 1),
            round(values['Proteins (g)'], 1),
            protein_percentage,
            round(values['Carbs (g)'], 1),
            carbs_percentage,
            round(values['Fats (g)'], 1),
            fats_percentage
        ))


    # Applying custom tags for each row
    summary_table.item(summary_row_ids['Target'], tags=('target_row', 'bold_text'))
    summary_table.item(summary_row_ids['Actuals'], tags=('actuals_row', 'bold_text'))
    summary_table.item(summary_row_ids['Left'], tags=('left_row', 'bold_text'))

def initialize():
    CheckExistingData()
    time.sleep(0.1)
    update_summary_table()

def save_macros_to_csv():
    # Create a list to hold the data
    data_to_save = []
    for item in macros_table.get_children():
        data_to_save.append(macros_table.item(item)['values'])
    
    # Convert the list to a DataFrame and save as CSV
    df = pd.DataFrame(data_to_save, columns=["Time", "Food", "Unit", "Quantity", "Calories", "Protein", "Carbs", "Fats"])
    
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Macros.csv"
    df.to_csv(FileName, index=False)
    
def on_tab_selected(event):
    selected_tab = event.widget.select()
    selected_tab_name = event.widget.tab(selected_tab, "text")
    if selected_tab_name == "Macros":
        update_summary_table()
    if selected_tab_name == "Dashboard":
        load_dashboard_data()

def edit_selected_from_macros():
    selected_items = macros_table.selection()
    if not selected_items:
        messagebox.showwarning("Warning", "No item selected for editing")
        return

    # Assume single selection for simplicity
    item_id = selected_items[0]
    selected_item = macros_table.item(item_id, 'values')

    # Pre-populate the Time and Quantity fields with selected item's details
    TimeVar.set(selected_item[0])
    FoodTypeVar.set(selected_item[1])
    QuantityVar.set(selected_item[3])

    # Disable Add button to prevent adding new items while editing
    addButton['state'] = 'disabled'
    delete_buton['state'] = 'disabled'
    # Change Edit button text to "Update" and bind it to a new function to update the item
    editButton['text'] = 'Update'
    editButton['command'] = lambda: update_selected_in_macros(item_id)

def update_selected_in_macros(item_id):
    # Validate input as necessary
    new_time = TimeVar.get()
    new_food_name = FoodTypeVar.get()
    new_quantity = QuantityVar.get()
    if not all([new_time, new_food_name, new_quantity]):
        messagebox.showwarning("Warning", "Please fill in all fields")
        return
    
    # Find the selected food in the Foods table
    for item in food_table.get_children():
        if food_table.item(item)['values'][0] == new_food_name:
            food_data = food_table.item(item)['values']
            break
    else:
        messagebox.showerror("Error", "Selected food not found in Foods table")
        return

    try:
        quantity = float(new_quantity)  # Convert quantity to a number
    except ValueError:
        messagebox.showerror("Error", "Invalid quantity")
        return

    # Calculate nutritional values
    measurement, calories, protein, carbs, fats = food_data[2:]  # Skip name and unit columns
    calories = round((float(calories) * quantity) / float(measurement), 1)
    protein = round((float(protein) * quantity) / float(measurement), 1)
    carbs = round((float(carbs) * quantity) / float(measurement), 1)
    fats = round((float(fats) * quantity) / float(measurement), 1)
    unit = food_data[1]
    new_values = (new_time, new_food_name, unit, new_quantity, calories, protein, carbs, fats)

    # Update the item in the table
    macros_table.item(item_id, values=new_values)

    # Reset UI
    addButton['state'] = 'normal'
    delete_buton['state'] = 'normal'
    editButton['text'] = 'Edit Selected'
    editButton['command'] = edit_selected_from_macros

    # Clear input fields or reset them to default values
    TimeVar.set("")
    FoodTypeVar.set("")
    QuantityVar.set("")

    # Update the preview labels
    PreviewCaloriesVar.set(f"Calories  ")
    PreviewProteinVar.set(f"Protein   ")
    PreviewCarbsVar.set(f"Carbs     ")
    PreviewFatsVar.set(f"Fats      ")

    # Update the summary table
    sort_macros_table()
    update_summary_table()
    save_macros_to_csv()

def sort_macros_table():
    # Retrieve all the items in the table
    time_of_day_order = {
        "Breakfast": 1,
        "Morning Snack": 2,
        "Lunch": 3,
        "Afternoon Snack": 4,
        "Dinner": 5,
        "Evening Snack": 6,
        "Other": 7
    }

    # Retrieve all items and their values from the table
    items_with_values = [(item_id, macros_table.item(item_id)["values"]) for item_id in macros_table.get_children('')]
    
    # Sort items based on the custom time of day order
    sorted_items = sorted(items_with_values, key=lambda x: time_of_day_order.get(x[1][0], 8))

    # Clear the table
    macros_table.delete(*macros_table.get_children())

    # Reinsert items in sorted order, ensuring values are in list format
    for item_id, values in sorted_items:
        # Ensure values are formatted as a list or tuple
        formatted_values = list(values) if isinstance(values, (list, tuple)) else []
        macros_table.insert('', 'end', values=formatted_values)

# Variables
Data = {}

# SETUP UI
root = tk.Tk()
root.title("FitnessTracker - By Carlos Finocchiaro")

# Create Notebook
notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Create Frames for each tab
CalculatorFrame = ttk.Frame(notebook)
MacrosFrame = ttk.Frame(notebook)
FoodsFrame = ttk.Frame(notebook)

# Configure grid to expand the cell where the table is located
MacrosFrame.grid_rowconfigure(1, weight=1)
MacrosFrame.grid_columnconfigure(0, weight=1)


# Add Frames to notebook as tabs
notebook.add(CalculatorFrame, text="Calculator")
notebook.add(MacrosFrame, text="Macros", state='disabled')
notebook.add(FoodsFrame, text="Foods", state='disabled')

# Variables
NameEntry = tk.StringVar()
GenderVar = tk.StringVar()
AgeEntry = tk.StringVar()
WeightEntry = tk.StringVar()
HeightEntry = tk.StringVar()
DaysOfTrainingEntry = tk.StringVar()
BodyFatPercentEntry = tk.StringVar()
BodyFatPercentGoalEntry = tk.StringVar()
BodyFatPercentLossPerWeekEntry = tk.StringVar()
ProteinPercentEntry = tk.StringVar()
CarbsPercentEntry = tk.StringVar()
FatsPercentEntry = tk.StringVar()

# Frames
InputFrame = tk.Frame(CalculatorFrame, padx=10, pady=10)
InputFrame.grid(row=0, column=0, sticky="ew")

ButtonsFrame = tk.Frame(InputFrame, padx=10, pady=10)
ButtonsFrame.grid(row=12, column=1, pady=20)

ResultsFrame = tk.Frame(CalculatorFrame, padx=20, pady=20)
ResultsFrame.grid(row=0, column=1, sticky='ew')

# Input Widgets
Font = ('Courier', 14)
Font2 = ('Courier', 12)

tk.Label(InputFrame, text="Name", font=Font2, padx=10).grid(row=0, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=NameEntry, font=Font).grid(row=0, column=1, sticky="ew")

tk.Label(InputFrame, text="Gender (Male/Female)", font=Font2, padx=10).grid(row=1, column=0, sticky="w")
menu = tk.OptionMenu(InputFrame, GenderVar, "Male", "Female")
menu.config(font=Font)
menu.grid(row=1, column=1, sticky="ew")

tk.Label(InputFrame, text="Age", font=Font2, padx=10).grid(row=2, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=AgeEntry, font=Font).grid(row=2, column=1, sticky="ew")

tk.Label(InputFrame, text="Weight (lbs)", font=Font2, padx=10).grid(row=3, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=WeightEntry, font=Font).grid(row=3, column=1, sticky="ew")

tk.Label(InputFrame, text="Height (inches)", font=Font2, padx=10).grid(row=4, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=HeightEntry, font=Font).grid(row=4, column=1, sticky="ew")

tk.Label(InputFrame, text="Days of Training Per Week", font=Font2, padx=10).grid(row=5, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=DaysOfTrainingEntry, font=Font).grid(row=5, column=1, sticky="ew")

tk.Label(InputFrame, text="Body Fat Percentage", font=Font2, padx=10).grid(row=6, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=BodyFatPercentEntry, font=Font).grid(row=6, column=1, sticky="ew")
BodyFatPercentEntry.trace_add('write', lambda *args: AddPercent(*args, var=BodyFatPercentEntry))

tk.Label(InputFrame, text="Body Fat Percent Goal", font=Font2, padx=10).grid(row=7, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=BodyFatPercentGoalEntry, font=Font).grid(row=7, column=1, sticky="ew")
BodyFatPercentGoalEntry.trace_add('write', lambda *args: AddPercent(*args, var=BodyFatPercentGoalEntry))  

tk.Label(InputFrame, text="Body Fat Percent Loss Per Week", font=Font2, padx=10).grid(row=8, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=BodyFatPercentLossPerWeekEntry, font=Font).grid(row=8, column=1, sticky="ew")
BodyFatPercentLossPerWeekEntry.trace_add('write', lambda *args: AddPercent(*args, var=BodyFatPercentLossPerWeekEntry))

tk.Label(InputFrame, text="Protein Percent", font=Font2, padx=10).grid(row=9, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=ProteinPercentEntry, font=Font).grid(row=9, column=1, sticky="ew")
ProteinPercentEntry.trace_add('write', lambda *args: AddPercent(*args, var=ProteinPercentEntry))

tk.Label(InputFrame, text="Carbs Percent", font=Font2, padx=10).grid(row=10, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=CarbsPercentEntry, font=Font).grid(row=10, column=1, sticky="ew")
CarbsPercentEntry.trace_add('write', lambda *args: AddPercent(*args, var=CarbsPercentEntry))

tk.Label(InputFrame, text="Fat Percent", font=Font2, padx=10).grid(row=11, column=0, sticky="w")
tk.Entry(InputFrame, textvariable=FatsPercentEntry, font=Font).grid(row=11, column=1, sticky="ew")
FatsPercentEntry.trace_add('write', lambda *args: AddPercent(*args, var=FatsPercentEntry))

tk.Button(ButtonsFrame, text="Calculate", command=UpdateCalculations, font=Font).pack(side=tk.LEFT, padx=10)
tk.Button(ButtonsFrame, text="Save Results", command=SaveResults, font=Font).pack(side=tk.LEFT, padx=10)

ResultsText = tk.Text(ResultsFrame, font=Font, width=55, height=21)
ResultsText.grid(row=0, column=0,sticky='nsew')

# Configure grid to expand the cell where the ResultsText is located
ResultsFrame.grid_rowconfigure(0, weight=1)
ResultsFrame.grid_columnconfigure(0, weight=1)


# Variables for food entry
FoodNameVar = tk.StringVar()
FoodUnitVar = tk.StringVar()
FoodMeasurementVar = tk.StringVar()
FoodCaloriesVar = tk.StringVar()
FoodProteinVar = tk.StringVar()
FoodCarbsVar = tk.StringVar()
FoodFatsVar = tk.StringVar()

# Food Entry Frame
FoodEntryFrame = tk.Frame(FoodsFrame, padx=10, pady=10)
FoodEntryFrame.grid(row=0, column=0, sticky="new")

# Food Entry Widgets
tk.Label(FoodEntryFrame, text="Food Name", font=Font2).grid(row=0, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodNameVar, font=Font).grid(row=0, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Unit", font=Font2).grid(row=1, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodUnitVar, font=Font).grid(row=1, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Quantity", font=Font2).grid(row=2, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodMeasurementVar, font=Font).grid(row=2, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Calories", font=Font2).grid(row=3, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodCaloriesVar, font=Font).grid(row=3, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Protein (g)", font=Font2).grid(row=4, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodProteinVar, font=Font).grid(row=4, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Carbs   (g)", font=Font2).grid(row=5, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodCarbsVar, font=Font).grid(row=5, column=1, sticky="ew")

tk.Label(FoodEntryFrame, text="Fats    (g)", font=Font2).grid(row=6, column=0, sticky="w")
tk.Entry(FoodEntryFrame, textvariable=FoodFatsVar, font=Font).grid(row=6, column=1, sticky="ew")

# Add and Remove Buttons
tk.Button(FoodEntryFrame, text="Add Food", command=add_food, font=Font).grid(row=7, column=0, padx=10, pady=10)
tk.Button(FoodEntryFrame, text="Remove Selected", command=remove_selected_food, font=Font).grid(row=7, column=1, padx=10, pady=10)

# Food Table
food_table = ttk.Treeview(FoodsFrame, columns=("name", "unit", "quantity", "calories", "protein", "carbs", "fats"), show='headings')
food_table.grid(row=0, column=1, sticky='nsew')

# Configure row tags
food_table.tag_configure('evenrow', background='#FFFFFF')  # White
food_table.tag_configure('oddrow', background='#E8E8E8')   # Light Grey

# Creating a scrollbar
scrollbar = ttk.Scrollbar(FoodsFrame, orient="vertical", command=food_table.yview)
scrollbar.grid(row=0, column=1, sticky='ens')

# Configure grid to expand the cell where the table is located
FoodsFrame.grid_rowconfigure(0, weight=1)
FoodsFrame.grid_columnconfigure(1, weight=1)

# Configuring the food_table to use the scrollbar
food_table.configure(yscrollcommand=scrollbar.set)


# Define headings
for col in food_table['columns']:
    food_table.heading(col, text=col.capitalize())

# Adjust column alignments
food_table.column("name", width=120, anchor='w')
food_table.column("unit", width=80, anchor='center')
food_table.column("quantity", width=80, anchor='center')
food_table.column("calories", width=80, anchor='center')
food_table.column("protein", width=80, anchor='center')
food_table.column("carbs", width=80, anchor='center')
food_table.column("fats", width=80, anchor='center')



# Macros Functions
# User Input Fields
MacrosInputFrame = tk.Frame(MacrosFrame, padx=10, pady=10)
MacrosInputFrame.grid(row=0, column=0, sticky="ew")

# Configure the grid for the summary table
MacrosInputFrame.grid_rowconfigure(0, weight=1)
MacrosInputFrame.grid_columnconfigure(2, weight=1)


tk.Label(MacrosInputFrame, text="Time", font=Font2).grid(row=0, column=0, sticky="w")
TimeVar = tk.StringVar()
TimeEntry = ttk.Combobox(MacrosInputFrame, textvariable=TimeVar, values=["Breakfast", "Morning Snack", "Lunch", "Afternoon Snack", "Dinner", "Evening Snack", "Other"], font=Font)
TimeEntry.grid(row=0, column=1, sticky="ew")

tk.Label(MacrosInputFrame, text="Food", font=Font2).grid(row=1, column=0, sticky="w")
FoodTypeVar = tk.StringVar()
FoodTypeEntry = ttk.Combobox(MacrosInputFrame, textvariable=FoodTypeVar, font=Font)
FoodTypeEntry.grid(row=1, column=1, sticky="ew")

tk.Label(MacrosInputFrame, text="Quantity", font=Font2).grid(row=2, column=0, sticky="w")
QuantityVar = tk.StringVar()
QuantityEntry = tk.Entry(MacrosInputFrame, textvariable=QuantityVar, font=Font)
QuantityEntry.grid(row=2, column=1, sticky="ew")

# Add a label to display the unit of measurement
UnitLabel = tk.Label(MacrosInputFrame, font=Font2)
UnitLabel.grid(row=3, column=1, sticky="w")

FoodTypeEntry.bind('<<ComboboxSelected>>', on_food_select)
def on_food_type_var_change(*args):
    on_food_select("<<ComboboxSelected>>")
FoodTypeVar.trace_add("write", on_food_type_var_change)

# Bind the tab change event
notebook.bind("<<NotebookTabChanged>>", on_tab_selected)

PreviewCaloriesVar = tk.StringVar(value="Calories ")
PreviewProteinVar = tk.StringVar(value="Protein   ")
PreviewCarbsVar = tk.StringVar(value="Carbs     ")
PreviewFatsVar = tk.StringVar(value="Fats      ")

tk.Label(MacrosInputFrame, textvariable=PreviewCaloriesVar, font=Font2).grid(row=4, column=0,columnspan=2, sticky="w")
tk.Label(MacrosInputFrame, textvariable=PreviewProteinVar, font=Font2).grid(row=5, column=0,columnspan=2, sticky="w")
tk.Label(MacrosInputFrame, textvariable=PreviewCarbsVar, font=Font2).grid(row=6, column=0,columnspan=2, sticky="w")
tk.Label(MacrosInputFrame, textvariable=PreviewFatsVar, font=Font2).grid(row=7, column=0,columnspan=2, sticky="w")

# Bind the update function to the quantity variable
QuantityVar.trace_add("write", update_nutritional_preview)


# Add Button
addButton = tk.Button(MacrosInputFrame, text="Add to Macros", command=add_to_macros, font=Font)
addButton.grid(row=8, column=0, sticky="w", padx=10, pady=10)

# Add Delete Button
delete_buton = tk.Button(MacrosInputFrame, text="Delete Selected", command=delete_selected_from_macros, font=Font)
delete_buton.grid(row=9, column=0, sticky="w", padx=10, pady=10)

# Add Edit Button
editButton = tk.Button(MacrosInputFrame, text="Edit Selected", command=edit_selected_from_macros, font=Font)
editButton.grid(row=9, column=1, sticky="w", padx=10, pady=10)


# Macros Table
macros_table = ttk.Treeview(MacrosFrame, columns=("time", "food", "unit", "quantity", "calories", "protein", "carbs", "fats"), show='headings')
macros_table.grid(row=1, column=0, sticky='nsew', padx=20, pady=10)

# Define headings
for col in macros_table['columns']:
    macros_table.heading(col, text=col.capitalize())

# Adjust column alignments
macros_table.column("time", width=100, anchor='w')
macros_table.column("food", width=120, anchor='center')
macros_table.column("unit", width=80, anchor='center')
macros_table.column("quantity", width=80, anchor='center')
macros_table.column("calories", width=80, anchor='center')
macros_table.column("protein", width=80, anchor='center')
macros_table.column("carbs", width=80, anchor='center')
macros_table.column("fats", width=80, anchor='center')

# Configure row tags for alternate row colors
macros_table.tag_configure('evenrow', background='#FFFFFF')  # White
macros_table.tag_configure('oddrow', background='#E8E8E8')   # Light Grey

# Creating a vertical scrollbar for the Macros table
macros_scrollbar = ttk.Scrollbar(MacrosFrame, orient="vertical", command=macros_table.yview)
macros_scrollbar.grid(row=1, column=1, sticky='ns')
macros_table.configure(yscrollcommand=macros_scrollbar.set)


# Create the summary table
summary_table = ttk.Treeview(MacrosInputFrame, columns=("Category", "Calories", "Proteins (g)", "Proteins (%)", "Carbs (g)", "Carbs (%)", "Fats (g)", "Fats (%)"), show='headings')
summary_table.grid(row=0, column=2, sticky='nsew',rowspan=9, padx=20)

# Customize the headers and adjust column widths
for col in summary_table['columns']:
    summary_table.heading(col, text=col.replace("_", " ").capitalize())
    if col in ["Category", "Proteins (%)", "Carbs (%)", "Fats (%)"]:
        summary_table.column(col, width=90, anchor='center')  # Narrower columns
    else:
        summary_table.column(col, width=110, anchor='center')  # Wider columns


# Configure row tags for coloring and bold text
summary_table.tag_configure('target_row', background='#D3D3D3')   # Grey
summary_table.tag_configure('actuals_row', background='#ADD8E6')  # Light Blue
summary_table.tag_configure('left_row', background='#90EE90')     # Light Green

summary_row_ids = {}  # Global variable to store row IDs

# Populate the table with initial rows (Target, Actuals, Left)
for row_name in ["Target", "Actuals", "Left"]:
    row_id = summary_table.insert('', 'end', values=(row_name, 0, 0, 0, 0, 0, 0, 0))
    summary_row_ids[row_name] = row_id  # Store the row ID

# Applying custom tags for each row
summary_table.item(summary_row_ids['Target'], tags=('target_row', 'bold_text'))
summary_table.item(summary_row_ids['Actuals'], tags=('actuals_row', 'bold_text'))
summary_table.item(summary_row_ids['Left'], tags=('left_row', 'bold_text'))

# Add a new Dashboard Frame to the notebook
DashboardFrame = ttk.Frame(notebook)
notebook.add(DashboardFrame, text="Dashboard", state='disabled')

# Assume this code is added to your existing script where other imports are defined
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from matplotlib.dates import DateFormatter


# Step 2: Implement a function to create and display charts
def create_weight_progress_chart(frame):
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Calculation.csv"
    if not os.path.exists(FileName):
        return

    # Load weight data
    data = pd.read_csv(FileName)
    dates = pd.to_datetime(data['Date'],format='mixed')
    weights = data['Weight']

    # Create a figure and plot the data
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(dates, weights, marker='o', linestyle='-', color='blue')
    ax.set_title('Weight Loss Progress')
    ax.set_ylabel('Weight (lbs)')
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Set date format on x-axis
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    # Embed the chart in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def create_body_fat_progress_chart(frame):
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Calculation.csv"
    if not os.path.exists(FileName):
        return

    # Load data
    data = pd.read_csv(FileName)
    dates = pd.to_datetime(data['Date'],format='mixed')
    body_fat_percent = data['Body Fat Percent']

    # Create a figure and plot the data
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(dates, body_fat_percent, marker='o', linestyle='-', color='green')
    ax.set_title('Body Fat Percentage Progress')
    ax.set_ylabel('Body Fat %')
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Set date format on x-axis
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    # Embed the chart in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def create_bmi_progress_chart(frame):
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Calculation.csv"
    if not os.path.exists(FileName):
        return

    # Load data
    data = pd.read_csv(FileName)
    dates = pd.to_datetime(data['Date'],format='mixed')
    bmi = data['BMI']

    # Create a figure and plot the data
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(dates, bmi, marker='o', linestyle='-', color='purple')
    ax.set_title('BMI Progress')
    ax.set_ylabel('BMI')
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Set date format on x-axis
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    # Embed the chart in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)


def create_calories_progress_chart(frame):
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}-Calculation.csv"
    if not os.path.exists(FileName):
        return

    # Load data
    data = pd.read_csv(FileName)
    dates = pd.to_datetime(data['Date'],format='mixed')
    calories = data['Maintenace cal']

    # Create a figure and plot the data
    fig, ax = plt.subplots(figsize=(6,3))
    ax.plot(dates, calories, marker='o', linestyle='-', color='red')
    ax.set_title('Calories Per Day Progress')
    ax.set_ylabel('Calories')
    ax.tick_params(axis='both', which='major', labelsize=6)

    # Set date format on x-axis
    ax.xaxis.set_major_formatter(DateFormatter('%m/%d'))

    # Embed the chart in the tkinter frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def load_dashboard_data():
    # Clear existing content in the dashboard frame
    for widget in DashboardFrame.winfo_children():
        widget.destroy()
    
    # Create sub-frames for each chart, arranging them in two columns
    frame1 = ttk.Frame(DashboardFrame)
    frame1.grid(row=0, column=0, padx=5, pady=5)
    frame2 = ttk.Frame(DashboardFrame)
    frame2.grid(row=0, column=1, padx=5, pady=5)
    frame3 = ttk.Frame(DashboardFrame)
    frame3.grid(row=1, column=0, padx=5, pady=5)
    frame4 = ttk.Frame(DashboardFrame)
    frame4.grid(row=1, column=1, padx=5, pady=5)

    # Make the frames expand with the window
    DashboardFrame.grid_rowconfigure(0, weight=1)
    DashboardFrame.grid_rowconfigure(1, weight=1)
    DashboardFrame.grid_columnconfigure(0, weight=1)
    DashboardFrame.grid_columnconfigure(1, weight=1)
    
    # Create charts and display them in the designated sub-frames
    create_weight_progress_chart(frame1)
    create_body_fat_progress_chart(frame2)
    create_bmi_progress_chart(frame3)
    create_calories_progress_chart(frame4)

# Check for existing data before starting the main loop
root.after(1000, initialize)

# UI Callbacks
if __name__ == "__main__":
    root.protocol("WM_DELETE_WINDOW", root.quit)
    root.mainloop()