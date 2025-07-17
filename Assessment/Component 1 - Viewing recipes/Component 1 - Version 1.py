"""
Component 1: Viewing recipes

Created by: Matthew C
Created on: 16/07/2025

Version 1: Baseline functional product
"""
"""
# Importing modules
import json

# Open file
with open("../data/chocolate_chip_cookie/info.json") as f:
    current_recipe = json.load(f)
    
#print(current_recipe)

name = current_recipe["name"]
print(name)

author_source = current_recipe["author/source"]
print(author_source)

prep_time = current_recipe["prep_time"]
print(prep_time)

total_time = current_recipe["total_time"]
print(total_time)

serves = current_recipe["serves"]
print(serves)

list_of_ingredients = current_recipe["ingredients"]
for each_item in range(len(list_of_ingredients)):
    print(list_of_ingredients[each_item])
    
list_of_instructions = current_recipe["instructions"]
for each_instruction in list_of_instructions:
    print(list_of_instructions[each_instruction])
    
timer_set_to = current_recipe["timer_set_to"]
print(timer_set_to)"""

import os

os.remove("../data/chocolate_chip_cookie/image.jpg")
os.remove("../data/chocolate_chip_cookie/info.json")

os.rmdir("../data/chocolate_chip_cookie")