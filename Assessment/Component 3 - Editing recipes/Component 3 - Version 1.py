"""
Component 3: Editing recipes 

Created by: Matthew C
Created on: 14/08/25

Version 1: minimum viable product GUI
"""

import json
import shutil # File management
from tkinter import *
from tkinter import ttk # For checkbox

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 3 - Version 1")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        # Homepage 
        self.windows["HomeEditRecipesFrame"]