"""
Component 1: Viewing recipes

Created by: Matthew C
Created on: 16/07/2025

Version 1: Baseline functional product
"""

# Importing modules
import json

with open("./data/chocolate_chip_cookie/info.json") as f:
    current_recipe = json.load(f)
    
print(current_recipe)

