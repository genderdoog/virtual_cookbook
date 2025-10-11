"""
Virtual cookbook software

Created by: Matthew C
Created on: 26/08/25

Version 1: minimum viable product GUI
Version 2: theming, updates ported from individual components
"""

import json
import random # For random recipe button
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
        self.root.title("Virtual Cookbook")
        
        # Make the root window expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)        
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Make the main container expandable
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Themes
        # This will open up the themes json file
        with open("./data/theme_config.json") as f:
            theme_config_json = json.load(f)              
        
        chosen_theme_name = theme_config_json["chosen_theme"] # Find the name of the theme that the user has last selected
        
        chosen_theme_details = theme_config_json[chosen_theme_name] # Find the details of that theme.
        
        # Set the theme related variables to that theme
        self.bg = chosen_theme_details["bg"]
        self.heading_bg = chosen_theme_details["heading_bg"]
        self.heading_txt = chosen_theme_details["heading_txt"]
        self.subheading_bg = chosen_theme_details["subheading_bg"]
        self.subheading_txt = chosen_theme_details["subheading_txt"]
        self.button_bg = chosen_theme_details["button_bg"]
        self.button_txt = chosen_theme_details["button_txt"]
        
        # VARIABLES FOR COMPONENT 1
        # Initialise strings used to output recipe information
        self.recipe_name = StringVar()
        self.name_of_author_source = StringVar()
        self.recipe_info = StringVar()
        self.recipe_ingredients = StringVar()
        self.recipe_instructions = StringVar()
        
        # Set up timer textvariable for timer
        self.recipe_timer = StringVar()
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # VARIABLES FOR COMPONENT 2
        self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
        self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to new_ingredient_info
        self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info
        
        # When the user is adding ingredient amount, this info will be shown
        self.display_ingredient_name = StringVar() 
        self.display_ingredient_type = StringVar()
        
        # When the user is asked if they want to add ingredients to the recipe, we show them this textvariable
        self.display_ingredients = StringVar()
        
        # When the user is asked if they want to add instructions, they will see this text variable which will show them what steps they have added so far
        self.display_instructions = StringVar()
        
        # When user is adding instructions, these are the related variables
        self.new_instruction_info = {} # This will be added to new_recipe_info as the value of the key "instructions"
        self.current_step = IntVar() # While user is adding instructions, the step counter needs to increase automatically
        self.current_step.set(1) # On startup, we set it to 1
        
        # This creates the variable which displays status of if it is a valid input or not
        self.display_user_input_status = StringVar()
        self.display_user_input_status.set("----")
        
        # Creates variable which helps us tell if user is able to proceed
        self.able_to_proceed = IntVar()
        self.able_to_proceed.set(0) # If it is equal to 0, we don't allow the user to proceed        
        
        # VARIABLES FOR COMPONENT 3
        self.edited_recipe_info = {} 
        self.display_recipe_name_edit_homepage = StringVar()        
        
        # COMPONENT 1 WINDOWS
        self.windows["HomeChoosingToViewRecipeFrame"] = self.create_HomeChoosingToViewRecipeFrame()
        self.windows["ShowRecipeFrame"] = self.create_ShowRecipeFrame("do_not_delete") # To make program run, we first to parse in blank data
        
        # COMPONENT 2 WINDOWS
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
        
        # COMPONENT 3 WINDOWS
        # Homepage 
        self.windows["HomeEditRecipesFrame"] = self.create_HomeEditRecipesFrame()
        # Homepage for a specific recipe
        self.windows["HomeEditSpecificRecipeFrame"] = self.create_HomeEditSpecificRecipeFrame()        
        
        # COMPONENT 4 WINDOWS
        self.windows["HomePageFrame"] = self.create_HomePageFrame() # Main menu of program
        self.windows["SettingsFrame"] = self.create_SettingsFrame() # Settings frame
        
        # Show this frame when program first starts
        self.show_frame("HomePageFrame")
    
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        self.display_user_input_status.set("----") # Reset status box
        self.able_to_proceed.set(0) # Don't allow the user to proceed until they press save
        frame = self.windows[name]
        frame.tkraise()
        
    
    def run(self):
        '''Run program'''
        self.root.mainloop() 
     
     
    def quit_program(self):
        '''Closes program when user presses the quit button on the main menu'''
        self.root.destroy()        
    
    
    def set_theme(self, theme_name):
        '''After the user selects an item from the combobox, the user presses the
        save button which runs this code'''
        
        # This will open up the themes json file
        with open("./data/theme_config.json") as f:
            theme_config_json = json.load(f)              
        
        chosen_theme_details = theme_config_json[theme_name] # Find the details of that theme the user has selected
        
        # Set the theme related variables to that theme
        self.bg = chosen_theme_details["bg"]
        self.heading_bg = chosen_theme_details["heading_bg"]
        self.heading_txt = chosen_theme_details["heading_txt"]
        self.subheading_bg = chosen_theme_details["subheading_bg"]
        self.subheading_txt = chosen_theme_details["subheading_txt"]
        self.button_bg = chosen_theme_details["button_bg"]
        self.button_txt = chosen_theme_details["button_txt"]
        
        # To make it persistent across application restarts, we change the first variable of the json file
        theme_config_json["chosen_theme"] = theme_name
        
        # Then write the theme file back
        with open("./data/theme_config.json", "w") as f:
            json.dump(theme_config_json, f, indent = 4)
            
        # We now recreate each window, so that the theme takes effect for each window
        # COMPONENT 1 WINDOWS
        self.windows["HomeChoosingToViewRecipeFrame"] = self.create_HomeChoosingToViewRecipeFrame()
        self.windows["ShowRecipeFrame"] = self.create_ShowRecipeFrame("do_not_delete") # To make program run, we first to parse in blank data
        
        # COMPONENT 2 WINDOWS
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
        
        # COMPONENT 3 WINDOWS
        # Homepage 
        self.windows["HomeEditRecipesFrame"] = self.create_HomeEditRecipesFrame()
        # Homepage for a specific recipe
        self.windows["HomeEditSpecificRecipeFrame"] = self.create_HomeEditSpecificRecipeFrame()        
        
        # COMPONENT 4 WINDOWS
        self.windows["HomePageFrame"] = self.create_HomePageFrame() # Main menu of program
        self.windows["SettingsFrame"] = self.create_SettingsFrame() # Settings frame
        
        # Refresh the main window
        self.root.mainloop()
        
    
    def run_timer(self):
        '''Runs the timer of a recipe'''
        self.recipe_timer.set(f"{self.timer_in_sec // 60}:{self.timer_in_sec % 60}")
        self.timer_in_sec -= 1    
        
        
    def save_information(self, data_type, info):
        '''When the users presses the save button when adding recipes, it saves it to the main dictionary'''
        if data_type == "name": # This clears the values, when user adds recipes back to back.
            self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
            self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to new_ingredient_info
            self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info            
            self.new_instruction_info = {} # This will be added to new_recipe_info as the value of the key "instructions"
            self.display_instructions.set("") # Reset this text variable used when showing what instructions the user has added so far
            self.display_ingredients.set("") # Reset this text variable used when showing what ingredients the user has added so far
            self.current_step.set(1) # On startup, we set it back to 1
            
            if info == "": # If information given is blank from text box
                self.able_to_proceed.set(0) # Ensures that the user cannot continue with invalid information entered
                self.display_user_input_status.set("ERROR: Enter required information")
            
            else:
                info = info.strip().capitalize() # Remove white space and capitalize input
                # We cannot allow the user to create recipes which have the same name, so the below code wil check that
                info_directory_recipe_name = info.lower().replace(" ", "_") # find out the name which will be used in the directory
                
                # This will open up the recipe index, so that we can cross check in case there is already a recipe that is named as the input
                with open("./data/recipe_index.json") as f:
                    dict_recipes_combobox = json.load(f)
                    
                current_recipe_names = list(dict_recipes_combobox.values()) # Turn into a list
                
                if info_directory_recipe_name in current_recipe_names: # If recipe of same name is detected
                    self.able_to_proceed.set(0) # Ensures that the user can continue on with adding information for the recipe
                    self.display_user_input_status.set("ERROR: Recipe of same name has already been added, please choose a different name.")                    
                
                else: # If this name has not been seen before            
                    self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is i
                    self.able_to_proceed.set(1) # Ensures that the user can continue on with adding information for the recipe
                    self.display_user_input_status.set("Information successfully saved")
        
        else: # For all other frames other than asking for the recipe name such as prep time etc
            if data_type == "timer_set_to": # We need special handing for when user is adding an integer value for inputting timer set to how many minutes
                try:
                    info = int(info)
                    
                    if info > 0: # If input is valid
                        self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
                        self.able_to_proceed.set(1) # Ensures that the user can continue on with adding information for the recipe
                        self.display_user_input_status.set("Information successfully saved") 
                    else:
                        self.able_to_proceed.set(0) # Ensures that user will not able to proceed
                        self.display_user_input_status.set("ERROR: Enter required information")
                        
                except ValueError: # If string is detected
                    self.able_to_proceed.set(0) # Ensures that user will not able to proceed
                    self.display_user_input_status.set("ERROR: Enter whole numbers only in input.")                    
                        
            else: # For other inputs, such as asking for recipe name
                try: 
                    info = info.strip().capitalize() # Remove white space and capitalize input
                    if info.strip() == "": # If information given is blank from text box, or a blank list of instructions
                        self.able_to_proceed.set(0) # Ensures that the user cannot continue with invalid information entered
                        self.display_user_input_status.set("ERROR: Enter required information")
                    
                    else:
                        self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
                        self.able_to_proceed.set(1) # Ensures that the user can continue on with adding information for the recipe
                        self.display_user_input_status.set("Information successfully saved")
                        
                except AttributeError: # When saving ingredients or instructions, we need to use this code
                    if info == []: # If the user has not added any ingredients we cannot let them proceed
                        self.able_to_proceed.set(0) # Ensures that the user cannot continue with invalid information entered
                        self.display_user_input_status.set("ERROR: No ingredients added, press the 'Add' button to add at least one ingredient.")
                        
                    elif info == {}: # When saving instrucions list, we need to use this code
                        self.able_to_proceed.set(0) # Ensures that the user cannot continue with invalid information entered
                        self.display_user_input_status.set("ERROR: No instructions added, press the 'Add' button to add at least one instruction.")                        
                    
                    else:
                        self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
                        self.able_to_proceed.set(1) # Ensures that the user can continue on with adding information for the recipe
                        self.display_user_input_status.set("Information successfully saved")                
        
        
    def save_temp_ingredient_info(self, data_type, info):
        '''This determines what the save button does while the user is adding ingredients'''
        # If user presses the save button when choosing quantity type
        if data_type == "quantity_type":
            self.temp_ingredient_info = [] # We will first blank out the list that stores the temp_ingredient info, in case user previously added a ingredient
            
            # Once again we open the quantity types json file so that we can append the apropriate end to the final string
            with open("./data/quantity_types.json") as f:
                quantity_types_combobox = json.load(f)
            
            try: # If the user wants to change their quantity type, after having pressed save
                self.temp_ingredient_info.pop(-1) # Remove the current quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) # Add the quantity type to the temporary ingredients dictionary
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
           
            except IndexError: # If this is the first time the user is selecting a quantity type
                self.temp_ingredient_info.append(quantity_types_combobox[info]) 
                self.display_ingredient_type.set(info) # This will be used on the page where they add the ingredient amount
            
        # If user presses save button when entering the ingredient name
        elif data_type == "quantity_name":
            info = info.strip("0123456789") # Remove any stray numbers from input
            if info.strip() == "": # If information given is blank from text box
                self.able_to_proceed.set(0) # Ensures that the user cannot continue with invalid information entered
                self.display_user_input_status.set("ERROR: Enter required information")
            
            else:    
                # If this is the first time the user is adding the name to the ingredient
                if len(self.temp_ingredient_info) == 1:
                    self.temp_ingredient_info.append(info) # Add the name to the temp ingredient list
                    self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                    self.display_user_input_status.set("Information successfully saved")
                    self.able_to_proceed.set(1)
                
                # If user has changed their ingredient name after pressing save
                else:
                    self.temp_ingredient_info.pop(-1) # Remove the old ingredient name
                    self.temp_ingredient_info.append(info) # Add the new ingredient name to the temp list
                    self.display_ingredient_name.set(info) # This will be used on the next page when asking for quantity name
                    self.display_user_input_status.set("Information successfully saved")
                    self.able_to_proceed.set(1)
                
            
        # If user presses save button when entering ingredient amount
        # This is special as we need to save it to the ingredient_info as well when the user presses save in this text
        elif data_type == "quantity_amount":
            try:
                info = int(info) # Turn the ingredient amount into a integer value
                
                if info <= 0: # If amount entered is less than 0, this is an invalid amount 
                    self.display_user_input_status.set("ERROR: Enter whole number greater than zero.")
                    self.able_to_proceed.set(0) # Ensure that the user cannot proceed with invalid input
                
                else: # Amount entered is valid, so we now add it to temp_ingredient_info
                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        self.display_ingredients.set(str(self.new_ingredient_info))
                        self.display_user_input_status.set("Information successfully saved")
                        self.able_to_proceed.set(1) # Ensure that the user can continue
                    
                    else: # If user has already saved their ingredient amount
                        self.temp_ingredient_info.pop(-1) # Removes old quantity value
                        self.temp_ingredient_info.append(info) # Add the new quantity amount to the list
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        self.new_ingredient_info.pop(-1) # Removes the old ingredient which user has decided to replace
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        self.display_ingredients.set(str(self.new_ingredient_info))
                        self.display_user_input_status.set("Information successfully saved")
                        self.able_to_proceed.set(1) # Ensure that the user can continue                        
                    
            except ValueError: # If a letter is found in the ingredient amount
                if "/" in info: # Special case for entering fractions like 3/4 if user has say wanted to use a tsp quantity type
                    info = str(info) # Turn it into a string
                    info = info.strip("abcdefghijklmnopqrstuvwxyz!@#$%^&*()_+={}[]-:;'<>,.? ") # Remove any stray letters and symbols that might be in the user input

                    if len(self.temp_ingredient_info) == 2: # If this is the first that the user saves their ingredient amount
                        self.temp_ingredient_info.append(info) # Add the quantity amount to the list
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                        self.display_ingredients.set(str(self.new_ingredient_info)) # Add it to the variable that displays the list of added ingredients so far to the user
                        self.display_user_input_status.set("Information successfully saved")
                        self.able_to_proceed.set(1) # Ensure that the user can continu
                        
                    else: # If user has already saved their ingredient amount
                        self.temp_ingredient_info.pop(-1) # Removes old quantity value
                        self.temp_ingredient_info.append(info) # Add the new quantity amount to the list
                        final_ingredient = f"{self.temp_ingredient_info[2]}{self.temp_ingredient_info[0]} {self.temp_ingredient_info[1]}" # Concatnate ingredients info to form final ingredient line, which we will add to the temp_ingredient_info list
                        self.new_ingredient_info.pop(-1) # Removes the old ingredient which user has decided to replace
                        self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary (which will be dumped to json)
                        self.display_ingredients.set(str(self.new_ingredient_info)) # Add it to the variable that displays the list of added ingredients so far to the user
                        self.display_user_input_status.set("Information successfully saved")
                        self.able_to_proceed.set(1) # Ensure that the user can continue
                
                else:
                    self.display_user_input_status.set("ERROR: Enter whole numbers or fractional amounts (e.g. 3/4)")
                    self.able_to_proceed.set(0) # Ensure that the user cannot continue  
        
        # If user presses save button while on the adding generic text screen            
        elif data_type == "generic_text":
            info = info.strip()
            if info == "": # If input is blank
                self.able_to_proceed.set(0)
                self.display_user_input_status.set("ERROR: Enter required information")        
            
            else: # If input is valid (not blank)
                if len(self.temp_ingredient_info) == 1: # If user has not pressed the save button before
                    self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                    final_ingredient = self.temp_ingredient_info[1] # The second item in the temp ingredient dictionary has the string we want to add
                    self.new_ingredient_info.append(final_ingredient) # Add the fully built ingredient line to the temp ingredient dictionary
                    self.display_ingredients.set(str(self.new_ingredient_info)) # Add it to the variable that displays the list of added ingredients so far to the user
                    self.display_user_input_status.set("Information successfully saved") # Inform user that information has been saved
                    self.able_to_proceed.set(1) # Allows user to proceed
                    self.temp_ingredient_info = []
                    
                else:
                    self.temp_ingredient_info.pop(-1) # Removes old generic text
                    self.temp_ingredient_info.append(info) # Add the quantity amount to the temp list
                    final_ingredient = self.temp_ingredient_info[1] # The second item in the temp ingredient dictionary has the string we want to add
                    self.new_ingredient_info.pop(-1) # Removes the old generic text which user has decided to replace
                    self.new_ingredient_info.append(final_ingredient) # Add generic text to the new ingredient dictionary
                    self.display_ingredients.set(str(self.new_ingredient_info)) # Add it to the variable that displays the list of added ingredients so far to the user
                    self.display_user_input_status.set("Information successfully saved") # Inform user that information has been saved
                    self.able_to_proceed.set(1) # Allows user to proceed
                    self.temp_ingredient_info = []
          
                    
    def create_generic_text_or_other_frame(self):
        '''If a user wants to add a ingredient that does not require a 
        quantity type e.g. tsp or g, they need to be sent to another frame. 
        This code will decide if they should be'''
        
        if self.temp_ingredient_info[0] == "generictext": # If user has picked generic text as their ingredient type, we send them to this frame
            self.create_AddIngredientGenericTextFrame()
            
        else: # For any other quantity type, we need send them to the add ingredient name frame
            self.create_AddIngredientNameFrame()    
        
        
    def save_instruction_info(self, instruction):
        '''When the user presses the save button after entering into the 
        instructions, this is what will be run''' 
        
        if instruction.strip() == "": # Validation checking, blank inputs are invalid
            self.display_user_input_status.set("ERROR: Enter required information")
            self.able_to_proceed.set(0) # Ensure that the user cannot continue
            
        else:
            self.new_instruction_info[f"step{self.current_step.get()}"] = instruction # Add the instruction, which will save the step to new_instruction info
            self.display_instructions.set(str(self.new_instruction_info)) # Update the text variable so that user knows what steps they have added so far
            self.display_user_input_status.set("Information successfully saved") # Inform user that information has been saved
            self.able_to_proceed.set(1) # Ensure that the user can continue

            
    def upload_file(self):
        '''When the user presses this button, it will open a popup windows
        where the user can then select the image they would like to place
        in their recipe'''
        file_path = filedialog.askopenfilename() # Open windows prompt
        
        file_extension = f"{file_path[-4]}{file_path[-3]}{file_path[-2]}{file_path[-1]}"
        file_extension = file_extension.lower()
        
        try: # We find out the size of the imaae first, so that if it is too small, we can not accept the file upload
            uploaded_image= PhotoImage(file = file_path)
            uploaded_image_width = uploaded_image.width()
            uploaded_image_height = uploaded_image.height()
            
            if file_extension == ".png": # If a valid image is found
                if uploaded_image_width < 640 or uploaded_image_height < 480: # If user has uploaded too small of an image
                    self.display_user_input_status.set("ERROR: Image must be larger than 640x480.") # Inform user of incorrect image size uploaded
                    self.able_to_proceed.set(0) # # Does not allow the user to proceed                
                else: # Valid image uploaded
                    self.new_recipe_info["path_to_image"] = file_path # Stores it in new_recipe_info
                    self.display_user_input_status.set("Information successfully saved") # Informs user that process is correct
                    self.able_to_proceed.set(1) # Allows the user to proceed with saving recipe
            
            else: # Rare edge case, if no file extension is there
                self.display_user_input_status.set("ERROR: Unknown file type detected, upload a png image file.") # Informs user to only input png files
                self.able_to_proceed.set(0) # Does not allow the user to proceed 
                
        except: # For any other generic errors
            self.display_user_input_status.set("ERROR: Unknown file type detected, upload a png image file.") # Informs user to only input png files
            self.able_to_proceed.set(0) # Does not allow the user to proceed            
        
        
    def dump_new_recipe_to_json(self):
        '''When the user is finished adding detail of recipe, they press the
        save button and this is what will run'''
        # Json and image file management
        # We first need to find out the name of the folder which will house this recipe
        directory_recipe_name = self.new_recipe_info["name"].lower().replace(" ", "_") # This name will be used to create the folder of the recipe
        
        # Create a directory which will house the recipe and image
        os.mkdir("./data/" + directory_recipe_name) 
        
        # Copy the image uploaded by user into the the newly created recipe folder
        shutil.copy(self.new_recipe_info["path_to_image"], "./data/" + directory_recipe_name + "/image.png")
        
        # Remove the path_to_image key in new_recipe_info, as that is not required when dumping recipe info to json
        self.new_recipe_info.pop("path_to_image")
        
        # Create json file in the newly created recipe folder
        with open("./data/" + directory_recipe_name + "/info.json", "w") as f:
            json.dump(self.new_recipe_info, f, indent = 4)        
        
        # Updating recipe_index.json
        # Read the current recipes in the index
        with open("./data/recipe_index.json", "r") as f:
            current_json_index = json.load(f)
        
        current_json_index[self.new_recipe_info["name"]] = directory_recipe_name # Add the appropriate key and value to the index from the temporary dictionary
        
        # Write this newly updated dictionary back into recipe_index.json 
        with open("./data/recipe_index.json", "w") as f:
            json.dump(current_json_index, f, indent = 4)
            
        # Update comboboxes in other components, this is so that the user can see the new recipe
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)    
            
        self.list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        self.list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)        
        
        # Replace the combobox that is there to force a refresh of contents
        self.home_edit_recipes_frame_combobox = ttk.Combobox(self.home_edit_recipes_frame,
                                                             state = "readonly",
                                                             values = self.list_recipes_combobox_name,
                                                             font = "verdana 15")
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack combo box, for component 1
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = self.list_recipes_combobox_name,
                                                   font = "verdana 15")
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 1, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        # Refresh contents of view button
        self.home_choosing_to_view_recipe_frame_viewbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            # We want to parse in the name of the folder which holds the image and json of the recipe, hence we use the value of the dictionary
                                            text = "View recipe", 
                                            command=lambda: self.create_ShowRecipeFrame(dict_recipes_combobox[self.home_choosing_to_view_recipe_frame_combobox.get()]),
                                            bg = self.button_bg,
                                            fg = self.button_txt,
                                            font = "verdana 15") 
        self.home_choosing_to_view_recipe_frame_viewbutt.grid(row = 2, column = 0, 
                                                              sticky="NESW",
                                                              padx = 10,
                                                              pady = 10)        
        
        self.clear_entry_widgets() # Clear entries from all inputs
        
        self.show_frame("HomePageFrame") # Put user back to homepage
    
    
    def allow_user_to_proceed(self, frame_name):
        '''When the user presses the next button when adding recipes, we want to 
        ensure that they have entered the required information before hand.'''
        
        if self.able_to_proceed.get() == 0: # If user has not entered valid information
            if frame_name == "SaveRecipeToJsonFrame": # Custom error messages for the uploading json frame
                self.display_user_input_status.set("ERROR: Upload a valid image file.") # Change status box to inform user
            else:
                self.display_user_input_status.set("ERROR: Enter required information then press the save button.") # Change status box to inform user
        
        else:
            if frame_name == "ShowCurrentIngredientsFrame":
                self.temp_ingredient_info = [] # Reset for validation purposes
                
            self.able_to_proceed.set(0) # Reset the counter for the next frame
            self.display_user_input_status.set("----") # Reset the status box
            self.clear_entry_widgets() # Clear entries from all inputs
            self.show_frame(frame_name) # Show the next frame
     
             
    def go_to_home_instruction_frame(self):
        '''After the user has pressed save when adding an instruction, we need 
        to increment self.current_step() by one, then show the home page frame
        for adding instructions'''
        
        if self.able_to_proceed.get() == 0: # If user has entered invalid input
            self.display_user_input_status.set("ERROR: Enter required information then press the save button.") # Change status box to inform user
        else:
            self.current_step.set(self.current_step.get() + 1) # Increment the step counter by one
            self.able_to_proceed.set(0) # Reset the counter for the next frame
            self.display_user_input_status.set("----") # Reset the status box
            self.clear_entry_widgets() # Clear entries from all inputs
            self.show_frame("ShowCurrentInstructionsFrame") # Go to next frame
    
        
    def find_selected_recipe(self):
        '''Once user has selected what recipe they want to edit and push the edit
        button, this will store the .json contents in self.edited_recipe_info, 
        and change the frame'''
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)          
        
        # Find the name of the recipe as named in the directory
        directory_recipe_name = dict_recipes_combobox[self.home_edit_recipes_frame_combobox.get()] 
        
        # Set contents of that recipe into the dictionary self.edited_recipe_info
        with open("./data/" + directory_recipe_name + "/info.json") as f:
            self.edited_recipe_info = json.load(f)
         
        # Set the display name variable, so that it can be shown on the next page        
        self.display_recipe_name_edit_homepage.set(self.edited_recipe_info["name"])
        
        # Change frames
        self.show_frame("HomeEditSpecificRecipeFrame")
    

    def delete_recipe(self):
        '''Deletes the specified recipe from /data'''
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)  
        
        directory_recipe_name = self.edited_recipe_info["name"].lower().replace(" ", "_") # First find the name of the recipe in terms of the folder name
        
        shutil.rmtree("./data/" + directory_recipe_name) # Remove the data from that recipe
        
        # Updating index file
        # Read the current recipes in the index
        with open("./data/recipe_index.json", "r") as f:
            current_json_index = json.load(f)
            
        current_json_index.pop(self.edited_recipe_info["name"]) # Remove that recipe from the json index
        
        # Write this newly updated dictionary back into recipe_index.json 
        with open("./data/recipe_index.json", "w") as f:
            json.dump(current_json_index, f, indent = 4)
            
        # Update comboboxes, this is so that the user doesn't see it again once it is deleted.
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)    
            
        self.list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        self.list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)        
        
        # Replace the combobox that is there to force a refresh of contents
        self.home_edit_recipes_frame_combobox = ttk.Combobox(self.home_edit_recipes_frame,
                                                             state = "readonly",
                                                             values = self.list_recipes_combobox_name,
                                                             font = "verdana 15")
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack combo box for component 1
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = self.list_recipes_combobox_name,
                                                   font = "verdana 15")
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 1, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        self.show_frame("HomeEditRecipesFrame") # Return user to homepage
    
    
    def clear_entry_widgets(self):
        '''This will clear all entryboxes present in the program'''
        self.ask_recipe_name_frame_textbox.delete(0, END) 
        self.ask_recipe_author_source_frame_textbox.delete(0, END)
        self.ask_recipe_prep_time_frame_textbox.delete(0, END)
        self.ask_recipe_total_time_frame_textbox.delete(0, END)
        self.ask_recipe_how_many_serves_frame_textbox.delete(0, END)
        self.add_ingredient_name_frame_textbox.delete(0, END)
        self.add_ingredient_amount_frame_textbox.delete(0, END)
        self.add_ingredient_generic_text_frame_textbox.delete(0, END)
        self.add_new_instruction_frame_textbox.delete(0, END)
        self.ask_recipe_timer_frame_textbox.delete(0, END)
        
        # Clear combobox
        self.add_ingredient_quantity_type_frame_combobox.set("")
    
    
    def create_HomePageFrame(self):
        '''Creates homepage frame'''
        self.home_page_frame = Frame(self.main_container, bg = self.bg)
        self.home_page_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_page_frame.columnconfigure([0,1], minsize=150)
        self.home_page_frame.rowconfigure([0,1,2,3,4], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(5): # 5 rows
            self.home_page_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.home_page_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.home_page_frame_heading = Label(self.home_page_frame,
                                             text = "Virtual cookbook",
                                             bg = self.heading_bg,
                                             fg = self.heading_txt,
                                             font = "verdana 30 bold")
        self.home_page_frame_heading.grid(row = 0, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2,
                                          padx = 10, pady = 10)
        
        # Create and pack view recipes button
        self.home_page_frame_viewbutt = Button(self.home_page_frame,
                                               text = "View recipes",
                                               bg = self.button_bg,
                                               fg = self.button_txt,
                                               command=lambda: self.show_frame("HomeChoosingToViewRecipeFrame"),
                                               font = "verdana 15")
        self.home_page_frame_viewbutt.grid(row = 1, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack add recipes button
        self.home_page_frame_addbutt = Button(self.home_page_frame,
                                              text = "Add recipes",
                                              bg = self.button_bg,
                                              fg = self.button_txt,
                                              command=lambda: self.show_frame("AskRecipeNameFrame"),
                                              font = "verdana 15")
        self.home_page_frame_addbutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack edit recipes button
        self.home_page_frame_editbutt = Button(self.home_page_frame,
                                               text = "Edit recipes",
                                               bg = self.button_bg,
                                               fg = self.button_txt,
                                               command=lambda: self.show_frame("HomeEditRecipesFrame"),
                                               font = "verdana 15")
        self.home_page_frame_editbutt.grid(row = 3, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack setting button
        self.home_page_frame_settingsbutt = Button(self.home_page_frame,
                                                   text = "Settings",
                                                   command=lambda: self.show_frame("SettingsFrame"),
                                                   bg = self.button_bg,
                                                   fg = self.button_txt,
                                                   font = "verdana 15")
        self.home_page_frame_settingsbutt.grid(row = 4, column = 0, 
                                               sticky = "NESW", 
                                               padx = 10, pady = 10)
        
        # Create and pack quit button
        self.home_page_frame_quitbutt = Button(self.home_page_frame,
                                               text = "Quit program",
                                               command = self.quit_program,
                                               bg = self.button_bg,
                                               fg = self.button_txt,
                                               font = "verdana 15 bold")
        self.home_page_frame_quitbutt.grid(row = 4, column = 1,
                                           sticky = "NESW", padx = 10,
                                           pady = 10)
        
        return self.home_page_frame
  

    def create_SettingsFrame(self):
        '''Creates the settings window'''
        self.settings_frame = Frame(self.main_container, bg = self.bg)
        self.settings_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.settings_frame.columnconfigure([0,1], minsize=150)
        self.settings_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.settings_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.settings_frame.grid_columnconfigure(j, weight=1)    
            
        # Create and pack heading
        self.settings_frame_heading = Label(self.settings_frame,
                                            text = "Settings", 
                                            bg = self.heading_bg,
                                            fg = self.heading_txt,
                                            font = "verdana 15 bold")
        self.settings_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                         columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack subheading "Change theme"
        self.settings_frame_subhead1 = Label(self.settings_frame,
                                            text = "Change theme:",
                                            bg = self.subheading_bg,
                                            fg = self.subheading_txt,
                                            font = "verdana 15")
        self.settings_frame_subhead1.grid(row = 1, column = 0,
                                          sticky = "NESW",
                                          padx = 10, pady = 10)
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/theme_config.json") as f:
            theme_config_json = json.load(f)        
        
        list_theme_names = list(theme_config_json.keys()) # Creates a list of the non-folder names of the recipes
        
        # Remove the first entry in the list as that is not supposed to be selectable to the user
        list_theme_names.pop(0)
        
        # Create and pack combobox for changing theme
        self.settings_frame_combobox1 = ttk.Combobox(self.settings_frame,
                                                     state = "readonly",
                                                     values = list_theme_names,
                                                     font = "verdana 15") 
        self.settings_frame_combobox1.grid(row = 1, column = 1,
                                           sticky = "NESW",
                                           padx = 10, pady = 10)
        
        # Create and pack save button for settings frame
        self.settings_frame_savebutt = Button(self.settings_frame, 
                                              text = "Save theme details",
                                              bg = self.button_bg,
                                              fg = self.button_txt,
                                              command=lambda: self.set_theme(self.settings_frame_combobox1.get()),
                                              font = "verdana 15")
        self.settings_frame_savebutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack back button
        self.settings_frame_backbutt = Button(self.settings_frame,
                                              text = "Back",
                                              command=lambda: self.show_frame("HomePageFrame"),
                                              bg = self.button_bg,
                                              fg = self.button_txt,
                                              font = "verdana 15 bold")
        self.settings_frame_backbutt.grid(row = 3, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        return self.settings_frame
    
    
    def create_HomeChoosingToViewRecipeFrame(self):
        '''Menu which allows user to pick and choose a recipe'''
        # Create choose recipe frame window
        self.home_choosing_to_view_recipe_frame = Frame(self.main_container, 
                                                        bg = self.bg)
        self.home_choosing_to_view_recipe_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_choosing_to_view_recipe_frame.columnconfigure([0], minsize=150)
        self.home_choosing_to_view_recipe_frame.rowconfigure([0,1,2,3,4], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.home_choosing_to_view_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 2 column
            self.home_choosing_to_view_recipe_frame.grid_columnconfigure(j, weight=1)        
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)
        
        self.list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        self.list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)
        
        # Create and pack heading
        self.home_choosing_to_view_recipe_frame_heading = Label(self.home_choosing_to_view_recipe_frame,
                                                                text = "Viewing: Select a recipe from the combo box below",
                                                                bg = self.heading_bg,
                                                                fg = self.heading_txt,
                                                                font = "verdana 15 bold")
        self.home_choosing_to_view_recipe_frame_heading.grid(row = 0, column = 0,
                                                             sticky = "NESW",
                                                             padx = 10, pady = 10)
        
        # Create and pack combo box
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = self.list_recipes_combobox_name,
                                                   font = "verdana 15")
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 1, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        # Create and pack button which will change the view recipes frame
        self.home_choosing_to_view_recipe_frame_viewbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            # We want to parse in the name of the folder which holds the image and json of the recipe, hence we use the value of the dictionary
                                            text = "View recipe", 
                                            command=lambda: self.create_ShowRecipeFrame(dict_recipes_combobox[self.home_choosing_to_view_recipe_frame_combobox.get()]),
                                            bg = self.button_bg,
                                            fg = self.button_txt,
                                            font = "verdana 15") 
        self.home_choosing_to_view_recipe_frame_viewbutt.grid(row = 2, column = 0, 
                                                              sticky="NESW",
                                                              padx = 10,
                                                              pady = 10)
        
        # Similar to the view recipe button, except it uses a random item from the list "list_recipes_folder_name"
        self.home_choosing_to_view_recipe_frame_ranbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            text = "Pick a random recipe for me!",
                                            command=lambda: self.create_ShowRecipeFrame(random.choice(self.list_recipes_folder_name)),
                                            bg = self.button_bg,
                                            fg = self.button_txt,
                                            font = "verdana 15")
        self.home_choosing_to_view_recipe_frame_ranbutt.grid(row = 3, column = 0, 
                                                sticky = "NESW", padx = 10,
                                                pady = 10)
        
        # Create and pack back button
        self.home_choosing_to_view_recipe_frame_backbutt = Button(self.home_choosing_to_view_recipe_frame,
                                                                  text = "Back",
                                                                  bg = self.button_bg,
                                                                  fg = self.button_txt,
                                                                  command=lambda: self.show_frame("HomePageFrame"),
                                                                  font = "verdana 15 bold")
        self.home_choosing_to_view_recipe_frame_backbutt.grid(row = 4, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10, 
                                                              pady = 10)
                                            
        
        return self.home_choosing_to_view_recipe_frame
    
    
    def create_ShowRecipeFrame(self, recipe_folder_name):
        '''Creates recipe frame for chosen recipe'''
        # Creates frame for each widget in recipe frame
        self.show_recipe_frame = Frame(self.main_container, bg = self.bg)
        self.show_recipe_frame.grid(row=0, column=0, sticky="NESW")
        
        # Used in conjunction with sticky to make it fill the window
        # First column, which displays 
        
        self.show_recipe_frame.columnconfigure([0,1,2], minsize = 420) # Formatting for first 3 columns       
        self.show_recipe_frame.columnconfigure(3, minsize = 100) # Formatting for last column (timer)
        
        self.show_recipe_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.show_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(4): # 4 columns
            self.show_recipe_frame.grid_columnconfigure(j, weight=1)
        
        # Open current recipe information from info.json file
        with open("./data/" + recipe_folder_name + "/info.json") as f:
            current_recipe = json.load(f)
    
        # Show recipe name
        # Get information from json file
        self.recipe_name.set(current_recipe["name"])
        
        # Create then pack heading
        self.show_recipe_frame_heading = Label(self.show_recipe_frame, 
                                          textvariable=self.recipe_name, 
                                          bg = self.heading_bg, 
                                          fg = self.heading_txt,
                                          font = "Verdana 15 bold")
        self.show_recipe_frame_heading.grid(row = 0, column = 0, 
                                            sticky = "NESW",
                                            padx = 10, pady = 10)
        
        # Show image
        self.show_recipe_frame_image = PhotoImage(file="./data/" + recipe_folder_name + "/image.png") # Create image widget
        
        # Scaling for image 
        # Get width and height of image
        image_height_pixels = self.show_recipe_frame_image.height()
        image_width_pixels = self.show_recipe_frame_image.width()
        
        # Find the scale factor, based on the size of the image
        result_height = image_height_pixels // 500
        result_width = image_width_pixels // 600
        
        # Find the final scale factor, which we will use with .subsample()
        scale_factor = result_height + result_width
        
        self.show_recipe_frame_image = self.show_recipe_frame_image.subsample(scale_factor) # Resizes image to be smaller
        # Create then show widget with the image inside
        self.show_recipe_frame_image_frame = Label(self.show_recipe_frame, image = self.show_recipe_frame_image, 
                                                   bg = self.subheading_bg,
                                                   fg = self.subheading_txt)
        self.show_recipe_frame_image_frame.grid(row = 1, column = 0, 
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Showing other recipe information
        self.building_recipe_info = "" # Create a temporary string so that we can add info to the textbox of the recipe
        
        # Concatnate recipe information, so that info is stored all in one string
        self.building_recipe_info += f"Author/source: {current_recipe['author/source']}\n"
        self.building_recipe_info += f"Prep time: {current_recipe['prep_time']}\n"
        self.building_recipe_info += f"Total time: {current_recipe['total_time']}\n"
        self.building_recipe_info += f"Serves: {current_recipe['serves']}"
        
        # Set the variable so then the Label widget can retrive this information via textvariable
        self.recipe_info.set(self.building_recipe_info)
        
        # Show recipe info box
        self.show_recipe_frame_recipe_info_textbox = Label(self.show_recipe_frame, 
                                         textvariable=self.recipe_info, 
                                         bg = self.subheading_bg,
                                         fg = self.subheading_txt,
                                         font = "Verdana")
        self.show_recipe_frame_recipe_info_textbox.grid(row = 2, column = 0, 
                                                        sticky="NESW",
                                                        padx = 10, pady = 10)
        
        # Show recipe ingredients
        self.building_recipe_ingredients = "" # Once again we set a temporary variable which strings will be joined together
        
        self.list_of_ingredients = current_recipe["ingredients"] # Find list of ingredients from json
        for each_item in range(len(self.list_of_ingredients)): # For each ingredient, we can add it to the temporary variable
            self.building_recipe_ingredients += f"{self.list_of_ingredients[each_item]}\n\n"       
        
        # Set the concatnated information into the textvariable
        self.recipe_ingredients.set(self.building_recipe_ingredients)
        
        # Show ingredients list
        self.show_recipe_frame_ingredients_textbox = Label(self.show_recipe_frame,
                                               textvariable=self.recipe_ingredients, 
                                               bg = self.subheading_bg,
                                               fg = self.subheading_txt, 
                                               justify = LEFT,
                                               wraplength = 400,
                                               font = "verdana 8")
        self.show_recipe_frame_ingredients_textbox.grid(row = 0, column = 1, 
                                                        sticky="NESW",
                                                        rowspan = 3,
                                                        padx = 10, pady = 10)
        
        # Show recipe instructions
        self.building_recipe_instructions = "" # Create a temporary string which we will use to display the recipe instructions
        
        self.list_of_instructions = current_recipe["instructions"] # Create a variable which stores the instructions in a dictionary format
        
        # We now loop through each item in the dictionary
        for each_step in self.list_of_instructions:
            self.building_recipe_instructions += f"{each_step.title()}: {self.list_of_instructions[each_step]}\n\n"        
            
        # Set the textvariable which will be used in the label
        self.recipe_instructions.set(self.building_recipe_instructions)
        
        # Create then pack recipe instructions
        self.show_recipe_frame_instructions_textbox = Label(self.show_recipe_frame,
                                         textvariable=self.recipe_instructions,
                                         wraplength=400, justify = LEFT,
                                         bg = self.subheading_bg,
                                         fg = self.subheading_txt,
                                         font = "verdana 8")
        self.show_recipe_frame_instructions_textbox.grid(row = 0, column = 2, 
                                                         sticky="NESW",
                                                         rowspan = 3,
                                                         padx = 10, pady = 10)
        
        # Getting timer information from json file
        self.timer_in_min = current_recipe["timer_set_to"] # Find the set timer in minutes from json file
        self.recipe_timer.set(self.timer_in_min) # Set the timer label to what is found in the json file
        self.timer_in_sec = self.timer_in_min * 60 # Convert minutes to seconds, which will be used for our calculations

        # Time textlabel
        self.show_recipe_frame_timer_label = Label(self.show_recipe_frame, textvariable=self.recipe_timer, 
                                 bg = self.subheading_bg,
                                 fg = self.subheading_txt,
                                 font = "verdana 15")
        self.show_recipe_frame_timer_label .grid(row = 0, column = 3, 
                                                 sticky = "NESW", padx = 10,
                                                 pady = 10)
        
        # Timer start button
        #self.show_recipe_frame_timer_startbutt = Button(self.show_recipe_frame, 
                                                        #text = "Start timer",
                                                        #command=self.run_timer)
        #self.show_recipe_frame_timer_startbutt.grid(row = 1, column = 3, 
                                                    #sticky = "NESW",
                                                    #padx = 10, pady = 10)
        
        # Back button (return to main menu)
        self.show_recipe_frame_backbutt = Button(self.show_recipe_frame, text = "Back",
                                  command=lambda: self.show_frame("HomeChoosingToViewRecipeFrame"),
                                  bg = self.button_bg,
                                  fg = self.button_txt,
                                  font = "verdana 15 bold")
        self.show_recipe_frame_backbutt.grid(row = 3, column = 0, columnspan = 4, 
                                             sticky="NESW", padx = 10, pady = 10)        
        
        return self.show_recipe_frame
    
    
    def create_AskRecipeNameFrame(self):
        '''Asks for recipe name window'''
        # Sets up window
        self.ask_recipe_name_frame = Frame(self.main_container, bg = self.bg)
        self.ask_recipe_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_name_frame.columnconfigure([0,1,2], minsize=150)
        self.ask_recipe_name_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_name_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.ask_recipe_name_frame.grid_columnconfigure(j, weight=1)         
        
        # Creating and packing heading widget
        self.ask_recipe_name_frame_heading = Label(self.ask_recipe_name_frame,
                                                   text = "Enter name of recipe (e.g 'muffins') in text box below, then press 'save', then 'next'.",
                                                   bg = self.heading_bg,
                                                   fg = self.heading_txt,
                                                   font = "verdana 15 bold",
                                                   wraplength = 800)
        self.ask_recipe_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                                columnspan = 3, padx = 10, 
                                                pady = 10)
        
        # Creating and packing text box
        self.ask_recipe_name_frame_textbox = Entry(self.ask_recipe_name_frame,
                                                   bg = self.subheading_bg,
                                                   fg = self.subheading_txt,
                                                   font = "verdana 15")
        self.ask_recipe_name_frame_textbox.grid(row = 1, column = 0,
                                                columnspan = 3,
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Create next button
        self.ask_recipe_name_frame_nextbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Next",
                                                     command=lambda: self.allow_user_to_proceed("AskRecipeAuthorSourceFrame"),
                                                     bg = self.button_bg,
                                                     fg = self.button_txt,
                                                     font = "verdana 15")
        self.ask_recipe_name_frame_nextbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Create save button to store value in self.new_recipe_info
        self.ask_recipe_name_frame_savebutt = Button(self.ask_recipe_name_frame,
                                                     text = "Save",
                                                     command=lambda: self.save_information("name", self.ask_recipe_name_frame_textbox.get()),
                                                     bg = self.button_bg,
                                                     fg = self.button_txt,
                                                     font = "verdana 15 bold") 
        self.ask_recipe_name_frame_savebutt.grid(row = 2, column = 1, 
                                                 sticky = "NESW",
                                                 padx = 10, pady = 10)
        
        # Create and pack back button to return to main menu
        self.ask_recipe_name_frame_backbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Back to main menu",
                                                     bg = self.button_bg,
                                                     fg = self.button_txt,
                                                     command=lambda: self.show_frame("HomePageFrame"),
                                                     font = "verdana 15")
        self.ask_recipe_name_frame_backbutt.grid(row = 2, column = 2,
                                                 sticky = "NESW", padx = 10,
                                                 pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_frame_statusbox = Label(self.ask_recipe_name_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 3)
        
        return self.ask_recipe_name_frame
    
    
    def create_AskRecipeAuthorSourceFrame(self):
        '''Window which asks user for author/source'''
        # Set up window
        self.ask_recipe_author_source_frame = Frame(self.main_container,
                                                    bg = self.bg)
        self.ask_recipe_author_source_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_author_source_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_author_source_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_author_source_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_author_source_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading widget
        self.ask_recipe_author_source_frame_heading = Label(self.ask_recipe_author_source_frame,
                                                            text = "Enter author's name or source of recipe (e.g 'Matthew') in text box below then press 'save', then 'next'.",
                                                            bg = self.heading_bg,
                                                            fg = self.heading_txt,
                                                            font = "verdana 15 bold",
                                                            wraplength = 800)
        self.ask_recipe_author_source_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 2,
                                                         padx = 10, pady = 10)
        # Create and pack text box
        self.ask_recipe_author_source_frame_textbox = Entry(self.ask_recipe_author_source_frame,
                                                            bg = self.subheading_bg,
                                                            fg = self.subheading_txt,
                                                            font = "verdana 15")
        self.ask_recipe_author_source_frame_textbox.grid(row = 1, column = 0,
                                                         sticky = "NESW", 
                                                         columnspan = 2,
                                                         padx = 10, pady = 10)
        
        # Create next button and pack next button
        self.ask_recipe_author_source_frame_nextbutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Next",
                                                              command=lambda: self.allow_user_to_proceed("AskRecipePrepTimeFrame"),
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15")
        self.ask_recipe_author_source_frame_nextbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_author_source_frame_savebutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("author/source", self.ask_recipe_author_source_frame_textbox.get()),
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15 bold")
        self.ask_recipe_author_source_frame_savebutt.grid(row = 2, column = 1,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_author_source_frame_statusbox = Label(self.ask_recipe_author_source_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_author_source_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 2)        
        
        return self.ask_recipe_author_source_frame
    
    
    def create_AskRecipePrepTimeFrame(self):
        '''Creates window to ask for prep time'''
        self.ask_recipe_prep_time_frame = Frame(self.main_container, bg = 
                                                self.bg)
        self.ask_recipe_prep_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_prep_time_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_prep_time_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_prep_time_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_prep_time_frame.grid_columnconfigure(j, weight=1)          
        
        # Create and pack heading widget
        self.ask_recipe_prep_time_frame_heading = Label(self.ask_recipe_prep_time_frame,
                                                        text = "Enter prep time of recipe (e.g '15 minutes') in text box below, then press 'save', then 'next'.",
                                                        bg = self.heading_bg,
                                                        fg = self.heading_txt,
                                                        font = "verdana 15 bold",
                                                        wraplength = 800)
        self.ask_recipe_prep_time_frame_heading.grid(row = 0, column = 0,
                                                     sticky = "NESW", 
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack text box widget
        self.ask_recipe_prep_time_frame_textbox = Entry(self.ask_recipe_prep_time_frame,
                                                        bg = self.subheading_bg,
                                                        fg = self.subheading_txt,
                                                        font = "verdana 15")
        self.ask_recipe_prep_time_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack next button
        self.ask_recipe_prep_time_frame_nextbutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Next",
                                                          command=lambda: self.allow_user_to_proceed("AskRecipeTotalTimeFrame"),
                                                          bg = self.button_bg,
                                                          fg = self.button_txt,
                                                          font = "verdana 15")
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_prep_time_frame_savebutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Save",
                                                          command=lambda: self.save_information("prep_time", self.ask_recipe_prep_time_frame_textbox.get()),
                                                          bg = self.button_bg,
                                                          fg = self.button_txt,
                                                          font = "verdana 15 bold")
        self.ask_recipe_prep_time_frame_savebutt.grid(row = 2, column = 1,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_prep_time_frame_statusbox = Label(self.ask_recipe_prep_time_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_prep_time_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 2)        
        
        return self.ask_recipe_prep_time_frame
    
    
    def create_AskRecipeTotalTimeFrame(self):
        '''Creates window which asks user for total time to make recipe'''
        self.ask_recipe_total_time_frame = Frame(self.main_container,
                                                 bg = self.bg)
        self.ask_recipe_total_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_total_time_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_total_time_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_total_time_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_total_time_frame.grid_columnconfigure(j, weight=1)         
        
        # Create and pack heading widget
        self.ask_recipe_total_time_frame_heading = Label(self.ask_recipe_total_time_frame,
                                                         text = "Enter total cooking time (e.g '30 minutes') in text box below, then press 'save', then 'next'.",
                                                         bg = self.heading_bg,
                                                         fg = self.heading_txt,
                                                         font = "verdana 15 bold",
                                                         wraplength = 800)
        self.ask_recipe_total_time_frame_heading.grid(row = 0, column = 0,
                                                      sticky = "NESW", 
                                                      columnspan = 2,
                                                      padx = 10, pady = 10)
        
        # Create and pack entry box so that user can enter how long in total it will take to make that recipe
        self.ask_recipe_total_time_frame_textbox = Entry(self.ask_recipe_total_time_frame,
                                                         bg = self.subheading_bg,
                                                         fg = self.subheading_txt,
                                                         font = "verdana 15")
        self.ask_recipe_total_time_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2,
                                                      padx = 10, pady = 10)
        
        # Create and pack next button, to move onto asking how many servings is this recipe for
        self.ask_recipe_total_time_frame_nextbutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Next",
                                                           command=lambda: self.allow_user_to_proceed("AskRecipeHowManyServesFrame"),
                                                           bg = self.button_bg,
                                                           fg = self.button_txt,
                                                           font = "verdana 15")
        self.ask_recipe_total_time_frame_nextbutt.grid(row = 2, column = 0,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Create and pack save button, to save total time required to make this recipe
        self.ask_recipe_total_time_frame_savebutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_information("total_time", self.ask_recipe_total_time_frame_textbox.get()),
                                                           bg = self.button_bg,
                                                           fg = self.button_txt,
                                                           font = "verdana 15 bold")
        self.ask_recipe_total_time_frame_savebutt.grid(row = 2, column = 1,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_total_time_frame_statusbox = Label(self.ask_recipe_total_time_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_total_time_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 2)
        
        return self.ask_recipe_total_time_frame
    
    
    def create_AskRecipeHowManyServesFrame(self):
        '''Creates window which allows user to input how many people this recipe serves'''
        self.ask_recipe_how_many_serves_frame = Frame(self.main_container,
                                                      bg = self.bg)
        self.ask_recipe_how_many_serves_frame.grid(row = 0, column = 0,
                                                   sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_how_many_serves_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_how_many_serves_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_how_many_serves_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_how_many_serves_frame.grid_columnconfigure(j, weight=1)         
            
        # Creates and packs heading widget
        self.ask_recipe_how_many_serves_frame_heading = Label(self.ask_recipe_how_many_serves_frame,
                                                              text = "Enter how many people this recipe serves (e.g 'four') in the text box below, then press 'save', then 'next.",
                                                              bg = self.heading_bg,
                                                              fg = self.heading_txt,
                                                              font = "verdana 15 bold",
                                                              wraplength = 800)
        self.ask_recipe_how_many_serves_frame_heading.grid(row = 0, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs entry box for user to input number of servings
        self.ask_recipe_how_many_serves_frame_textbox = Entry(self.ask_recipe_how_many_serves_frame,
                                                              bg = self.subheading_bg,
                                                              fg = self.subheading_txt,
                                                              font = "verdana 15")
        self.ask_recipe_how_many_serves_frame_textbox.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs next button, which will move onto asking for ingredients
        self.ask_recipe_how_many_serves_frame_nextbutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Next",
                                                                command=lambda: self.allow_user_to_proceed("ShowCurrentIngredientsFrame"),
                                                                bg = self.button_bg,
                                                                fg = self.button_txt,
                                                                font = "verdana 15")
        self.ask_recipe_how_many_serves_frame_nextbutt.grid(row = 2, column = 0,
                                                            sticky = "NESW",
                                                            padx = 10, pady = 10)
        
        # Creates and packs save button, to save current information into self.new_recipe_info
        self.ask_recipe_how_many_serves_frame_savebutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Save",
                                                                command=lambda: self.save_information("serves", self.ask_recipe_how_many_serves_frame_textbox.get()),
                                                                bg = self.button_bg,
                                                                fg = self.button_txt,
                                                                font = "verdana 15 bold")
        self.ask_recipe_how_many_serves_frame_savebutt.grid(row = 2, column = 1,
                                                            sticky = "NESW",
                                                            padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_how_many_serves_frame_statusbox = Label(self.ask_recipe_how_many_serves_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_how_many_serves_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 2)        
        
        return self.ask_recipe_how_many_serves_frame
    
    
    def create_ShowCurrentIngredientsFrame(self):
        '''Shows current ingredients added to new recipe'''
        # Setting up frame
        self.show_current_ingredients_frame = Frame(self.main_container,
                                                    bg = self.bg)
        self.show_current_ingredients_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.show_current_ingredients_frame.columnconfigure([0,1,2], minsize=150)
        self.show_current_ingredients_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.show_current_ingredients_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.show_current_ingredients_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading widget
        self.show_current_ingredients_frame_heading = Label(self.show_current_ingredients_frame,
                                                            text = "Below is the ingredient(s) you have added so far to this recipe. \n\n To add an ingredient, press the 'add' button. \n\n Once you are finished, press 'save' then 'next'.",
                                                            bg = self.heading_bg,
                                                            fg = self.heading_txt,
                                                            font = "verdana 15 bold",
                                                            wraplength = 800)
        self.show_current_ingredients_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 3,
                                                         padx = 10, pady = 10)
        
        # Create and pack "current list of ingredients"
        self.show_current_ingredients_frame_list = Label(self.show_current_ingredients_frame,
                                                         textvariable = self.display_ingredients,
                                                         bg = self.subheading_bg,
                                                         fg = self.subheading_txt,
                                                         font = "verdana 8")
        self.show_current_ingredients_frame_list.grid(row = 1, column = 0,
                                                      sticky = "NESW",
                                                      columnspan = 3,
                                                      padx = 10, pady = 10)
        
        # Create and pack "add ingredients" button
        self.show_current_ingredients_frame_addbutt = Button(self.show_current_ingredients_frame,
                                                             text = "Add",
                                                             command=lambda: self.show_frame("AddIngredientQuantityTypeFrame"),
                                                             bg = self.button_bg,
                                                             fg = self.button_txt,
                                                             font = "verdana 15")
        self.show_current_ingredients_frame_addbutt.grid(row = 2, column = 0,
                                                         sticky = "NESW",
                                                         padx = 10, pady = 10)
        
        # Create and pack "next" button
        self.show_current_ingredients_frame_nextbutt = Button(self.show_current_ingredients_frame,
                                                              text = "Next",
                                                              command=lambda: self.allow_user_to_proceed("ShowCurrentInstructionsFrame"),
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15")
        self.show_current_ingredients_frame_nextbutt.grid(row = 2, column = 1,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack save button, which will add everything self.ingredient_info into self.new_recipe_info
        self.show_current_ingredients_frame_savebutt = Button(self.show_current_ingredients_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("ingredients", self.new_ingredient_info),
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15 bold")
        self.show_current_ingredients_frame_savebutt.grid(row = 2, column = 2,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.show_current_ingredients_frame_statusbox = Label(self.show_current_ingredients_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.show_current_ingredients_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 3)      
        
        return self.show_current_ingredients_frame
        
        
    def create_AddIngredientQuantityTypeFrame(self):
        '''Asks user for ingredient quantity type'''
        self.add_ingredient_quantity_type_frame = Frame(self.main_container,
                                                        bg = self.bg)
        self.add_ingredient_quantity_type_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_quantity_type_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_quantity_type_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.add_ingredient_quantity_type_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_quantity_type_frame.grid_columnconfigure(j, weight=1) 
            
        # Create heading and pack heading
        self.add_ingredient_quantity_type_frame_heading = Label(self.add_ingredient_quantity_type_frame,
                                                                text = "You are now adding an ingredient: \n\n Select a quantity type from the combo box below (e.g 'Gram (g)', then press 'save', then 'next'.",
                                                                bg = self.heading_bg,
                                                                fg = self.heading_txt,
                                                                font = "verdana 15 bold",
                                                                wraplength = 800)
        self.add_ingredient_quantity_type_frame_heading.grid(row = 0, column = 0,
                                                             sticky = "NESW",
                                                             columnspan = 2,
                                                             padx = 10, 
                                                             pady = 10)
        
        # This will open up the dictionary which stores all the valid quantity types, used for the combo box
        with open("./data/quantity_types.json") as f:
            quantity_types_combobox = json.load(f)
            
        # Find all the keys in the dictionary and then put it in one list
        quantity_types_keys = list(quantity_types_combobox.keys())
        
        # Create and pack combo box 
        self.add_ingredient_quantity_type_frame_combobox = ttk.Combobox(self.add_ingredient_quantity_type_frame,
                                                                        state = "readonly", # So that user cannot add their own quantity values
                                                                        values = quantity_types_keys,
                                                                        font = "verdana 15") # Set values to what is in the dictionary keys
        self.add_ingredient_quantity_type_frame_combobox.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              columnspan = 2,
                                                              padx = 10,
                                                              pady = 10)
        
        # Create and pack next button, to move onto asking the ingredient name or generic text if the user has selected that option
        self.add_ingredient_quantity_type_frame_nextbutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Next",
                                                                  command=self.create_generic_text_or_other_frame, # Special case, as user might want to add generic text
                                                                  bg = self.button_bg,
                                                                  fg = self.button_txt,
                                                                  font = "verdana 15")
        self.add_ingredient_quantity_type_frame_nextbutt.grid(row = 2, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10,
                                                              pady = 10)
        
        # Create and pack save button, to save information to self.temp_ingredient_info
        self.add_ingredient_quantity_type_frame_savebutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Save",
                                                                  command=lambda: self.save_temp_ingredient_info("quantity_type", self.add_ingredient_quantity_type_frame_combobox.get()),
                                                                  bg = self.button_bg,
                                                                  fg = self.button_txt,
                                                                  font = "verdana 15 bold") 
        self.add_ingredient_quantity_type_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW",
                                                             padx = 10,
                                                             pady = 10)
        
        return self.add_ingredient_quantity_type_frame
    
    
    def create_AddIngredientNameFrame(self):
        '''Asks user for ingredient name when adding new ingredients'''
        self.add_ingredient_name_frame = Frame(self.main_container, bg = self.bg)
        self.add_ingredient_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_name_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_name_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.add_ingredient_name_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_name_frame.grid_columnconfigure(j, weight=1)
            
        # Create and pack heading
        self.add_ingredient_name_frame_heading = Label(self.add_ingredient_name_frame,
                                                       text = "You are now adding an ingredient: \n\n Enter name of ingredient (e.g 'all-purpose flour') in the text box below, then press 'save' then 'next'.",
                                                       bg = self.heading_bg,
                                                       fg = self.heading_txt,
                                                       font = "verdana 15 bold",
                                                       wraplength = 800)
        self.add_ingredient_name_frame_heading.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack text box which stores name of ingredient
        self.add_ingredient_name_frame_textbox = Entry(self.add_ingredient_name_frame,
                                                       bg = self.subheading_bg,
                                                       fg = self.subheading_txt,
                                                       font = "verdana 15")
        self.add_ingredient_name_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack save button
        self.add_ingredient_name_frame_savebutt = Button(self.add_ingredient_name_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_temp_ingredient_info("quantity_name", self.add_ingredient_name_frame_textbox.get()),
                                                         bg = self.button_bg,
                                                         fg = self.button_txt,
                                                         font = "verdana 15 bold") 
        self.add_ingredient_name_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack next button
        self.add_ingredient_name_frame_nextbutt = Button(self.add_ingredient_name_frame,
                                                         text = "Next",
                                                         command=lambda: self.allow_user_to_proceed("AddIngredientAmountFrame"),
                                                         bg = self.button_bg,
                                                         fg = self.button_txt,
                                                         font = "verdana 15")
        self.add_ingredient_name_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.add_ingredient_name_frame_statusbox = Label(self.add_ingredient_name_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.add_ingredient_name_frame_statusbox.grid(row = 3, column = 0, 
                                                      sticky = "NESW", 
                                                      columnspan = 2)        
        
        return self.add_ingredient_name_frame
    
    
    def create_AddIngredientAmountFrame(self):
        '''Asks user for the amount of that ingredient which they have chosen'''
        self.add_ingredient_amount_frame = Frame(self.main_container, 
                                                 bg = self.bg)
        self.add_ingredient_amount_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_amount_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_amount_frame.rowconfigure([0,1,2,3,4], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(5): # 5 rows
            self.add_ingredient_amount_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_amount_frame .grid_columnconfigure(j, weight=1)
            
        # Creates and packs heading
        self.add_ingredient_amount_frame_heading1 = Label(self.add_ingredient_amount_frame,
                                                         text = "Enter amount of this ingredient named:",
                                                         bg = self.heading_bg,
                                                         fg = self.heading_txt,
                                                         font = "verdana 15")
        self.add_ingredient_amount_frame_heading1.grid(row = 0, column = 0, 
                                                      sticky = "NESW", 
                                                      padx = 10,
                                                      pady = 10)
        
        # Creates and displays the name of the ingredient, entered in a previous page
        self.add_ingredient_amount_frame_quantityname = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_name,
                                                              bg = self.heading_bg,
                                                              fg = self.heading_txt,
                                                              font = "verdana 15 bold")
        self.add_ingredient_amount_frame_quantityname.grid(row = 0, column = 1,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        # Creates and packs entrybox
        self.add_ingredient_amount_frame_textbox = Entry(self.add_ingredient_amount_frame,
                                                         bg = self.subheading_bg,
                                                         fg = self.subheading_txt,
                                                         font = "verdana 15")
        self.add_ingredient_amount_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2, padx = 10,
                                                      pady = 10)
        
        # Creates and packs heading for "in"
        self.add_ingredient_amount_frame_heading2 = Label(self.add_ingredient_amount_frame,
                                                          text = "in the quantity type:",
                                                          bg = self.subheading_bg,
                                                          fg = self.subheading_txt,
                                                          font = "verdana 15")
        self.add_ingredient_amount_frame_heading2.grid(row = 2, column = 0,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Creates and displays quantity type of ingredient, entered on a previous page
        self.add_ingredient_amount_frame_quantitytype = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_type,
                                                              bg = self.subheading_bg,
                                                              fg = self.subheading_txt,
                                                              font = "verdana 15 bold")
        self.add_ingredient_amount_frame_quantitytype.grid(row = 2, column = 1,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        # Creates and packs next button
        self.add_ingredient_amount_frame_nextbutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Next",
                                                           command=lambda: self.allow_user_to_proceed("ShowCurrentIngredientsFrame"),
                                                           bg = self.button_bg,
                                                           fg = self.button_txt,
                                                           font = "verdana 15")
        self.add_ingredient_amount_frame_nextbutt.grid(row = 3, column = 0,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Creates and packs save button, which will add the quantity amount to the temp ingredient dictionary
        self.add_ingredient_amount_frame_savebutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_temp_ingredient_info("quantity_amount", self.add_ingredient_amount_frame_textbox.get()),
                                                           bg = self.button_bg,
                                                           fg = self.button_txt,
                                                           font = "verdana 15 bold")
        self.add_ingredient_amount_frame_savebutt.grid(row = 3, column = 1,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.add_ingredient_amount_frame_statusbox = Label(self.add_ingredient_amount_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.add_ingredient_amount_frame_statusbox.grid(row = 4, column = 0, 
                                                      sticky = "NESW", 
                                                      columnspan = 2)        
        
        return self.add_ingredient_amount_frame
    
    
    def create_AddIngredientGenericTextFrame(self):
        '''If user chooses quantity type = "generic text", they will be put on this frame'''
        self.add_ingredient_generic_text_frame = Frame(self.main_container,
                                                       bg = self.bg)
        self.add_ingredient_generic_text_frame.grid(row = 0, column = 0,
                                                    sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_generic_text_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_generic_text_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.add_ingredient_generic_text_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_generic_text_frame.grid_columnconfigure(j, weight=1)
            
        # Create and pack heading
        self.add_ingredient_generic_text_frame_heading = Label(self.add_ingredient_generic_text_frame,
                                                               text = "You are now adding an ingredient: \n\n Enter generic text in entry box below (e.g '1 large egg'), then press 'save', then 'next'.",
                                                               bg = self.heading_bg,
                                                               fg = self.heading_txt,
                                                               font = "verdana 15 bold",
                                                               wraplength = 800)
        self.add_ingredient_generic_text_frame_heading.grid(row = 0, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2,
                                                            padx = 10, 
                                                            pady = 10)
        
        # Creates and packs textbox, where user can input whatever they need for the ingredient
        self.add_ingredient_generic_text_frame_textbox = Entry(self.add_ingredient_generic_text_frame,
                                                               bg = self.subheading_bg,
                                                               fg = self.subheading_txt,
                                                               font = "verdana 15")
        self.add_ingredient_generic_text_frame_textbox.grid(row = 1, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2,
                                                            padx = 10,
                                                            pady = 10)
        
        # Creates and packs next button
        self.add_ingredient_generic_text_frame_nextbutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Next",
                                                                 command=lambda: self.allow_user_to_proceed("ShowCurrentIngredientsFrame"),
                                                                 bg = self.button_bg,
                                                                 fg = self.button_txt,
                                                                 font = "verdana 15")
        self.add_ingredient_generic_text_frame_nextbutt.grid(row = 2, column = 0,
                                                             sticky = "NESW",
                                                             padx = 10, 
                                                             pady = 10)
        
        # Creates and packs save button
        self.add_ingredient_generic_text_frame_savebutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Save",
                                                                 command=lambda: self.save_temp_ingredient_info("generic_text",  self.add_ingredient_generic_text_frame_textbox.get()),
                                                                 bg = self.button_bg,
                                                                 fg = self.button_txt,
                                                                 font = "verdana 15 bold")
        self.add_ingredient_generic_text_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW",
                                                             padx = 10, 
                                                             pady = 10)
        
        # Create and pack status box at bottom
        self.add_ingredient_generic_text_frame_statusbox = Label(self.add_ingredient_generic_text_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.add_ingredient_generic_text_frame_statusbox.grid(row = 3, column = 0, 
                                                      sticky = "NESW", 
                                                      columnspan = 2)        
        
                                                               
        
        return self.add_ingredient_generic_text_frame
    
    
    def create_ShowCurrentInstructionsFrame(self):
        '''When the user wants to add instructions, this frame will show them all the instructions they have added so far'''
        self.show_current_instructions_frame = Frame(self.main_container, 
                                                     bg = self.bg)
        self.show_current_instructions_frame.grid(row = 0, column = 0,
                                                  sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.show_current_instructions_frame.columnconfigure([0,1,2], minsize=150)
        self.show_current_instructions_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.show_current_instructions_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.show_current_instructions_frame.grid_columnconfigure(j, weight=1)          
        
        # Create and pack heading widget
        self.show_current_instructions_frame_heading = Label(self.show_current_instructions_frame,
                                                             text = "Below are the instruction(s) you have added so far to this recipe. \n\n To add a new instruction, press the 'add' button. \n\n Once you are finished, press 'save' then 'next'.",
                                                             bg = self.heading_bg,
                                                             fg = self.heading_txt,
                                                             font = "verdana 15 bold",
                                                             wraplength = 800)
        self.show_current_instructions_frame_heading.grid(row = 0, column = 0,
                                                          sticky = "NESW",
                                                          columnspan = 3,
                                                          padx = 10, pady = 10)
        
        # Create and pack label which will display what steps the user has added so far
        self.show_current_instructions_frame_list = Label(self.show_current_instructions_frame,
                                                          textvariable = self.display_instructions,
                                                          wraplength = 500,
                                                          bg = self.subheading_bg,
                                                          fg = self.subheading_txt,
                                                          font = "verdana 8")
        self.show_current_instructions_frame_list.grid(row = 1, column = 0,
                                                       sticky = "NESW",
                                                       columnspan = 3,
                                                       padx = 10, pady = 10)
        
        # Create and pack add button, so that user can add a instruction
        self.show_current_instructions_frame_addbutt = Button(self.show_current_instructions_frame,
                                                              text = "Add",
                                                              command=lambda: self.show_frame("AddNewInstructionFrame"),
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15")
        self.show_current_instructions_frame_addbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack next button, which is asking for the timer input
        self.show_current_instructions_frame_nextbutt = Button(self.show_current_instructions_frame,
                                                               text = "Next",
                                                               command=lambda: self.allow_user_to_proceed("AskRecipeTimerFrame"),
                                                               bg = self.button_bg,
                                                               fg = self.button_txt,
                                                               font = "verdana 15")
        self.show_current_instructions_frame_nextbutt.grid(row = 2, column = 1, 
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        # Create and pack save button, to save all instructions to new_recipe_info
        self.show_current_instructions_frame_savebutt = Button(self.show_current_instructions_frame,
                                                               text = "Save",
                                                               command=lambda: self.save_information("instructions", self.new_instruction_info),
                                                               bg = self.button_bg,
                                                               fg = self.button_txt,
                                                               font = "verdana 15 bold")
        self.show_current_instructions_frame_savebutt.grid(row = 2, column = 2,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.show_current_instructions_frame_statusbox = Label(self.show_current_instructions_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.show_current_instructions_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 3)        
        
        return self.show_current_instructions_frame
    
    
    def create_AddNewInstructionFrame(self):
        '''This frame allows the user to input and save a new instruction to their recipe'''
        self.add_new_instruction_frame = Frame(self.main_container,
                                               bg = self.bg)
        self.add_new_instruction_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_new_instruction_frame.columnconfigure([0,1], minsize=150)
        self.add_new_instruction_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.add_new_instruction_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_new_instruction_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.add_new_instruction_frame_heading = Label(self.add_new_instruction_frame,
                                                       text = "Enter one instruction into the entry box below (e.g 'Pour 500g of flour into...'), then press 'save', then 'next'.",
                                                       bg = self.heading_bg,
                                                       fg = self.heading_txt,
                                                       font = "verdana 15 bold",
                                                       wraplength = 800)
        self.add_new_instruction_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack text box for inputting instruction
        self.add_new_instruction_frame_textbox = Entry(self.add_new_instruction_frame,
                                                       bg = self.subheading_bg,
                                                       fg = self.subheading_txt,
                                                       font = "verdana 15")
        self.add_new_instruction_frame_textbox.grid(row = 1, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack next button, which will return the user back to the show_current_ingredients_frame
        self.add_new_instruction_frame_nextbutt = Button(self.add_new_instruction_frame,
                                                         text = "Next",
                                                         command=lambda: self.go_to_home_instruction_frame(),
                                                         bg = self.button_bg,
                                                         fg = self.button_txt,
                                                         font = "verdana 15")
        self.add_new_instruction_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack save button
        self.add_new_instruction_frame_savebutt = Button(self.add_new_instruction_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_instruction_info(self.add_new_instruction_frame_textbox.get()),
                                                         bg = self.button_bg,
                                                         fg = self.button_txt,
                                                         font = "verdana 15 bold")
        self.add_new_instruction_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.add_new_instruction_frame_statusbox = Label(self.add_new_instruction_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.add_new_instruction_frame_statusbox.grid(row = 3, column = 0, 
                                                      sticky = "NESW", 
                                                      columnspan = 2)        
        
        
        return self.add_new_instruction_frame
        
    
    def create_AskRecipeTimerFrame(self):
        '''This will ask the user what they want to set the timer for this recipe'''
        self.ask_recipe_timer_frame = Frame(self.main_container, bg = self.bg)
        self.ask_recipe_timer_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_timer_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_timer_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.ask_recipe_timer_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_timer_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading when user is inputting integer for timer
        self.ask_recipe_timer_frame_heading = Label(self.ask_recipe_timer_frame,
                                                    text = "Enter the number of minutes you want to set the timer to (e.g '20'), then press 'save', then 'next'.",
                                                    bg = self.heading_bg,
                                                    fg = self.heading_txt,
                                                    font = "verdana 15 bold",
                                                    wraplength = 800)
        self.ask_recipe_timer_frame_heading.grid(row = 0, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2, padx = 10,
                                                 pady = 10)
        
        # Create and pack textbox for user input
        self.ask_recipe_timer_frame_textbox = Entry(self.ask_recipe_timer_frame,
                                                    bg = self.subheading_bg,
                                                    fg = self.subheading_txt,
                                                    font = "verdana 15")
        self.ask_recipe_timer_frame_textbox.grid(row = 1, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2,
                                                 padx = 10, pady = 10)
        
        # Create and pack next button
        self.ask_recipe_timer_frame_nextbutt = Button(self.ask_recipe_timer_frame,
                                                     text = "Next",
                                                     command=lambda: self.allow_user_to_proceed("UploadImageFrame"),
                                                     bg = self.button_bg,
                                                     fg = self.button_txt,
                                                     font = "verdana 15")
        self.ask_recipe_timer_frame_nextbutt.grid(row = 2, column = 0,
                                                  sticky = "NESW",
                                                  padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_timer_frame_savebutt = Button(self.ask_recipe_timer_frame,
                                                      text = "Save",
                                                      command=lambda: self.save_information("timer_set_to", self.ask_recipe_timer_frame_textbox.get()),
                                                      bg = self.button_bg,
                                                      fg = self.button_txt,
                                                      font = "verdana 15 bold") 
        self.ask_recipe_timer_frame_savebutt.grid(row = 2, column = 1,
                                                  sticky = "NESW",
                                                  padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.ask_recipe_timer_frame_statusbox = Label(self.ask_recipe_timer_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.ask_recipe_timer_frame_statusbox.grid(row = 3, column = 0, sticky = "NESW",
                                          columnspan = 2)
        
        return self.ask_recipe_timer_frame
    
    
    def create_UploadImageFrame(self):
        '''This is the frame where the user can upload an image to add to their recipe'''
        self.upload_image_frame = Frame(self.main_container, bg = self.bg)
        self.upload_image_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.upload_image_frame.columnconfigure([0,1], minsize=150)
        self.upload_image_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.upload_image_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.upload_image_frame.grid_columnconfigure(j, weight=1) 
            
        # Create and pack heading
        self.upload_image_frame_heading = Label(self.upload_image_frame, 
                                                text = "Press the upload button to add an image to your recipe. Images must be in .png format, with a size greater than 640x480. Then press 'next'.",
                                                bg = self.heading_bg,
                                                fg = self.heading_txt,
                                                font = "verdana 15 bold",
                                                wraplength = 800)
        self.upload_image_frame_heading.grid(row = 0, column = 0, 
                                             sticky = "NESW",
                                             columnspan = 2,
                                             padx = 10, pady = 10)
        
        # Create and pack next button
        self.upload_image_frame_nextbutt = Button(self.upload_image_frame,
                                                  text = "Next",
                                                  command=lambda: self.allow_user_to_proceed("SaveRecipeToJsonFrame"),
                                                  bg = self.button_bg,
                                                  fg = self.button_txt,
                                                  font = "verdana 15")
        self.upload_image_frame_nextbutt.grid(row = 1, column = 0,
                                              sticky = "NESW",
                                              padx = 10, pady = 10)
        
        # Create and pack upload button
        self.upload_image_frame_upbutt = Button(self.upload_image_frame,
                                                text = "Upload",
                                                command = self.upload_file,
                                                bg = self.button_bg,
                                                fg = self.button_txt,
                                                font = "verdana 15 bold")
        self.upload_image_frame_upbutt.grid(row = 1, column = 1,
                                            sticky = "NESW",
                                            padx = 10, pady = 10)
        
        # Create and pack status box at bottom
        self.upload_image_frame_statusbox = Label(self.upload_image_frame,
                                             textvariable = self.display_user_input_status,
                                             bg = self.subheading_bg,
                                             fg = self.subheading_txt,
                                             font = "verdana 15")
        self.upload_image_frame_statusbox.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2)        

        return self.upload_image_frame
    
    
    def create_SaveRecipeToJsonFrame(self):
        '''This frame is where the user will dump the info to json'''
        self.save_recipe_to_json_frame = Frame(self.main_container, bg = self.bg)
        self.save_recipe_to_json_frame.grid(row = 0, column = 0,
                                            sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.save_recipe_to_json_frame.columnconfigure([0], minsize=150)
        self.save_recipe_to_json_frame.rowconfigure([0,1], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(2): # 2 rows
            self.save_recipe_to_json_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 2 columns
            self.save_recipe_to_json_frame.grid_columnconfigure(j, weight=1) 
        
        # Create and pack heading
        self.save_recipe_to_json_frame_heading = Label(self.save_recipe_to_json_frame,
                                                      text = "Press the save button below to add you recipe. You will return to the homepage automatically.",
                                                      bg = self.heading_bg,
                                                      fg = self.heading_txt,
                                                      font = "verdana 15 bold",
                                                      wraplength = 800)
        self.save_recipe_to_json_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack savebutton
        self.save_recipe_to_json_frame_savebutt = Button(self.save_recipe_to_json_frame,
                                                         text = "Save recipe",
                                                         command = self.dump_new_recipe_to_json,
                                                         bg = self.button_bg,
                                                         fg = self.button_txt,
                                                         font = "verdana 15")
        self.save_recipe_to_json_frame_savebutt.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        return self.save_recipe_to_json_frame
    
    
    def create_HomeEditRecipesFrame(self):
        '''Creates homepage frame for adding recipes'''
        self.home_edit_recipes_frame = Frame(self.main_container, bg = self.bg)
        self.home_edit_recipes_frame.grid(row = 0, column = 0, sticky = "NESW") 
        
        # Used in conjunction with sticky to make it fill the window
        self.home_edit_recipes_frame.columnconfigure([0], minsize=150)
        self.home_edit_recipes_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.home_edit_recipes_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 1 column
            self.home_edit_recipes_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.home_edit_recipes_frame_heading = Label(self.home_edit_recipes_frame,
                                                     text = "Editing: Select a recipe below via the combo box, then press the edit button.",
                                                     bg = self.heading_bg,
                                                     fg = self.heading_txt,
                                                     font = "verdana 15 bold")
        self.home_edit_recipes_frame_heading.grid(row = 0, column = 0,
                                                  sticky = "NESW",
                                                  padx = 10, pady = 10)
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)        
        
        self.list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Used for the combobox   
        
        # Create and pack combobox
        self.home_edit_recipes_frame_combobox = ttk.Combobox(self.home_edit_recipes_frame,
                                                             state = "readonly",
                                                             values = self.list_recipes_combobox_name,
                                                             font = "verdana 15")
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack "edit!" button
        self.home_edit_recipes_frame_editbutt = Button(self.home_edit_recipes_frame,
                                                       text = "Edit!",
                                                       command = self.find_selected_recipe,
                                                       bg = self.button_bg,
                                                       fg = self.button_txt,
                                                       font = "verdana 15")
        self.home_edit_recipes_frame_editbutt.grid(row = 2, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack back button 
        self.home_edit_recipes_frame_backbutt = Button(self.home_edit_recipes_frame,
                                                               text = "Back",
                                                               bg = self.button_bg,
                                                               fg = self.button_txt,
                                                               command=lambda: self.show_frame("HomePageFrame"),
                                                               font = "verdana 15 bold")
        self.home_edit_recipes_frame_backbutt.grid(row = 3, column = 0,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)        
        
        
        return self.home_edit_recipes_frame
    
    
    def create_HomeEditSpecificRecipeFrame(self):
        '''This serves as the main page for when the user selects a recipe they 
        want to edit'''
        self.home_edit_specific_recipe_frame = Frame(self.main_container,
                                                     bg = self.bg)
        self.home_edit_specific_recipe_frame.grid(row = 0, column = 0, 
                                                  sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_edit_specific_recipe_frame.columnconfigure([0], minsize=150)
        self.home_edit_specific_recipe_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.home_edit_specific_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 1 column
            self.home_edit_specific_recipe_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.home_edit_specific_recipe_frame_heading = Label(self.home_edit_specific_recipe_frame,
                                                             text = "Editings details for recipe named:",
                                                             bg = self.heading_bg,
                                                             fg = self.heading_txt,
                                                             font = "verdana 15 bold")
        self.home_edit_specific_recipe_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         padx = 10)
        
        # Create and pack recipe name
        self.home_edit_specific_recipe_frame_displayname = Label(self.home_edit_specific_recipe_frame,
                                                                 textvariable = self.display_recipe_name_edit_homepage,
                                                                 bg = self.subheading_bg,
                                                                 fg = self.subheading_txt,
                                                                 font = "verdana 15")
        self.home_edit_specific_recipe_frame_displayname.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10)
        
        # Create and pack delete recipe button
        self.home_edit_specific_recipe_frame_delbutt = Button(self.home_edit_specific_recipe_frame,
                                                              text = "Delete recipe",
                                                              command = self.delete_recipe,
                                                              bg = self.button_bg,
                                                              fg = self.button_txt,
                                                              font = "verdana 15")
        self.home_edit_specific_recipe_frame_delbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack back button 
        self.home_edit_specific_recipe_frame_backbutt = Button(self.home_edit_specific_recipe_frame,
                                                               text = "Back",
                                                               command=lambda: self.show_frame("HomeEditRecipesFrame"),
                                                               bg = self.button_bg,
                                                               fg = self.button_txt,
                                                               font = "verdana 15 bold")
        self.home_edit_specific_recipe_frame_backbutt.grid(row = 3, column = 0,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        return self.home_edit_specific_recipe_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()