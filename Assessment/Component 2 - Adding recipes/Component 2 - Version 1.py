"""
Component 2: Adding recipes

Created by: Matthew C
Created on: 30/07/2025

Version 1: Output to python shell
"""

import json

new_recipe_info = {} # Create blank dictionary which we will then dump to a json file

new_recipe_info["name"] = "Chocolate chip cookie"
new_recipe_info["author/source"] = "https://cloudykitchen.com/blog/chocolate-cookies/"
new_recipe_info["prep_time"] = "25 minutes"
new_recipe_info["total_time"] = "40 minutes"
new_recipe_info["serves"] = "Four"

def get_ingredient_amount(ingredient_name, quantity_type):
    '''Returns a postive number from a user input, used to get amount of ingredient added to a recipe'''
    valid_amount = False # Set up while loop
    
    while valid_amount != True:
        quantity_amount = input(f"Enter the amount of '{ingredient_name}' in {quantity_type}(s): ")
        try:
            quantity_amount = int(quantity_amount)
            if quantity_amount > 0: # Valid number, so we can end the while loop
                quantity_amount = str(quantity_amount) # Convert it back to string so it can be concatnated when returned
                valid_amount = True
            else:
                print("Enter positive integer")
        
        except ValueError:
            if "/" in quantity_amount: # If user wants to add say 3/4 of a tsp, we can create a special case for this to be a valid input
                quantity_amount = str(quantity_amount) # Convert it back to string so it can be concatnated when returned
                valid_amount = True # User input is correct, so we end the loop and return the final value
            else:
                print("Enter only whole numbers")
            
    return quantity_amount

# Adding ingredients
list_of_ingredients = []

user_finished_adding_ingredients = False

while user_finished_adding_ingredients != True:
    
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
    
new_recipe_info["Ingredients"] = list_of_ingredients

# Instructions
list_of_instructions = []
    

print(new_recipe_info)