import tkinter as tk
from tkinter import messagebox
import datetime
import os
import math
import pandas as pd
import matplotlib.pyplot as plt

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

def SaveResults():
    # Check if Data is empty
    if not Data:
        messagebox.showerror("Error", "Data is empty.")
        return
    
    # Preparing data to be saved
    FileName = f"Results/{Data['Name'][0]}.csv"
    
    # Check if 'Results' directory exists, if not, create it
    if not os.path.exists('Results'):
        os.makedirs('Results')

    # Check if file exists, if not, create it and write headers
    if not os.path.isfile(FileName):
        with open(FileName, 'w') as file:
            file.write("Date,Weight,Height,Body Fat Percent,Fat % to Loose,Fat lbs,Lean lbs,Fat lbs per week,Lbs to loose,Target lbs,Days Of Training Per Week,Weeks,BMI,BMR,Multiplier,Maintenace cal,Target deficit,Calories/Day,Protein,Carbs,Fats\n")
    
    # Write results to the file
    with open(FileName, 'a') as file:
        file.write((f"{Data['Date'][0]},"
                    f"{Data['Weight'][0]},"
                    f"{Data['Height'][0]},"
                    f"{Data['Body Fat Percent'][0]},"
                    f"{Data['Fat % to Loose'][0]},"
                    f"{Data['Fat lbs'][0]},"
                    f"{Data['Lean lbs'][0]},"
                    f"{Data['Fat lbs per week'][0]},"
                    f"{Data['Lbs to loose'][0]},"
                    f"{Data['Target lbs'][0]},"
                    f"{Data['Days Of Training Per Week'][0]},"
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
    
    # Create table image
    CreateTableImage(FileName)

    # Show message box
    messagebox.showinfo("Saved", "Results and table image saved successfully!")

def CreateTableImage(filename):
    import pandas as pd
    import matplotlib.pyplot as plt

    # Load the CSV data into a pandas DataFrame
    df = pd.read_csv(filename)

    # Determine the size of the figure dynamically
    figure_width = max(24, len(df.columns) * 2)  # Adjust as needed
    figure_height = max(8, len(df) * 0.5)  # Adjust as needed

    # Create a figure and a set of subplots
    fig, ax = plt.subplots(figsize=(figure_width, figure_height))
    ax.axis('off')

    # Create the table
    table = plt.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center')

    # Set properties for the table
    table.auto_set_font_size(False)
    table.set_fontsize(26)  # Choose a font size that fits your needs
    table.scale(1, 3)  # Increase row height, adjust scale to fit

    table.auto_set_column_width(col=list(range(len(df.columns))))  # Adjust column width automatically
    
    # Highlight the last four columns of the last row in yellow
    last_row_idx = len(df)
    for col_idx in range(len(df.columns) - 4, len(df.columns)):
        cell = table[(last_row_idx, col_idx)]
        cell.set_facecolor('yellow')
        cell.set_edgecolor('black')

    # Adjust layout
    plt.tight_layout()

    # Save the figure with minimal padding
    plt.savefig(f"Results/{filename.split('/')[1].split('.')[0]}Table.png", bbox_inches='tight', pad_inches=0.1)

    # Close the figure
    plt.close(fig)

def UpdateResultsText():
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
        
def AddPercent(*args, var):
        text = var.get()
        if len(text) > 0 and text[-1] != '%':
            var.set(text + '%')
        
# Variables
Data = {}

# SETUP UI
root = tk.Tk()
root.title("FitnessTracker - By Carlos Finocchiaro")

# Variables
NameEntry = tk.StringVar()
GenderVar = tk.StringVar()
AgeEntry = tk.StringVar()
WeightEntry = tk.StringVar()
HeightEntry = tk.StringVar()
DaysOfTrainingEntry = tk.StringVar()
BodyFatPercentEntry = tk.StringVar()
BodyFatPercentGoalEntry = tk.StringVar(value="12%")
BodyFatPercentLossPerWeekEntry = tk.StringVar(value="1%")
ProteinPercentEntry = tk.StringVar(value="45%")
CarbsPercentEntry = tk.StringVar(value="35%")
FatsPercentEntry = tk.StringVar(value="20%")
ResultsText = tk.StringVar()

# Frames
InputFrame = tk.Frame(root, padx=10, pady=10)
InputFrame.grid(row=0, column=0, sticky="ew")

ButtonsFrame = tk.Frame(InputFrame, padx=10, pady=10)
ButtonsFrame.grid(row=12, column=1, pady=20)

ResultsFrame = tk.Frame(root, padx=20, pady=20)
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
ResultsText.grid(row=0, column=0,sticky='we')

# UI Callbacks
if __name__ == "__main__":
    root.mainloop()