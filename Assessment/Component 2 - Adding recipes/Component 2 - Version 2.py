"""
Component 2: Adding recipes

Created by: Matthew C
Created on: 30/07/2025

Version 1: Output to python shell
Version 2: minimum viable product GUI
"""

import json
import shutil # For copying the uploaded image into the recipe folder
import os
from tkinter import *
from tkinter import ttk # For checkbox
from tkinter import filedialog # For image uploading

class Program:
    
    def __init__(self):
        '''Setup the GUI'''
        # Initialise window settings
        self.root = Tk()
        self.root.title("Component 2 - Version 2")
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Storing information
        self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
        self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to new_ingredient_info
        self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info
        
        # When the user is adding ingredient amount, this info will be shown
        self.display_ingredient_name = StringVar() 
        self.display_ingredient_type = StringVar()
        
        # When the user is asked if they want to add ingredients to the recipe, we show them this textvariable
        self.display_ingredients = StringVar()
        
        # When user is adding instructions, these are the related variables
        self.new_instruction_info = {} # This will be added to new_recipe_info as the value of the key "instructions"
        self.current_step = IntVar() # While user is adding instructions, the step counter needs to increase automatically
        self.current_step.set(1) # On startup, we set it to 1
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Creating windows for our GUI
        # Homepage
        self.windows["HomeAddRecipesFrame"] = self.create_HomeAddRecipesFrame()
        
        # Getting basic information
        self.windows["AskRecipeNameFrame"] = self.create_AskRecipeNameFrame()
        self.windows["AskRecipeAuthorSourceFrame"] = self.create_AskRecipeAuthorSourceFrame()
        self.windows["AskRecipePrepTimeFrame"] = self.create_AskRecipePrepTimeFrame()
        self.windows["AskRecipeTotalTimeFrame"] = self.create_AskRecipeTotalTimeFrame()
        self.windows["AskRecipeHowManyServesFrame"] = self.create_AskRecipeHowManyServesFrame()
        self.windows["AskRecipeTimerFrame"] = self.create_AskRecipeTimerFrame()
        
        # Adding ingredients
        self.windows["ShowCurrentIngredientsFrame"] = self.create_ShowCurrentIngredientsFrame()
        self.windows["AddIngredientQuantityTypeFrame"] = self.create_AddIngredientQuantityTypeFrame()
        self.windows["AddIngredientNameFrame"] = self.create_AddIngredientNameFrame()
        self.windows["AddIngredientAmountFrame"] = self.create_AddIngredientAmountFrame()
        self.windows["AddIngredientGenericTextFrame"] = self.create_AddIngredientGenericTextFrame()
        
        # Adding instructions
        self.windows["ShowCurrentInstructionsFrame"] = self.create_ShowCurrentInstructionsFrame()
        self.windows["AddNewInstructionFrame"] = self.create_AddNewInstructionFrame()
        
        # Image uploading when adding recipe
        self.windows["UploadImageFrame"] = self.create_UploadImageFrame()
        
        # Final save button for recipe
        self.windows["SaveRecipeToJsonFrame"] = self.create_SaveRecipeToJsonFrame()
        
        # Show home frame first when program starts
        self.show_frame("HomeAddRecipesFrame")   
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
       
        
    def run(self):
        '''Run program'''
        self.root.mainloop()
      
      
    def save_information(self, data_type, info):
        '''When the users presses this button, it saves it to the main dictionary'''
        if data_type == "name": # This clears the values, when user adds recipes back to back.
            self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
            self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to new_ingredient_info
            self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info            
            self.new_instruction_info = {} # This will be added to new_recipe_info as the value of the key "instructions"
            self.current_step.set(1) # On reset, we set it to 1
            
        # For all other frames other than asking for the recipe name
        self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
        print(self.new_recipe_info) 
        
    def save_temp_ingredient_info(self, data_type, info):
        '''This determines what the save button does while the user is adding ingredients'''
        # If user presses the save button when choosing quantity type
        if data_type == "quantity_type":
            self.temp_ingredient_info = [] # We will first blank out the list that stores the temp_ingredient info, in case user previously added a ingredient
            
            # Once again we open the quantity types json file so that we can append the apropriate end to the final string
            with open("../data/quantity_types.json") as f:
                quantity_types_combobox = json.load(f)
            
            try: # If the user wants to change their quantity type, after having pressed save
                self.temp_ingredient_info.pop(-1) # Remove the current quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) # Add the quantity type to the temporary ingredients dictionary
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
                print(self.temp_ingredient_info)
           
            except IndexError: # If this is the first time the user is selecting a quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) 
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
                print(self.temp_ingredient_info)
            
        # If user presses save button when entering the ingredient name
        elif data_type == "quantity_name":
            
            # If this is the first time the user is adding the name to the ingredient
            if len(self.temp_ingredient_info) == 1:
                self.temp_ingredient_info.append(info) # Add the name to the temp ingredient list
                self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                print(self.temp_ingredient_info)
            
            # If user has changed their ingredient name after pressing save
            else:
                self.temp_ingredient_info.pop(-1) # Remove the old ingredient name
                self.temp_ingredient_info.append(info) # Add the new ingredient name to the temp list
                self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                print(self.temp_ingredient_info)
                
            
        # If user presses save button when entering ingredient amount
        # This is special as we need to save it to the ingredient_info as well when the user presses save in this text
        elif data_type == "quantity_amount":
            try:
                info = int(info) # Turn the ingredient amount into a integer value
                
                if info <= 0: # If amount entered is less than 0, this is an invalid amount 
                    print("less than 0")
                
                else: # Amount entered is valid, so we now add it to temp_ingredient_info
                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        print(self.new_ingredient_info)
                        self.display_ingredients.set(str(self.new_ingredient_info))
                    else: # If user has already saved their ingredient amount
                        self.temp_ingredient_info.pop(-1) # Removes old quantity value
                        self.temp_ingredient_info.append(info) # Add the new quantity amount to the list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.pop(-1) # Removes the old ingredient which user has decided to replace
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        print(self.new_ingredient_info)

                        self.display_ingredients.set(str(self.new_ingredient_info))
                    
            except ValueError: # If a letter is found in the ingredient amount
                if "/" in info: # Special case for entering fractions like 3/4 if user has say wanted to use a tsp quantity type
                    info = str(info) # Turn it into a string
                    
                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        self.temp_ingredient_info.append(info) # Add the quantity amount to the list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        print(self.new_ingredient_info)
                        self.display_ingredients.set(str(self.new_ingredient_info))
                        
                    else: # If user has already saved their ingredient amount
                        self.temp_ingredient_info.pop(-1) # Removes old quantity value
                        self.temp_ingredient_info.append(info) # Add the new quantity amount to the list
                        print(self.temp_ingredient_info)
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        print(final_ingredient)
                        self.new_ingredient_info.pop(-1) # Removes the old ingredient which user has decided to replace
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary (which will be dumped to json)
                        print(self.new_ingredient_info)
                        self.display_ingredients.set(str(self.new_ingredient_info))
                
                else:
                    print("enter whole values only")
        
        # If user presses save button while on the adding generic text screen            
        elif data_type == "generic_text":
            if len(self.temp_ingredient_info) == 1: # If user has not pressed the save button before
                self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                print(self.temp_ingredient_info)
                final_ingredient = self.temp_ingredient_info[1] # The second item in the temp ingredient dictionary has the string we want to add
                print(final_ingredient)
                self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                print(self.new_ingredient_info)
                
            else:
                self.temp_ingredient_info.pop(-1) # Removes old generic text
                self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                print(self.temp_ingredient_info)
                final_ingredient = self.temp_ingredient_info[1] # The second item in the temp ingredient dictionary has the string we want to add
                print(final_ingredient)
                self.new_ingredient_info.pop(-1) # Removes the old generic text which user has decided to replace
                self.new_ingredient_info.append(final_ingredient) # Add generic text to the new ingredient dictionary
                print(self.new_ingredient_info)   
                    
    def create_generic_text_or_other_frame(self):
        '''If a user wants to add a ingredient that does not require a 
        quantity type e.g. tsp or g, they need to be sent to another frame. 
        This code will decide if they should be'''
        
        if self.temp_ingredient_info[0] == "generictext": # If user has picked generic text as their ingredient type, we send them to this frame
            self.create_AddIngredientGenericTextFrame()
        
        else: # For any other quantity type, we need send them to the add ingredient name frame
            self.create_AddIngredientNameFrame()
        
    def save_instruction_info(self, instruction):
        '''When the user presses the save button after entering into the instructions, this is what will be run''' 
        self.new_instruction_info[f"step{self.current_step.get()}"] = instruction # Add the instruction, which will save the step to new_instruction info
        self.current_step.set(self.current_step.get() + 1) # Increment the step by one, so that if user adds another instruction it will adjust accordingly

            
    def upload_file(self):
        '''When the user presses this button, it will open a popup windows
        where the user can then select the image they would like to place
        in their recipe'''
        file_path = filedialog.askopenfilename() # Open windows prompt
        if file_path:
            self.new_recipe_info["path_to_image"] = file_path # Stores it in new_recipe_info
            print(self.new_recipe_info)             
        
    def dump_new_recipe_to_json(self):
        '''When the user is finished adding detail of recipe, they press the
        save button and this is what will run'''
        print("-----")
        print(self.new_recipe_info)
        
        # Json and image file management
        # We first need to find out the name of the folder which will house this recipe
        directory_recipe_name = self.new_recipe_info["name"].lower().replace(" ", "_") # This name will be used to create the folder of the recipe
        
        # Create a directory which will house the recipe and image
        os.mkdir("../data/" + directory_recipe_name) 
        
        # Copy the image uploaded by user into the the newly created recipe folder
        shutil.copy(self.new_recipe_info["path_to_image"], "../data/" + directory_recipe_name + "/image.png")
        
        # Remove the path_to_image key in new_recipe_info, as that is not required when dumping recipe info to json
        self.new_recipe_info.pop("path_to_image")
        
        # Create json file in the newly created recipe folder
        with open("../data/" + directory_recipe_name + "/info.json", "w") as f:
            json.dump(self.new_recipe_info, f, indent = 4)        
        
        # Updating recipe_index.json
        # Read the current recipes in the index
        with open("../data/recipe_index.json", "r") as f:
            current_json_index = json.load(f)
        
        current_json_index[self.new_recipe_info["name"]] = directory_recipe_name # Add the appropriate key and value to the index from the temporary dictionary
        
        # Write this newly updated dictionary back into recipe_index.json 
        with open("../data/recipe_index.json", "w") as f:
            json.dump(current_json_index, f, indent = 4)        
       
        
    def create_HomeAddRecipesFrame(self):
        '''Creates homepage of adding recipes'''
        # Sets up home frame window
        self.home_add_recipes_frame = Frame(self.main_container)
        self.home_add_recipes_frame.grid(row = 0, column = 0, sticky = "NESW") 
        
        # Create button to start creating a new recipe
        self.add_new_recipebutt = Button(self.home_add_recipes_frame, 
                                     text = "Add new recipe", 
                                     command=lambda: self.show_frame("AskRecipeNameFrame"))
        self.add_new_recipebutt.grid(row = 0, column = 0, sticky = "NESW")
        
        return self.home_add_recipes_frame
    
    
    def create_AskRecipeNameFrame(self):
        '''Asks for recipe name window'''
        # Sets up window
        self.ask_recipe_name_frame = Frame(self.main_container)
        self.ask_recipe_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Creating and packing heading widget
        self.ask_recipe_name_frame_heading = Label(self.ask_recipe_name_frame,
                                                   text = "Enter name of recipe:")
        self.ask_recipe_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                                columnspan = 2,)
        
        # Creating and packing text box
        self.ask_recipe_name_frame_textbox = Entry(self.ask_recipe_name_frame)
        self.ask_recipe_name_frame_textbox.grid(row = 1, column = 0,
                                                columnspan = 2,
                                                sticky = "NESW")
        
        # Create next button
        self.ask_recipe_name_frame_nextbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("AskRecipeAuthorSourceFrame"))
        self.ask_recipe_name_frame_nextbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW")
        
        # Create save button to store value in self.new_recipe_info
        self.ask_recipe_name_frame_savebutt = Button(self.ask_recipe_name_frame,
                                                     text = "Save",
                                                     command=lambda: self.save_information("name", self.ask_recipe_name_frame_textbox.get())) 
        self.ask_recipe_name_frame_savebutt.grid(row = 2, column = 1, sticky = "NESW")
        
        return self.ask_recipe_name_frame
    
    
    def create_AskRecipeAuthorSourceFrame(self):
        '''Window which asks user for author/source'''
        # Set up window
        self.ask_recipe_author_source_frame = Frame(self.main_container)
        self.ask_recipe_author_source_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_author_source_frame_heading = Label(self.ask_recipe_author_source_frame,
                                                            text = "Enter author/source of recipe:")
        self.ask_recipe_author_source_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 2)
        
        # Create and pack text box
        self.ask_recipe_author_source_frame_textbox = Entry(self.ask_recipe_author_source_frame)
        self.ask_recipe_author_source_frame_textbox.grid(row = 1, column = 0,
                                                         sticky = "NESW", 
                                                         columnspan = 2)
        
        # Create next button and pack next button
        self.ask_recipe_author_source_frame_nextbutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("AskRecipePrepTimeFrame"))
        self.ask_recipe_author_source_frame_nextbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW")
        
        # Create and pack save button
        self.ask_recipe_author_source_frame_savebutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("author/source", self.ask_recipe_author_source_frame_textbox.get()))
        self.ask_recipe_author_source_frame_savebutt.grid(row = 2, column = 1,
                                                          sticky = "NESW")
                                                              
        
        return self.ask_recipe_author_source_frame
    
    
    def create_AskRecipePrepTimeFrame(self):
        '''Creates window to ask for prep time'''
        self.ask_recipe_prep_time_frame = Frame(self.main_container)
        self.ask_recipe_prep_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_prep_time_frame_heading = Label(self.ask_recipe_prep_time_frame,
                                                        text = "Enter prep time:")
        self.ask_recipe_prep_time_frame_heading.grid(row = 0, column = 0,
                                                     sticky = "NESW", 
                                                     columnspan = 2)
        
        # Create and pack text box widget
        self.ask_recipe_prep_time_frame_textbox = Entry(self.ask_recipe_prep_time_frame)
        self.ask_recipe_prep_time_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2)
        
        # Create and pack next button
        self.ask_recipe_prep_time_frame_nextbutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Next",
                                                          command=lambda: self.show_frame("AskRecipeTotalTimeFrame"))
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW")
        
        # Create and pack save button
        self.ask_recipe_prep_time_frame_savebutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Save",
                                                          command=lambda: self.save_information("prep_time", self.ask_recipe_prep_time_frame_textbox.get()))
        self.ask_recipe_prep_time_frame_savebutt.grid(row = 2, column = 1,
                                                      sticky = "NESW")
        
        return self.ask_recipe_prep_time_frame
    
    
    def create_AskRecipeTotalTimeFrame(self):
        '''Creates window which asks user for total time to make recipe'''
        self.ask_recipe_total_time_frame = Frame(self.main_container)
        self.ask_recipe_total_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.ask_recipe_total_time_frame_heading = Label(self.ask_recipe_total_time_frame,
                                                         text = "Enter total cooking time:")
        self.ask_recipe_total_time_frame_heading.grid(row = 0, column = 0,
                                                      sticky = "NESW", 
                                                      columnspan = 2)
        
        # Create and pack entry box so that user can enter how long in total it will take to make that recipe
        self.ask_recipe_total_time_frame_textbox = Entry(self.ask_recipe_total_time_frame)
        self.ask_recipe_total_time_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Create and pack next button, to move onto asking how many servings is this recipe for
        self.ask_recipe_total_time_frame_nextbutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("AskRecipeHowManyServesFrame"))
        self.ask_recipe_total_time_frame_nextbutt.grid(row = 2, column = 0,
                                                       sticky = "NESW")
        
        # Create and pack save button, to save total time required to make this recipe
        self.ask_recipe_total_time_frame_savebutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_information("total_time", self.ask_recipe_total_time_frame_textbox.get()))
        self.ask_recipe_total_time_frame_savebutt.grid(row = 2, column = 1,
                                                       sticky = "NESW")
        
        return self.ask_recipe_total_time_frame
    
    def create_AskRecipeHowManyServesFrame(self):
        '''Creates window which allows user to input how many people this recipe serves'''
        self.ask_recipe_how_many_serves_frame = Frame(self.main_container)
        self.ask_recipe_how_many_serves_frame.grid(row = 0, column = 0,
                                                   sticky = "NESW")
        
        # Creates and packs heading widget
        self.ask_recipe_how_many_serves_frame_heading = Label(self.ask_recipe_how_many_serves_frame,
                                                              text = "How many people does this recipe serve?")
        self.ask_recipe_how_many_serves_frame_heading.grid(row = 0, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs entry box for user to input number of servings
        self.ask_recipe_how_many_serves_frame_textbox = Entry(self.ask_recipe_how_many_serves_frame)
        self.ask_recipe_how_many_serves_frame_textbox.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs next button, which will move onto asking for ingredients
        self.ask_recipe_how_many_serves_frame_nextbutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Next",
                                                                command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.ask_recipe_how_many_serves_frame_nextbutt.grid(row = 2, column = 0,
                                                            sticky = "NESW")
        
        # Creates and packs save button, to save current information into self.new_recipe_info
        self.ask_recipe_how_many_serves_frame_savebutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Save",
                                                                command=lambda: self.save_information("serves", self.ask_recipe_how_many_serves_frame_textbox.get()))
        self.ask_recipe_how_many_serves_frame_savebutt.grid(row = 2, column = 1,
                                                            sticky = "NESW")
        
        return self.ask_recipe_how_many_serves_frame
    
    
    def create_ShowCurrentIngredientsFrame(self):
        '''Shows current ingredients added to new recipe'''
        # Setting up frame
        self.show_current_ingredients_frame = Frame(self.main_container)
        self.show_current_ingredients_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading widget
        self.show_current_ingredients_frame_heading = Label(self.show_current_ingredients_frame,
                                                            text = "Current ingredients:")
        self.show_current_ingredients_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 3)
        
        # Create and pack "current list of ingredients"
        self.show_current_ingredients_frame_list = Label(self.show_current_ingredients_frame,
                                                         textvariable = self.display_ingredients)
        self.show_current_ingredients_frame_list.grid(row = 1, column = 0,
                                                      sticky = "NESW",
                                                      columnspan = 3)
        
        # Create and pack "add ingredients" button
        self.show_current_ingredients_frame_addbutt = Button(self.show_current_ingredients_frame,
                                                             text = "Add",
                                                             command=lambda: self.show_frame("AddIngredientQuantityTypeFrame"))
        self.show_current_ingredients_frame_addbutt.grid(row = 2, column = 0,
                                                         sticky = "NESW")
        
        # Crreat and pack save button, which will add everything self.ingredient_info into self.new_recipe_info
        self.show_current_ingredients_frame_savebutt = Button(self.show_current_ingredients_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("ingredients", self.new_ingredient_info))
        self.show_current_ingredients_frame_savebutt.grid(row = 2, column = 2,
                                                          sticky = "NESW")
        
        # Create and pack "next" button
        self.show_current_ingredients_frame_nextbutt = Button(self.show_current_ingredients_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("ShowCurrentInstructionsFrame"))
        self.show_current_ingredients_frame_nextbutt.grid(row = 2, column = 1,
                                                          sticky = "NESW")
        
        return self.show_current_ingredients_frame
        
        
    def create_AddIngredientQuantityTypeFrame(self):
        '''Asks user for ingredient quantity type'''
        self.add_ingredient_quantity_type_frame = Frame(self.main_container)
        self.add_ingredient_quantity_type_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create heading and pack heading
        self.add_ingredient_quantity_type_frame_heading = Label(self.add_ingredient_quantity_type_frame,
                                                                text = "Enter quantity type:")
        self.add_ingredient_quantity_type_frame_heading.grid(row = 0, column = 0,
                                                             sticky = "NESW",
                                                             columnspan = 2)
        
        # This will open up the dictionary which stores all the valid quantity types, used for the combo box
        with open("../data/quantity_types.json") as f:
            quantity_types_combobox = json.load(f)
            
        # Find all the keys in the dictionary and then put it in one list
        quantity_types_keys = list(quantity_types_combobox.keys())
        
        # Create and pack combo box 
        self.add_ingredient_quantity_type_frame_combobox = ttk.Combobox(self.add_ingredient_quantity_type_frame,
                                                                        state = "readonly", # So that user cannot add their own quantity values
                                                                        values = quantity_types_keys) # Set values to what is in the dictionary keys
        self.add_ingredient_quantity_type_frame_combobox.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              columnspan = 2)
        
        # Create and pack next button, to move onto asking the ingredient name or generic text if the user has selected that option
        self.add_ingredient_quantity_type_frame_nextbutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Next",
                                                                  command=self.create_generic_text_or_other_frame)
        self.add_ingredient_quantity_type_frame_nextbutt.grid(row = 2, column = 0,
                                                              sticky = "NESW")
        
        # Create and pack save button, to save information to self.temp_ingredient_info
        self.add_ingredient_quantity_type_frame_savebutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Save",
                                                                  command=lambda: self.save_temp_ingredient_info("quantity_type", self.add_ingredient_quantity_type_frame_combobox.get())) 
        self.add_ingredient_quantity_type_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW")
        
        return self.add_ingredient_quantity_type_frame

    
    def create_AddIngredientNameFrame(self):
        '''Asks user for ingredient name when adding new ingredients'''
        self.add_ingredient_name_frame = Frame(self.main_container)
        self.add_ingredient_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.add_ingredient_name_frame_heading = Label(self.add_ingredient_name_frame,
                                                       text = "Enter name of ingredient:")
        self.add_ingredient_name_frame_heading.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    columnspan = 2)
        
        # Create and pack text box which stores name of ingredient
        self.add_ingredient_name_frame_textbox = Entry(self.add_ingredient_name_frame)
        self.add_ingredient_name_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2)
        
        # Create and pack save button
        self.add_ingredient_name_frame_savebutt = Button(self.add_ingredient_name_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_temp_ingredient_info("quantity_name", self.add_ingredient_name_frame_textbox.get())) 
        self.add_ingredient_name_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW")
        
        # Create and pack next button
        self.add_ingredient_name_frame_nextbutt = Button(self.add_ingredient_name_frame,
                                                         text = "Next",
                                                         command=lambda: self.show_frame("AddIngredientAmountFrame"))
        self.add_ingredient_name_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW")
        
        return self.add_ingredient_name_frame
    
    
    def create_AddIngredientAmountFrame(self):
        '''Asks user for the amount of that ingredient which they have chosen'''
        self.add_ingredient_amount_frame = Frame(self.main_container)
        self.add_ingredient_amount_frame.grid(row = 0, column = 0, sticky = "NESW")

        # Creates and packs heading
        self.add_ingredient_amount_frame_heading1 = Label(self.add_ingredient_amount_frame,
                                                         text = "Enter amount of this ingredient type ")
        self.add_ingredient_amount_frame_heading1.grid(row = 0, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Creates and displays the name of the ingredient, entered in a previous page
        self.add_ingredient_amount_frame_quantityname = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_name)
        self.add_ingredient_amount_frame_quantityname.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs entrybox
        self.add_ingredient_amount_frame_textbox = Entry(self.add_ingredient_amount_frame)
        self.add_ingredient_amount_frame_textbox.grid(row = 2, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2)
        
        # Creates and packs heading for "in"
        self.add_ingredient_amount_frame_heading2 = Label(self.add_ingredient_amount_frame,
                                                          text = "in")
        self.add_ingredient_amount_frame_heading2.grid(row = 3, column = 0,
                                                       sticky = "NESW",
                                                       columnspan = 2)
        
        # Creates and displays quantity type of ingredient, entered on a previous page
        self.add_ingredient_amount_frame_quantitytype = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_type)
        self.add_ingredient_amount_frame_quantitytype.grid(row = 4, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2)
        
        # Creates and packs next button
        self.add_ingredient_amount_frame_nextbutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_amount_frame_nextbutt.grid(row = 5, column = 0,
                                                       sticky = "NESW")
        
        # Creates and packs save button, which will add the quantity amount to the temp ingredient dictionary
        self.add_ingredient_amount_frame_savebutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_temp_ingredient_info("quantity_amount", self.add_ingredient_amount_frame_textbox.get()))
        self.add_ingredient_amount_frame_savebutt.grid(row = 5, column = 1,
                                                      sticky = "NESW")
        
        return self.add_ingredient_amount_frame
    
    def create_AddIngredientGenericTextFrame(self):
        '''If user chooses quantity type = "generic text", they will be put on this frame'''
        self.add_ingredient_generic_text_frame = Frame(self.main_container)
        self.add_ingredient_generic_text_frame.grid(row = 0, column = 0,
                                                    sticky = "NESW")
        
        # Create and pack heading
        self.add_ingredient_generic_text_frame_heading = Label(self.add_ingredient_generic_text_frame,
                                                               text = "Enter generic text here: ")
        self.add_ingredient_generic_text_frame_heading.grid(row = 0, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2)
        
        # Creates and packs textbox, where user can input whatever they need for the ingredient
        self.add_ingredient_generic_text_frame_textbox = Entry(self.add_ingredient_generic_text_frame)
        self.add_ingredient_generic_text_frame_textbox.grid(row = 1, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2)
        
        # Creates and packs next button
        self.add_ingredient_generic_text_frame_nextbutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Next",
                                                                 command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_generic_text_frame_nextbutt.grid(row = 2, column = 0,
                                                             sticky = "NESW")
        
        # Creates and packs save button
        self.add_ingredient_generic_text_frame_savebutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Save",
                                                                 command=lambda: self.save_temp_ingredient_info("generic_text",  self.add_ingredient_generic_text_frame_textbox.get()))
        self.add_ingredient_generic_text_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW")
        
                                                               
        
        return self.add_ingredient_generic_text_frame
    
    
    def create_ShowCurrentInstructionsFrame(self):
        '''When the user wants to add instructions, this frame will show them all the instructions they have added so far'''
        self.show_current_instructions_frame = Frame(self.main_container)
        self.show_current_instructions_frame.grid(row = 0, column = 0,
                                                  sticky = "NESW")
        
        # Create and pack heading widget
        self.show_current_instructions_frame_heading = Label(self.show_current_instructions_frame,
                                                             text = "Current instructions:")
        self.show_current_instructions_frame_heading.grid(row = 0, column = 0,
                                                          sticky = "NESW",
                                                          columnspan = 3)
        
        # Create and pack add button, so that user can add a instruction
        self.show_current_instructions_frame_addbutt = Button(self.show_current_instructions_frame,
                                                              text = "Add",
                                                              command=lambda: self.show_frame("AddNewInstructionFrame"))
        self.show_current_instructions_frame_addbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW")
        
        # Create and pack next button, which is asking for the timer functionality
        self.show_current_instructions_frame_nextbutt = Button(self.show_current_instructions_frame,
                                                               text = "Next",
                                                               command=lambda: self.show_frame("AskRecipeTimerFrame"))
        self.show_current_instructions_frame_nextbutt.grid(row = 2, column = 1, 
                                                           sticky = "NESW")
        
        # Create and pack save button, to save all instructions to new_recipe_info
        self.show_current_instructions_frame_savebutt = Button(self.show_current_instructions_frame,
                                                               text = "Save",
                                                               command=lambda: self.save_information("instructions", self.new_instruction_info))
        self.show_current_instructions_frame_savebutt.grid(row = 2, column = 2,
                                                           sticky = "NESW")
        
        return self.show_current_instructions_frame
    
    def create_AddNewInstructionFrame(self):
        '''This frame allows the user to input and save a new instruction to their recipe'''
        self.add_new_instruction_frame = Frame(self.main_container)
        self.add_new_instruction_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.add_new_instruction_frame_heading = Label(self.add_new_instruction_frame,
                                                       text = "Enter instruction:")
        self.add_new_instruction_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2)
        
        # Create and pack text box for inputting instruction
        self.add_new_instruction_frame_textbox = Entry(self.add_new_instruction_frame)
        self.add_new_instruction_frame_textbox.grid(row = 1, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2)
        
        # Create and pack next button, which will return the user back to the show_current_ingredients_frame
        self.add_new_instruction_frame_nextbutt = Button(self.add_new_instruction_frame,
                                                         text = "Next",
                                                         command=lambda: self.show_frame("ShowCurrentInstructionsFrame"))
        self.add_new_instruction_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW")
        
        # Create and pack save button
        self.add_new_instruction_frame_savebutt = Button(self.add_new_instruction_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_instruction_info(self.add_new_instruction_frame_textbox.get()))
        self.add_new_instruction_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW")
        
        return self.add_new_instruction_frame
        
    
    def create_AskRecipeTimerFrame(self):
        '''This will ask the user what they want to set the timer for this recipe'''
        self.ask_recipe_timer_frame = Frame(self.main_container)
        self.ask_recipe_timer_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading when user is inputting integer for timer
        self.ask_recipe_timer_frame_heading = Label(self.ask_recipe_timer_frame,
                                                    text = "Enter the number (mins) you want to set the timer to")
        self.ask_recipe_timer_frame_heading.grid(row = 0, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2)
        
        # Create and pack textbox for user input
        self.ask_recipe_timer_frame_textbox = Entry(self.ask_recipe_timer_frame)
        self.ask_recipe_timer_frame_textbox.grid(row = 1, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2)
        
        # Create and pack next button
        self.ask_recipe_timer_frame_nextbutt = Button(self.ask_recipe_timer_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("UploadImageFrame"))
        self.ask_recipe_timer_frame_nextbutt.grid(row = 2, column = 0,
                                                  sticky = "NESW")
        
        # Create and pack save button
        self.ask_recipe_timer_frame_savebutt = Button(self.ask_recipe_timer_frame,
                                                      text = "Save",
                                                      command=lambda: self.save_information("timer_set_to", int(self.ask_recipe_timer_frame_textbox.get()))) # Set input as integer
        self.ask_recipe_timer_frame_savebutt.grid(row = 2, column = 1,
                                                  sticky = "NESW")
        
        return self.ask_recipe_timer_frame
    
    def create_UploadImageFrame(self):
        '''This is the frame where the user can upload an image to add to their recipe'''
        self.upload_image_frame = Frame(self.main_container)
        self.upload_image_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Create and pack heading
        self.upload_image_frame_heading = Label(self.upload_image_frame, 
                                                text = "Press the upload button to add an image to your recipe.")
        self.upload_image_frame_heading.grid(row = 0, column = 0, 
                                             sticky = "NESW",
                                             columnspan = 2)
        
        # Create and pack next button
        self.upload_image_frame_nextbutt = Button(self.upload_image_frame,
                                                  text = "Next",
                                                  command=lambda: self.show_frame("SaveRecipeToJsonFrame"))
        self.upload_image_frame_nextbutt.grid(row = 1, column = 0,
                                              sticky = "NESW")
        
        # Create and pack upload button
        self.upload_image_frame_upbutt = Button(self.upload_image_frame,
                                                text = "Upload",
                                                command = self.upload_file)
        self.upload_image_frame_upbutt.grid(row = 1, column = 1,
                                            sticky = "NESW")

        
        return self.upload_image_frame
    
    def create_SaveRecipeToJsonFrame(self):
        '''This frame is where the user will dump the info to json'''
        self.save_recipe_to_json_frame = Frame(self.main_container)
        self.save_recipe_to_json_frame.grid(row = 0, column = 0,
                                            sticky = "NESW")
        
        # Create and pack heading
        self.save_recipe_to_json_frame_heading = Label(self.save_recipe_to_json_frame,
                                                      text = "Press the save button to add you recipe.")
        self.save_recipe_to_json_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2)
        
        # Create and pack next button
        self.save_recipe_to_json_frame_nextbutt = Button(self.save_recipe_to_json_frame,
                                                         text = "Return to home",
                                                         command=lambda: self.show_frame("HomeAddRecipesFrame"))
        self.save_recipe_to_json_frame_nextbutt.grid(row = 1, column = 0,
                                                     sticky = "NESW")
        
        # Create and pack savebutton
        self.save_recipe_to_json_frame_savebutt = Button(self.save_recipe_to_json_frame,
                                                         text = "Save recipe",
                                                         command = self.dump_new_recipe_to_json)
        self.save_recipe_to_json_frame_savebutt.grid(row = 1, column = 1,
                                                     sticky = "NESW")
        
        return self.save_recipe_to_json_frame
        
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()