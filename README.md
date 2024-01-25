
# FitnessTracker README.md

---

## Introduction
FitnessTracker is a comprehensive application developed by Carlos Finocchiaro, designed to help users manage and track their fitness journey effectively. Built using the Tkinter library for Python, this application offers a user-friendly interface for setting fitness goals, calculating body metrics, and maintaining a consistent diet and training regimen.

## Features
1. **User Profile Management:** Input personal data including name, gender, age, weight, height, and training frequency.
2. **Body Metrics Calculation:** Calculate body fat percentage, lean body mass, and target weight based on user-inputted goals.
3. **Fitness Goal Tracking:** Set and monitor goals for body fat percentage and weight loss.
4. **Diet Management:** Calculate daily caloric needs based on activity level, and manage macronutrient (protein, carbs, and fats) intake.
5. **Progress Tracking:** Save and visualize progress over time through generated reports and charts.

## Installation
To run FitnessTracker, ensure you have the following dependencies installed:
- Python 3.x
- Tkinter (should be included in standard Python installation)
- Pandas
- Matplotlib

## Usage
Launch the application by running the main script. Input your personal details and fitness goals. The application will guide you through the following processes:

1. **Calculate Weight Loss:** Input current body fat percentage, goal body fat percentage, weekly loss goal, and weight to receive a detailed plan.
2. **Calculate Activity Multiplier:** Based on the frequency of your training sessions per week, get your activity multiplier for caloric calculations.
3. **Calculate Maintenance Calories:** Input age, weight, height, days of training per week, and gender to find out the number of calories needed to maintain your current weight.
4. **Calculate Caloric Deficit:** Input maintenance calories and desired weight loss rate to receive a tailored dietary plan with specific macronutrient distribution.

## Functions Description

### `CalculateWeightLoss`
Calculates various metrics related to weight loss including body fat in pounds, lean body mass, the percentage of body fat to lose, total weight to lose, target weight, body fat pounds loss per week, and the number of weeks to reach the goal.

### `CalculateActivityMultiplier`
Determines the activity multiplier based on the number of days of training per week. This multiplier is used in the calculation of maintenance calories.

### `CalculateMaintenanceCalories`
Calculates the Basal Metabolic Rate (BMR) and maintenance calories based on the user's age, weight, height, days of training per week, and gender.

### `CalculateCaloricDeficit`
Determines the target caloric deficit needed to meet the user's weight loss goals and calculates the daily intake of macronutrients (proteins, carbs, and fats) based on the deficit.

### `GetEntries`
Collects and validates input from the user. If the input is invalid, it shows an error message.

### `UpdateCalculations`
Gathers entries from the user, performs all calculations, and updates the application interface with the results.

### `SaveResults`
Saves the user's data and calculation results in a CSV file and generates a table image for visualization.

### `CreateTableImage`
Generates a visual representation (image) of the user's progress and calculation results.

### `UpdateResultsText`
Updates the text box in the application interface with the latest calculation results and user data.

### `AddPercent`
Helper function to add a percentage sign to the end of the input string, used for fields where percentage values are expected.

## Author
Carlos Finocchiaro

## License
This project is open-sourced under the [MIT license](https://opensource.org/licenses/MIT).

Feel free to fork this project, contribute, or suggest improvements. For any queries or suggestions, please contact Carlos.

---