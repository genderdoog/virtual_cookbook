"""
Component 2: Adding recipes

Created by: Matthew C
Created on: 30/07/2025

Version 1: Output to python shell
"""

import json
import os

new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file

new_recipe_info["name"] = input("Enter name of recipe: ") # Ask for recipe name
new_recipe_info["author/source"] = input("Enter author/source of recipe: ") # Ask for author/source
new_recipe_info["prep_time"] = input("Enter prep time: ") # Ask for prep time
new_recipe_info["total_time"] = input("Enter total cooking time: ") # Ask for total time 
new_recipe_info["serves"] = input("How many people does this recipe serve? ") # Ask how many people this recipe serves

def get_ingredient_amount(ingredient_name, quantity_type):
    '''Returns a postive number from a user input, used to get amount of ingredient added to a recipe'''
    valid_amount = False # Set up while loop
    
    while valid_amount != True: # Repeat until a valid quantity amount entered by the user is valid
        quantity_amount = input(f"Enter the amount of '{ingredient_name}' in {quantity_type}(s): ")
        try:
            quantity_amount = int(quantity_amount) # Error checking, if a string is detected it will give a different error message
            if quantity_amount > 0: # Valid number, so we can end the while loop
                quantity_amount = str(quantity_amount) # Convert it back to string so it can be concatnated when returned
                valid_amount = True # End while loop
            else:
                print("Enter positive integer")
        
        except ValueError: # If a letter is found in the user input
            if "/" in quantity_amount: # If user wants to add say 3/4 of a tsp, we can create a special case for this as it is a valid input
                quantity_amount = str(quantity_amount) # Convert it back to string so it can be concatnated when returned
                valid_amount = True # User input is correct, so we end the loop and return the final value
            else:
                print("Enter only whole numbers")
            
    return quantity_amount

# Adding ingredients
list_of_ingredients = []

user_finished_adding_ingredients = False # Set up while loop

while user_finished_adding_ingredients != True: # Repeat until user is finished adding ingredients of recipe
    
    building_ingredient = "" # We will append information, then we will store it in the list_of_ingredients 
    
    quantity_type = input("Enter quantity type (type 'x' to stop): ")
    
    if quantity_type == "x":
        user_finished_adding_ingredients = True # End while loop
    
    # If user wants to add a weight quantity
    elif quantity_type == "g" or quantity_type == "gram":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = get_ingredient_amount(quantity_name, "gram") # Calls get_ingredient_amount function
        building_ingredient = quantity_amount + "g " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
    
    # If user wants to add a tablespoon quantity
    elif quantity_type == "tbsp" or quantity_type == "tablespoon":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = get_ingredient_amount(quantity_name, "tablespoon") # Calls get_ingredient_amount function
        building_ingredient = quantity_amount + "tbsp " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    # If user wants to add a teaspoon quantity
    elif quantity_type == "tsp" or quantity_type == "teaspoon":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = get_ingredient_amount(quantity_name, "teaspoon") # Calls get_ingredient_amount function
        building_ingredient = quantity_amount + "tsp " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    # If user wants to add a cup quantity
    elif quantity_type == "cup":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = get_ingredient_amount(quantity_name, "cup") # Calls get_ingredient_amount function
        building_ingredient = quantity_amount + "cups " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    # If user wants to add a milliliter quantity
    elif quantity_type == "ml" or quantity_type == "milliliter":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = get_ingredient_amount(quantity_name, "milliliter") # Calls get_ingredient_amount function
        building_ingredient = quantity_amount + "mL " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)        
        
    # To add generic text e.g. "one egg yolk"
    elif quantity_type == "generic text":
        quantity_name = input("Enter text: ")
        list_of_ingredients.append(quantity_name)  
    
    else:
        print("try again")
    
new_recipe_info["ingredients"] = list_of_ingredients # Append the temporary list to the main dictionary

# Create a temporary dictionary, this will be assigned to a key of the main dictionary
dict_of_instructions = {}

# We set up the while loop
current_step = 1
user_finished_adding_instructions = False 

while user_finished_adding_instructions != True: # Repeat until user has entered all instructions
    current_instruction = input(f"Enter instructions for step {current_step} (type 'x' to stop): ")
    
    if current_instruction == "x":
        user_finished_adding_instructions= True # End while loop as user has indicated they are finished
    
    else: # If user wants to add an instruction
        dict_of_instructions[f"step{current_step}"] = current_instruction # Append this step to the dict_of_instructions dictionary
        current_step += 1 # Increment the step counter by one for the next instruction if the user decides to add another one 
    
new_recipe_info["instructions"] = dict_of_instructions # Append dictionary filled with instruction to the main dictionary

new_recipe_info["timer_set_to"] = int(input("Enter how many minutes you want the timer to go for: ")) # Ask user to set timer

# File management/creation
# We first need to find out the name of the folder which will house this recipe
directory_recipe_name = new_recipe_info["name"].lower().replace(" ", "_") # This name will be used to create the folder of the recipe

os.mkdir("../data/" + directory_recipe_name) # Create a directory which will house the recipe and image

# Create json file in the newly created folder
with open("../data/" + directory_recipe_name + "/info.json", "w") as f:
    json.dump(new_recipe_info, f, indent = 4)
    
# Update recipe_index.json
# Read the current recipes in the index
with open("../data/recipe_index.json", "r") as f:
    current_json_index = json.load(f)

current_json_index[new_recipe_info["name"]] = directory_recipe_name # Add the appropriate key and value to the temporary dictionary

# Write this newly updated dictionary back into recipe_index.json 
with open("../data/recipe_index.json", "w") as f:
    json.dump(current_json_index, f, indent = 4)
    
