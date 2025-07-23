"""
Component 1: Viewing recipes

Created by: Matthew C
Created on: 22/07/2025

Version 1,2: Baseline functional product
"""
import json
from tkinter import *

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        
        # Initialise window settings
        self.root = Tk()
        self.root.title("component 1")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Initialise outputs to user
        self.recipe_name = StringVar()
        self.name_of_author_source = StringVar()
        
        # How we store what windows are in our program
        self.windows = {}
        
        # Creating windows in our GUI
        self.windows["RecipeFrame"] = self.create_RecipeFrame()
        
        # Show recipe frame first
        self.show_frame("RecipeFrame")
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
        
    def create_RecipeFrame(self):
        '''Creates recipe frame'''
        # Creates frame for each widget in recipe frame
        self.recipe_frame = Frame(self.main_container)
        self.recipe_frame.grid(row=0, column=0, sticky="NESW")
        
        # Open current recipe information from info.json file
        with open("../data/chocolate_chip_cookie/info.json") as f:
            current_recipe = json.load(f)
    
        # Show recipe name
        # Get information from json file
        self.recipe_name.set(current_recipe["name"])
        
        # Create then pack widget
        self.recipe_name_heading = Label(self.recipe_frame, 
                                          textvariable=self.recipe_name)
        self.recipe_name_heading.grid(row = 0, column = 0, sticky="NESW")
        
        # Show image
        self.recipe_image = PhotoImage(file="../data/chocolate_chip_cookie/image.png") # Create image widget
        self.recipe_image = self.recipe_image.subsample(10) # Resizes image
        # Create then show widget with the image inside
        Label(self.recipe_frame, image = self.recipe_image).grid(row = 1, column = 0)
        
        self.recipe_info_textbox = Text(self.recipe_frame)
        
        
        self.recipe_info_textbox.grid(row = 2, column = 0)
       
        
        return self.recipe_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()