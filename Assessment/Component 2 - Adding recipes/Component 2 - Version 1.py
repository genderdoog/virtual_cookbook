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

# Adding ingredients
list_of_ingredients = []

user_finished_adding_ingredients = False

while user_finished_adding_ingredients != True:
    
    building_ingredient = "" # We will append information, then we will store it in the list_of_ingredients 
    
    quantity_type = input("Enter quantity type (type 'x' to stop): ")
    
    if quantity_type == "x":
        user_finished_adding_ingredients = True # End while loop
    
    # If user wants to add a grams quantity
    elif quantity_type == "g" or quantity_type == "gram":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = input(f"Enter amount the amount of '{quantity_name}' in grams : ")  
        building_ingredient = quantity_amount + "g " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    elif quantity_type == "tbsp" or quantity_type == "tablespoon":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = input(f"Enter amount the amount of '{quantity_name}' in tablespoon(s) : ")
        building_ingredient = quantity_amount + "tbsp " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    elif quantity_type == "tsp" or quantity_type == "teaspoon":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = input(f"Enter amount the amount of '{quantity_name}' in tablespoon(s) : ")
        building_ingredient = quantity_amount + "tsp " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    elif quantity_type == "cup":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = input(f"Enter how many cups of '{quantity_name}' are required in you recipe: ")
        building_ingredient = quantity_amount + "cups " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)
        
    elif quantity_type == "ml" or quantity_type == "milliliter":
        quantity_name = input("Enter the name of ingredient: ")
        quantity_amount = input(f"Enter how many mL of '{quantity_name}' are required in you recipe: ")
        building_ingredient = quantity_amount + "mL " + quantity_name # Concatnate all information together
        list_of_ingredients.append(building_ingredient)        
        
    elif quantity_type == "generic text":
        quantity_name = input("Enter text: ")
        list_of_ingredients.append(quantity_name)  
    
    else:
        print("try again")
    
new_recipe_info["Ingredients"] = list_of_ingredients

# Instructions
list_of_instructions = []
    

print(new_recipe_info)