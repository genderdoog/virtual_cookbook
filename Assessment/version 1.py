"""
Virtual cookbook software

Created by: Matthew C
Created on: 15/08/25

Version 1: minimum viable product GUI
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
        self.root.title("Component 4 - Version 1")
        
        # Make the root window expandable
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)        
        
        # Generate main window container
        self.main_container = Frame(self.root)
        self.main_container.grid(row=0, column=0, sticky="NESW")
        
        # Make the main container expandable
        self.main_container.grid_rowconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(0, weight=1)
        
        # Variables for viewing recipe component
        # Initialise strings used to output recipe information
        self.recipe_name = StringVar()
        self.name_of_author_source = StringVar()
        self.recipe_info = StringVar()
        self.recipe_ingredients = StringVar()
        self.recipe_instructions = StringVar()
        
        # Set up timer textvariable for timer
        self.recipe_timer = StringVar()        
        
        # Variables for adding recipe component
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
        
        # Variables for editing recipes component
        self.edited_recipe_info = {}
        self.display_recipe_name_edit_homepage = StringVar()        
        
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
        
        # Create dictionary to store what windows are in our program
        self.windows = {}
        
        # Windows for main menu component
        self.windows["HomePageFrame"] = self.create_HomePageFrame() # Main menu of program
        self.windows["SettingsFrame"] = self.create_SettingsFrame() # Settings frame
        
        # Windows for viewing recipes component
        self.windows["HomeChoosingToViewRecipeFrame"] = self.create_HomeChoosingToViewRecipeFrame()
        self.windows["ShowRecipeFrame"] = self.create_ShowRecipeFrame("chocolate_chip_cookie") # We add an example recipe into the function 
        
        # Windows for adding recipes component
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
        
        # Windows for editing recipes component
        self.windows["HomeEditRecipesFrame"] = self.create_HomeEditRecipesFrame()
        # Homepage for a specific recipe
        self.windows["HomeEditSpecificRecipeFrame"] = self.create_HomeEditSpecificRecipeFrame()        
        
        # Show this frame when program first starts
        self.show_frame("HomePageFrame")
    
        
    def show_frame(self, name):
        '''Show a frame, then bring it to the top'''
        frame = self.windows[name]
        frame.tkraise()
        
    
    def run(self):
        '''Run program'''
        self.root.mainloop() 
     
    def run_timer(self):
        '''Runs the timer of a recipe'''
        self.recipe_timer.set(f"{self.timer_in_sec // 60}:{self.timer_in_sec % 60}")
        self.timer_in_sec -= 1    
     
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
        
        # Change the settings of each frame
        
        # Homepage frame
        self.home_page_frame.configure(bg = self.bg) 
        self.home_page_frame_heading.configure(bg = self.heading_bg,
                                               fg = self.heading_txt)
        self.home_page_frame_viewbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        self.home_page_frame_addbutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_editbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        self.home_page_frame_settingsbutt.configure(bg = self.button_bg,
                                                    fg = self.button_txt)
        self.home_page_frame_quitbutt.configure(bg = self.button_bg,
                                                fg = self.button_txt)
        
        # Settings frame
        self.settings_frame.configure(bg = self.bg)
        self.settings_frame_heading.configure(bg = self.heading_bg, 
                                              fg = self.heading_txt)
        self.settings_frame_subhead1.configure(bg = self.subheading_bg,
                                               fg = self.subheading_txt)
        self.settings_frame_savebutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        self.settings_frame_backbutt.configure(bg = self.button_bg,
                                               fg = self.button_txt)
        
        
        # To make it persistent across application restarts, we change the first variable of the json file
        theme_config_json["chosen_theme"] = theme_name
        
        # Then write the theme file back
        with open("./data/theme_config.json", "w") as f:
            json.dump(theme_config_json, f, indent = 4)
     
    def save_information(self, data_type, info):
        '''When the users presses this button when adding recipes, it saves it to the main dictionary'''
        if data_type == "name": # This clears the values, when user adds recipes back to back.
            self.new_recipe_info = {} # Creates the main dictionary which we will then dump to a json file
            self.temp_ingredient_info = [] # This will store information which will then be concatnated to then be added to new_ingredient_info
            self.new_ingredient_info = [] # This is the final list of all ingredients, which will be added to new_recipe_info            
            self.new_instruction_info = {} # This will be added to new_recipe_info as the value of the key "instructions"
            self.current_step.set(1) # On reset, we set it to 1
            self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
            print(self.new_recipe_info)            
            
        
        else:# For all other frames other than asking for the recipe name
            self.new_recipe_info[data_type] = info # Stores data_type name and value e.g. {"name": "chocolate chip cookie"} where name is data_type and chocolate chip cookie is info
            print(self.new_recipe_info)     
   
   
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
            
        # Update combobox so that user can immediately view recipe after they have added it
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)
        
        list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)
        
        # Create and pack combo box
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = list_recipes_combobox_name)
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
            
        self.create_HomePageFrame() # Places user back to main menu
            
    
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
            
        # Update combobox, this is so that the user doesn't see it again once it is deleted.
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)        
        
        self.list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        
        # Replace the combobox that is there to force a refresh of contents
        self.home_edit_recipes_frame_combobox = ttk.Combobox(self.home_edit_recipes_frame,
                                                             state = "readonly",
                                                             values = self.list_recipes_combobox_name)
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW")
        
        self.show_frame("HomeEditRecipesFrame") # Return user to homepage    
            
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
                                             fg = self.heading_txt)
        self.home_page_frame_heading.grid(row = 0, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2,
                                          padx = 10, pady = 10)
        
        # Create and pack view recipes button
        self.home_page_frame_viewbutt = Button(self.home_page_frame,
                                               text = "View recipes",
                                               command=lambda: self.show_frame("HomeChoosingToViewRecipeFrame"),
                                               bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_viewbutt.grid(row = 1, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack add recipes button
        self.home_page_frame_addbutt = Button(self.home_page_frame,
                                              text = "Add recipes",
                                              command=lambda: self.show_frame("AskRecipeNameFrame"),
                                              bg = self.button_bg,
                                              fg = self.button_txt)
        self.home_page_frame_addbutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack edit recipes button
        self.home_page_frame_editbutt = Button(self.home_page_frame,
                                               text = "Edit recipes",
                                               command=lambda: self.show_frame("HomeEditRecipesFrame"),
                                               bg = self.button_bg,
                                               fg = self.button_txt)
        self.home_page_frame_editbutt.grid(row = 3, column = 0, sticky = "NESW",
                                           columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack setting button
        self.home_page_frame_settingsbutt = Button(self.home_page_frame,
                                                   text = "Settings",
                                                   command=lambda: self.show_frame("SettingsFrame"),
                                                   bg = self.button_bg,
                                                   fg = self.button_txt)
        self.home_page_frame_settingsbutt.grid(row = 4, column = 0, 
                                               sticky = "NESW", 
                                               padx = 10, pady = 10)
        
        # Create and pack quit button
        self.home_page_frame_quitbutt = Button(self.home_page_frame,
                                               text = "Quit program",
                                               command = self.quit_program,
                                               bg = self.button_bg,
                                               fg = self.button_txt)
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
        self.settings_frame.rowconfigure([0,1,2,3,4,5], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.settings_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.settings_frame.grid_columnconfigure(j, weight=1)    
            
        # Create and pack heading
        self.settings_frame_heading = Label(self.settings_frame,
                                            text = "Settings", 
                                            bg = self.heading_bg,
                                            fg = self.heading_txt)
        self.settings_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                         columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack subheading "Change theme"
        self.settings_frame_subhead1 = Label(self.settings_frame,
                                            text = "Change theme:",
                                            bg = self.subheading_bg,
                                            fg = self.subheading_txt)
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
                                                     values = list_theme_names)
        self.settings_frame_combobox1.grid(row = 1, column = 1,
                                           sticky = "NESW",
                                           padx = 10, pady = 10)
        
        # Create and pack save button for settings frame
        self.settings_frame_savebutt = Button(self.settings_frame, 
                                              text = "Save theme details",
                                              bg = self.button_bg,
                                              fg = self.button_txt,
                                              command=lambda: self.set_theme(self.settings_frame_combobox1.get()))
        self.settings_frame_savebutt.grid(row = 2, column = 0, sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        # Create and pack back button
        self.settings_frame_backbutt = Button(self.settings_frame,
                                              text = "Back",
                                              command=lambda: self.show_frame("HomePageFrame"),
                                              bg = self.button_bg,
                                              fg = self.button_txt)
        self.settings_frame_backbutt.grid(row = 3, column = 0,
                                          sticky = "NESW",
                                          columnspan = 2, padx = 10, pady = 10)
        
        return self.settings_frame
    
    
    def create_HomeChoosingToViewRecipeFrame(self):
        '''Menu which allows user to pick and choose a recipe'''
        # Create choose recipe frame window
        self.home_choosing_to_view_recipe_frame = Frame(self.main_container)
        self.home_choosing_to_view_recipe_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.home_choosing_to_view_recipe_frame.columnconfigure([0], minsize=150)
        self.home_choosing_to_view_recipe_frame.rowconfigure([0,1,2,3], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(4): # 4 rows
            self.home_choosing_to_view_recipe_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(1): # 2 column
            self.home_choosing_to_view_recipe_frame.grid_columnconfigure(j, weight=1)        
        
        # This will open up the dictionary which stores the actual name given by the user, and the name of the folder.
        with open("./data/recipe_index.json") as f:
            dict_recipes_combobox = json.load(f)
        
        list_recipes_combobox_name = list(dict_recipes_combobox.keys()) # Creates a list of the non-folder names of the recipes
        list_recipes_folder_name = list(dict_recipes_combobox.values()) # Creates a list which is of the folder type names of each recipe (used for random recipe button)
        
        # Create and pack combo box
        self.home_choosing_to_view_recipe_frame_combobox = ttk.Combobox(self.home_choosing_to_view_recipe_frame, 
                                                   state = "readonly",
                                                   values = list_recipes_combobox_name)
        self.home_choosing_to_view_recipe_frame_combobox.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        # Create and pack button which will change the view recipes frame
        self.home_choosing_to_view_recipe_frame_viewbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            # We want to parse in the name of the folder which holds the image and json of the recipe, hence we use the value of the dictionary
                                            text = "View recipe", command=lambda: self.create_ShowRecipeFrame(dict_recipes_combobox[self.home_choosing_to_view_recipe_frame_combobox.get()])) 
        self.home_choosing_to_view_recipe_frame_viewbutt.grid(row = 1, column = 0, 
                                                              sticky="NESW",
                                                              padx = 10,
                                                              pady = 10)
        
        # Similar to the view recipe button, except it uses a random item from the list "list_recipes_folder_name"
        self.home_choosing_to_view_recipe_frame_ranbutt = Button(self.home_choosing_to_view_recipe_frame, 
                                            text = "Pick a random recipe for me!",
                                            command=lambda: self.create_ShowRecipeFrame(random.choice(list_recipes_folder_name)))
        self.home_choosing_to_view_recipe_frame_ranbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW", padx = 10,
                                                pady = 10)
        
        # Create and pack back button
        self.home_choosing_to_view_recipe_frame_backbutt = Button(self.home_choosing_to_view_recipe_frame,
                                                                  text = "Back",
                                                                  command=lambda: self.show_frame("HomePageFrame"))
        self.home_choosing_to_view_recipe_frame_backbutt.grid(row = 3, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10, 
                                                              pady = 10)        
                                            
        
        return self.home_choosing_to_view_recipe_frame
    
    
    def create_ShowRecipeFrame(self, recipe_folder_name):
        '''Creates recipe frame for chosen recipe'''
        # Creates frame for each widget in recipe frame
        self.show_recipe_frame = Frame(self.main_container)
        self.show_recipe_frame.grid(row=0, column=0, sticky="NESW")
        
        # Used in conjunction with sticky to make it fill the window
        # First column, which displays 
        
        self.show_recipe_frame.columnconfigure(0, minsize = 300)
        self.show_recipe_frame.columnconfigure(1, minsize = 350)
        self.show_recipe_frame.columnconfigure(2, minsize = 420) # Formatting for instructions        
        self.show_recipe_frame.columnconfigure(3, minsize = 100)
        
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
                                          bg="orange", font = "Verdana 25 bold")
        self.show_recipe_frame_heading.grid(row = 0, column = 0, 
                                            sticky = "NESW",
                                            padx = 10, pady = 10)
        
        # Show image
        self.show_recipe_frame_image = PhotoImage(file="./data/" + recipe_folder_name + "/image.png") # Create image widget
        self.show_recipe_frame_image = self.show_recipe_frame_image.subsample(12) # Resizes image to be smaller
        # Create then show widget with the image inside
        self.show_recipe_frame_image_frame = Label(self.show_recipe_frame, image = self.show_recipe_frame_image, bg="green")
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
                                         textvariable=self.recipe_info, bg="yellow",
                                         font = "Verdana 12")
        self.show_recipe_frame_recipe_info_textbox.grid(row = 2, column = 0, 
                                                        sticky="NESW",
                                                        padx = 10, pady = 10)
        
        # Show recipe ingredients
        self.building_recipe_ingredients = "" # Once again we set a temporary variable which strings will be joined together
        
        self.list_of_ingredients = current_recipe["ingredients"] # Find list of ingredients from json
        for each_item in range(len(self.list_of_ingredients)): # For each ingredient, we can add it to the temporary variable
            self.building_recipe_ingredients += f"{self.list_of_ingredients[each_item]}\n"       
        
        # Set the concatnated information into the textvariable
        self.recipe_ingredients.set(self.building_recipe_ingredients)
        
        # Show ingredients list
        self.show_recipe_frame_ingredients_textbox = Label(self.show_recipe_frame,
                                               textvariable=self.recipe_ingredients, 
                                               bg="red", justify = LEFT)
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
                                         wraplength=400, justify = LEFT)
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
                                 bg="yellow")
        self.show_recipe_frame_timer_label .grid(row = 0, column = 3, 
                                                 sticky = "NESW", padx = 10,
                                                 pady = 10)
        
        # Timer start button
        self.show_recipe_frame_timer_startbutt = Button(self.show_recipe_frame, 
                                                        text = "Start timer",
                                                        command=self.run_timer)
        self.show_recipe_frame_timer_startbutt.grid(row = 1, column = 3, 
                                                    sticky = "NESW",
                                                    padx = 10, pady = 10)
        
        # Back button (return to main menu)
        self.show_recipe_frame_backbutt = Button(self.show_recipe_frame, text = "Back",
                                  command=lambda: self.show_frame("HomeChoosingToViewRecipeFrame"))
        self.show_recipe_frame_backbutt.grid(row = 3, column = 0, columnspan = 4, 
                                             sticky="NESW", padx = 10, pady = 10)        
        
        return self.show_recipe_frame    
    
    
    def create_AskRecipeNameFrame(self):
        '''Asks for recipe name window'''
        # Sets up window
        self.ask_recipe_name_frame = Frame(self.main_container)
        self.ask_recipe_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_name_frame.columnconfigure([0,1,2], minsize=150)
        self.ask_recipe_name_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_name_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.ask_recipe_name_frame.grid_columnconfigure(j, weight=1)         
        
        # Creating and packing heading widget
        self.ask_recipe_name_frame_heading = Label(self.ask_recipe_name_frame,
                                                   text = "Enter name of recipe:")
        self.ask_recipe_name_frame_heading.grid(row = 0, column = 0, sticky = "NESW",
                                                columnspan = 3, padx = 10, 
                                                pady = 10)
        
        # Creating and packing text box
        self.ask_recipe_name_frame_textbox = Entry(self.ask_recipe_name_frame)
        self.ask_recipe_name_frame_textbox.grid(row = 1, column = 0,
                                                columnspan = 3,
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Create next button
        self.ask_recipe_name_frame_nextbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("AskRecipeAuthorSourceFrame"))
        self.ask_recipe_name_frame_nextbutt.grid(row = 2, column = 0, 
                                                sticky = "NESW",
                                                padx = 10, pady = 10)
        
        # Create save button to store value in self.new_recipe_info
        self.ask_recipe_name_frame_savebutt = Button(self.ask_recipe_name_frame,
                                                     text = "Save",
                                                     command=lambda: self.save_information("name", self.ask_recipe_name_frame_textbox.get())) 
        self.ask_recipe_name_frame_savebutt.grid(row = 2, column = 1, 
                                                 sticky = "NESW",
                                                 padx = 10, pady = 10)
        
        # Create and pack back button to return to main menu
        self.ask_recipe_name_frame_backbutt = Button(self.ask_recipe_name_frame,
                                                     text = "Back",
                                                     command=lambda: self.show_frame("HomePageFrame"))
        self.ask_recipe_name_frame_backbutt.grid(row = 2, column = 2,
                                                 sticky = "NESW", padx = 10,
                                                 pady = 10)
        
        return self.ask_recipe_name_frame
    
    
    def create_AskRecipeAuthorSourceFrame(self):
        '''Window which asks user for author/source'''
        # Set up window
        self.ask_recipe_author_source_frame = Frame(self.main_container)
        self.ask_recipe_author_source_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_author_source_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_author_source_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_author_source_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_author_source_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading widget
        self.ask_recipe_author_source_frame_heading = Label(self.ask_recipe_author_source_frame,
                                                            text = "Enter author/source of recipe:")
        self.ask_recipe_author_source_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 2,
                                                         padx = 10, pady = 10)
        # Create and pack text box
        self.ask_recipe_author_source_frame_textbox = Entry(self.ask_recipe_author_source_frame)
        self.ask_recipe_author_source_frame_textbox.grid(row = 1, column = 0,
                                                         sticky = "NESW", 
                                                         columnspan = 2,
                                                         padx = 10, pady = 10)
        
        # Create next button and pack next button
        self.ask_recipe_author_source_frame_nextbutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("AskRecipePrepTimeFrame"))
        self.ask_recipe_author_source_frame_nextbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_author_source_frame_savebutt = Button(self.ask_recipe_author_source_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("author/source", self.ask_recipe_author_source_frame_textbox.get()))
        self.ask_recipe_author_source_frame_savebutt.grid(row = 2, column = 1,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
                                                              
        
        return self.ask_recipe_author_source_frame
    
    
    def create_AskRecipePrepTimeFrame(self):
        '''Creates window to ask for prep time'''
        self.ask_recipe_prep_time_frame = Frame(self.main_container)
        self.ask_recipe_prep_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_prep_time_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_prep_time_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_prep_time_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_prep_time_frame.grid_columnconfigure(j, weight=1)          
        
        # Create and pack heading widget
        self.ask_recipe_prep_time_frame_heading = Label(self.ask_recipe_prep_time_frame,
                                                        text = "Enter prep time:")
        self.ask_recipe_prep_time_frame_heading.grid(row = 0, column = 0,
                                                     sticky = "NESW", 
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack text box widget
        self.ask_recipe_prep_time_frame_textbox = Entry(self.ask_recipe_prep_time_frame)
        self.ask_recipe_prep_time_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack next button
        self.ask_recipe_prep_time_frame_nextbutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Next",
                                                          command=lambda: self.show_frame("AskRecipeTotalTimeFrame"))
        self.ask_recipe_prep_time_frame_nextbutt.grid(row = 2, column = 0,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_prep_time_frame_savebutt = Button(self.ask_recipe_prep_time_frame,
                                                          text = "Save",
                                                          command=lambda: self.save_information("prep_time", self.ask_recipe_prep_time_frame_textbox.get()))
        self.ask_recipe_prep_time_frame_savebutt.grid(row = 2, column = 1,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        return self.ask_recipe_prep_time_frame
    
    
    def create_AskRecipeTotalTimeFrame(self):
        '''Creates window which asks user for total time to make recipe'''
        self.ask_recipe_total_time_frame = Frame(self.main_container)
        self.ask_recipe_total_time_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_total_time_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_total_time_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_total_time_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_total_time_frame.grid_columnconfigure(j, weight=1)         
        
        # Create and pack heading widget
        self.ask_recipe_total_time_frame_heading = Label(self.ask_recipe_total_time_frame,
                                                         text = "Enter total cooking time:")
        self.ask_recipe_total_time_frame_heading.grid(row = 0, column = 0,
                                                      sticky = "NESW", 
                                                      columnspan = 2,
                                                      padx = 10, pady = 10)
        
        # Create and pack entry box so that user can enter how long in total it will take to make that recipe
        self.ask_recipe_total_time_frame_textbox = Entry(self.ask_recipe_total_time_frame)
        self.ask_recipe_total_time_frame_textbox.grid(row = 1, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2,
                                                      padx = 10, pady = 10)
        
        # Create and pack next button, to move onto asking how many servings is this recipe for
        self.ask_recipe_total_time_frame_nextbutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("AskRecipeHowManyServesFrame"))
        self.ask_recipe_total_time_frame_nextbutt.grid(row = 2, column = 0,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Create and pack save button, to save total time required to make this recipe
        self.ask_recipe_total_time_frame_savebutt = Button(self.ask_recipe_total_time_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_information("total_time", self.ask_recipe_total_time_frame_textbox.get()))
        self.ask_recipe_total_time_frame_savebutt.grid(row = 2, column = 1,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        return self.ask_recipe_total_time_frame
    
    def create_AskRecipeHowManyServesFrame(self):
        '''Creates window which allows user to input how many people this recipe serves'''
        self.ask_recipe_how_many_serves_frame = Frame(self.main_container)
        self.ask_recipe_how_many_serves_frame.grid(row = 0, column = 0,
                                                   sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_how_many_serves_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_how_many_serves_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_how_many_serves_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_how_many_serves_frame.grid_columnconfigure(j, weight=1)         
            
        # Creates and packs heading widget
        self.ask_recipe_how_many_serves_frame_heading = Label(self.ask_recipe_how_many_serves_frame,
                                                              text = "How many people does this recipe serve?")
        self.ask_recipe_how_many_serves_frame_heading.grid(row = 0, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs entry box for user to input number of servings
        self.ask_recipe_how_many_serves_frame_textbox = Entry(self.ask_recipe_how_many_serves_frame)
        self.ask_recipe_how_many_serves_frame_textbox.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs next button, which will move onto asking for ingredients
        self.ask_recipe_how_many_serves_frame_nextbutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Next",
                                                                command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.ask_recipe_how_many_serves_frame_nextbutt.grid(row = 2, column = 0,
                                                            sticky = "NESW",
                                                            padx = 10, pady = 10)
        
        # Creates and packs save button, to save current information into self.new_recipe_info
        self.ask_recipe_how_many_serves_frame_savebutt = Button(self.ask_recipe_how_many_serves_frame,
                                                                text = "Save",
                                                                command=lambda: self.save_information("serves", self.ask_recipe_how_many_serves_frame_textbox.get()))
        self.ask_recipe_how_many_serves_frame_savebutt.grid(row = 2, column = 1,
                                                            sticky = "NESW",
                                                            padx = 10, pady = 10)
        
        return self.ask_recipe_how_many_serves_frame
    
    
    def create_ShowCurrentIngredientsFrame(self):
        '''Shows current ingredients added to new recipe'''
        # Setting up frame
        self.show_current_ingredients_frame = Frame(self.main_container)
        self.show_current_ingredients_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.show_current_ingredients_frame.columnconfigure([0,1,2], minsize=150)
        self.show_current_ingredients_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.show_current_ingredients_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.show_current_ingredients_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading widget
        self.show_current_ingredients_frame_heading = Label(self.show_current_ingredients_frame,
                                                            text = "Current ingredients:",
                                                            wraplength = 0)
        self.show_current_ingredients_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         columnspan = 3,
                                                         padx = 10, pady = 10)
        
        # Create and pack "current list of ingredients"
        self.show_current_ingredients_frame_list = Label(self.show_current_ingredients_frame,
                                                         textvariable = self.display_ingredients)
        self.show_current_ingredients_frame_list.grid(row = 1, column = 0,
                                                      sticky = "NESW",
                                                      columnspan = 3,
                                                      padx = 10, pady = 10)
        
        # Create and pack "add ingredients" button
        self.show_current_ingredients_frame_addbutt = Button(self.show_current_ingredients_frame,
                                                             text = "Add",
                                                             command=lambda: self.show_frame("AddIngredientQuantityTypeFrame"))
        self.show_current_ingredients_frame_addbutt.grid(row = 2, column = 0,
                                                         sticky = "NESW",
                                                         padx = 10, pady = 10)
        
        # Crreat and pack save button, which will add everything self.ingredient_info into self.new_recipe_info
        self.show_current_ingredients_frame_savebutt = Button(self.show_current_ingredients_frame,
                                                              text = "Save",
                                                              command=lambda: self.save_information("ingredients", self.new_ingredient_info))
        self.show_current_ingredients_frame_savebutt.grid(row = 2, column = 2,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack "next" button
        self.show_current_ingredients_frame_nextbutt = Button(self.show_current_ingredients_frame,
                                                              text = "Next",
                                                              command=lambda: self.show_frame("ShowCurrentInstructionsFrame"))
        self.show_current_ingredients_frame_nextbutt.grid(row = 2, column = 1,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        return self.show_current_ingredients_frame
        
        
    def create_AddIngredientQuantityTypeFrame(self):
        '''Asks user for ingredient quantity type'''
        self.add_ingredient_quantity_type_frame = Frame(self.main_container)
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
                                                                text = "Enter quantity type:")
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
                                                                        values = quantity_types_keys) # Set values to what is in the dictionary keys
        self.add_ingredient_quantity_type_frame_combobox.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              columnspan = 2,
                                                              padx = 10,
                                                              pady = 10)
        
        # Create and pack next button, to move onto asking the ingredient name or generic text if the user has selected that option
        self.add_ingredient_quantity_type_frame_nextbutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Next",
                                                                  command=self.create_generic_text_or_other_frame)
        self.add_ingredient_quantity_type_frame_nextbutt.grid(row = 2, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10,
                                                              pady = 10)
        
        # Create and pack save button, to save information to self.temp_ingredient_info
        self.add_ingredient_quantity_type_frame_savebutt = Button(self.add_ingredient_quantity_type_frame,
                                                                  text = "Save",
                                                                  command=lambda: self.save_temp_ingredient_info("quantity_type", self.add_ingredient_quantity_type_frame_combobox.get())) 
        self.add_ingredient_quantity_type_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW",
                                                             padx = 10,
                                                             pady = 10)
        
        return self.add_ingredient_quantity_type_frame

    
    def create_AddIngredientNameFrame(self):
        '''Asks user for ingredient name when adding new ingredients'''
        self.add_ingredient_name_frame = Frame(self.main_container)
        self.add_ingredient_name_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_name_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_name_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.add_ingredient_name_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_name_frame.grid_columnconfigure(j, weight=1)
            
        # Create and pack heading
        self.add_ingredient_name_frame_heading = Label(self.add_ingredient_name_frame,
                                                       text = "Enter name of ingredient:")
        self.add_ingredient_name_frame_heading.grid(row = 0, column = 0, 
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack text box which stores name of ingredient
        self.add_ingredient_name_frame_textbox = Entry(self.add_ingredient_name_frame)
        self.add_ingredient_name_frame_textbox.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     columnspan = 2,
                                                     padx = 10, pady = 10)
        
        # Create and pack save button
        self.add_ingredient_name_frame_savebutt = Button(self.add_ingredient_name_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_temp_ingredient_info("quantity_name", self.add_ingredient_name_frame_textbox.get())) 
        self.add_ingredient_name_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack next button
        self.add_ingredient_name_frame_nextbutt = Button(self.add_ingredient_name_frame,
                                                         text = "Next",
                                                         command=lambda: self.show_frame("AddIngredientAmountFrame"))
        self.add_ingredient_name_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        return self.add_ingredient_name_frame
    
    
    def create_AddIngredientAmountFrame(self):
        '''Asks user for the amount of that ingredient which they have chosen'''
        self.add_ingredient_amount_frame = Frame(self.main_container)
        self.add_ingredient_amount_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_amount_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_amount_frame.rowconfigure([0,1,2,3,4,5], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(6): # 3 rows
            self.add_ingredient_amount_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_amount_frame .grid_columnconfigure(j, weight=1)
            
        # Creates and packs heading
        self.add_ingredient_amount_frame_heading1 = Label(self.add_ingredient_amount_frame,
                                                         text = "Enter amount of this ingredient type ")
        self.add_ingredient_amount_frame_heading1.grid(row = 0, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2, padx = 10,
                                                      pady = 10)
        
        # Creates and displays the name of the ingredient, entered in a previous page
        self.add_ingredient_amount_frame_quantityname = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_name)
        self.add_ingredient_amount_frame_quantityname.grid(row = 1, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs entrybox
        self.add_ingredient_amount_frame_textbox = Entry(self.add_ingredient_amount_frame)
        self.add_ingredient_amount_frame_textbox.grid(row = 2, column = 0, 
                                                      sticky = "NESW",
                                                      columnspan = 2, padx = 10,
                                                      pady = 10)
        
        # Creates and packs heading for "in"
        self.add_ingredient_amount_frame_heading2 = Label(self.add_ingredient_amount_frame,
                                                          text = "in")
        self.add_ingredient_amount_frame_heading2.grid(row = 3, column = 0,
                                                       sticky = "NESW",
                                                       columnspan = 2,
                                                       padx = 10, pady = 10)
        
        # Creates and displays quantity type of ingredient, entered on a previous page
        self.add_ingredient_amount_frame_quantitytype = Label(self.add_ingredient_amount_frame,
                                                              textvariable = self.display_ingredient_type)
        self.add_ingredient_amount_frame_quantitytype.grid(row = 4, column = 0,
                                                           sticky = "NESW",
                                                           columnspan = 2,
                                                           padx = 10, pady = 10)
        
        # Creates and packs next button
        self.add_ingredient_amount_frame_nextbutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Next",
                                                           command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_amount_frame_nextbutt.grid(row = 5, column = 0,
                                                       sticky = "NESW",
                                                       padx = 10, pady = 10)
        
        # Creates and packs save button, which will add the quantity amount to the temp ingredient dictionary
        self.add_ingredient_amount_frame_savebutt = Button(self.add_ingredient_amount_frame,
                                                           text = "Save",
                                                           command=lambda: self.save_temp_ingredient_info("quantity_amount", self.add_ingredient_amount_frame_textbox.get()))
        self.add_ingredient_amount_frame_savebutt.grid(row = 5, column = 1,
                                                      sticky = "NESW",
                                                      padx = 10, pady = 10)
        
        return self.add_ingredient_amount_frame
    
    def create_AddIngredientGenericTextFrame(self):
        '''If user chooses quantity type = "generic text", they will be put on this frame'''
        self.add_ingredient_generic_text_frame = Frame(self.main_container)
        self.add_ingredient_generic_text_frame.grid(row = 0, column = 0,
                                                    sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_ingredient_generic_text_frame.columnconfigure([0,1], minsize=150)
        self.add_ingredient_generic_text_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.add_ingredient_generic_text_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_ingredient_generic_text_frame.grid_columnconfigure(j, weight=1)
            
        # Create and pack heading
        self.add_ingredient_generic_text_frame_heading = Label(self.add_ingredient_generic_text_frame,
                                                               text = "Enter generic text here: ")
        self.add_ingredient_generic_text_frame_heading.grid(row = 0, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2,
                                                            padx = 10, 
                                                            pady = 10)
        
        # Creates and packs textbox, where user can input whatever they need for the ingredient
        self.add_ingredient_generic_text_frame_textbox = Entry(self.add_ingredient_generic_text_frame)
        self.add_ingredient_generic_text_frame_textbox.grid(row = 1, column = 0,
                                                            sticky = "NESW",
                                                            columnspan = 2,
                                                            padx = 10,
                                                            pady = 10)
        
        # Creates and packs next button
        self.add_ingredient_generic_text_frame_nextbutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Next",
                                                                 command=lambda: self.show_frame("ShowCurrentIngredientsFrame"))
        self.add_ingredient_generic_text_frame_nextbutt.grid(row = 2, column = 0,
                                                             sticky = "NESW",
                                                             padx = 10, 
                                                             pady = 10)
        
        # Creates and packs save button
        self.add_ingredient_generic_text_frame_savebutt = Button(self.add_ingredient_generic_text_frame,
                                                                 text = "Save",
                                                                 command=lambda: self.save_temp_ingredient_info("generic_text",  self.add_ingredient_generic_text_frame_textbox.get()))
        self.add_ingredient_generic_text_frame_savebutt.grid(row = 2, column = 1,
                                                             sticky = "NESW",
                                                             padx = 10, 
                                                             pady = 10)
        
                                                               
        
        return self.add_ingredient_generic_text_frame
    
    
    def create_ShowCurrentInstructionsFrame(self):
        '''When the user wants to add instructions, this frame will show them all the instructions they have added so far'''
        self.show_current_instructions_frame = Frame(self.main_container)
        self.show_current_instructions_frame.grid(row = 0, column = 0,
                                                  sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.show_current_instructions_frame.columnconfigure([0,1,2], minsize=150)
        self.show_current_instructions_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.show_current_instructions_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(3): # 3 columns
            self.show_current_instructions_frame.grid_columnconfigure(j, weight=1)          
        
        # Create and pack heading widget
        self.show_current_instructions_frame_heading = Label(self.show_current_instructions_frame,
                                                             text = "Current instructions:")
        self.show_current_instructions_frame_heading.grid(row = 0, column = 0,
                                                          sticky = "NESW",
                                                          columnspan = 3,
                                                          padx = 10, pady = 10)
        
        # Create and pack add button, so that user can add a instruction
        self.show_current_instructions_frame_addbutt = Button(self.show_current_instructions_frame,
                                                              text = "Add",
                                                              command=lambda: self.show_frame("AddNewInstructionFrame"))
        self.show_current_instructions_frame_addbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack next button, which is asking for the timer input
        self.show_current_instructions_frame_nextbutt = Button(self.show_current_instructions_frame,
                                                               text = "Next",
                                                               command=lambda: self.show_frame("AskRecipeTimerFrame"))
        self.show_current_instructions_frame_nextbutt.grid(row = 2, column = 1, 
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        # Create and pack save button, to save all instructions to new_recipe_info
        self.show_current_instructions_frame_savebutt = Button(self.show_current_instructions_frame,
                                                               text = "Save",
                                                               command=lambda: self.save_information("instructions", self.new_instruction_info))
        self.show_current_instructions_frame_savebutt.grid(row = 2, column = 2,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        return self.show_current_instructions_frame
    
    def create_AddNewInstructionFrame(self):
        '''This frame allows the user to input and save a new instruction to their recipe'''
        self.add_new_instruction_frame = Frame(self.main_container)
        self.add_new_instruction_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.add_new_instruction_frame.columnconfigure([0,1], minsize=150)
        self.add_new_instruction_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.add_new_instruction_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.add_new_instruction_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading
        self.add_new_instruction_frame_heading = Label(self.add_new_instruction_frame,
                                                       text = "Enter instruction:")
        self.add_new_instruction_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack text box for inputting instruction
        self.add_new_instruction_frame_textbox = Entry(self.add_new_instruction_frame)
        self.add_new_instruction_frame_textbox.grid(row = 1, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack next button, which will return the user back to the show_current_ingredients_frame
        self.add_new_instruction_frame_nextbutt = Button(self.add_new_instruction_frame,
                                                         text = "Next",
                                                         command=lambda: self.show_frame("ShowCurrentInstructionsFrame"))
        self.add_new_instruction_frame_nextbutt.grid(row = 2, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        # Create and pack save button
        self.add_new_instruction_frame_savebutt = Button(self.add_new_instruction_frame,
                                                         text = "Save",
                                                         command=lambda: self.save_instruction_info(self.add_new_instruction_frame_textbox.get()))
        self.add_new_instruction_frame_savebutt.grid(row = 2, column = 1,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        return self.add_new_instruction_frame
        
    
    def create_AskRecipeTimerFrame(self):
        '''This will ask the user what they want to set the timer for this recipe'''
        self.ask_recipe_timer_frame = Frame(self.main_container)
        self.ask_recipe_timer_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.ask_recipe_timer_frame.columnconfigure([0,1], minsize=150)
        self.ask_recipe_timer_frame.rowconfigure([0,1,2], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(3): # 3 rows
            self.ask_recipe_timer_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.ask_recipe_timer_frame.grid_columnconfigure(j, weight=1)        
        
        # Create and pack heading when user is inputting integer for timer
        self.ask_recipe_timer_frame_heading = Label(self.ask_recipe_timer_frame,
                                                    text = "Enter the number (mins) you want to set the timer to")
        self.ask_recipe_timer_frame_heading.grid(row = 0, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2, padx = 10,
                                                 pady = 10)
        
        # Create and pack textbox for user input
        self.ask_recipe_timer_frame_textbox = Entry(self.ask_recipe_timer_frame)
        self.ask_recipe_timer_frame_textbox.grid(row = 1, column = 0,
                                                 sticky = "NESW",
                                                 columnspan = 2,
                                                 padx = 10, pady = 10)
        
        # Create and pack next button
        self.ask_recipe_timer_frame_nextbutt = Button(self.ask_recipe_timer_frame,
                                                     text = "Next",
                                                     command=lambda: self.show_frame("UploadImageFrame"))
        self.ask_recipe_timer_frame_nextbutt.grid(row = 2, column = 0,
                                                  sticky = "NESW",
                                                  padx = 10, pady = 10)
        
        # Create and pack save button
        self.ask_recipe_timer_frame_savebutt = Button(self.ask_recipe_timer_frame,
                                                      text = "Save",
                                                      command=lambda: self.save_information("timer_set_to", int(self.ask_recipe_timer_frame_textbox.get()))) # Set input as integer
        self.ask_recipe_timer_frame_savebutt.grid(row = 2, column = 1,
                                                  sticky = "NESW",
                                                  padx = 10, pady = 10)
        
        return self.ask_recipe_timer_frame
    
    def create_UploadImageFrame(self):
        '''This is the frame where the user can upload an image to add to their recipe'''
        self.upload_image_frame = Frame(self.main_container)
        self.upload_image_frame.grid(row = 0, column = 0, sticky = "NESW")
        
        # Used in conjunction with sticky to make it fill the window
        self.upload_image_frame.columnconfigure([0,1], minsize=150)
        self.upload_image_frame.rowconfigure([0,1], minsize=50)
        
        # Make each grid in the frame expandable
        for i in range(2): # 2 rows
            self.upload_image_frame.grid_rowconfigure(i, weight=1)
        
        for j in range(2): # 2 columns
            self.upload_image_frame.grid_columnconfigure(j, weight=1) 
            
        # Create and pack heading
        self.upload_image_frame_heading = Label(self.upload_image_frame, 
                                                text = "Press the upload button to add an image to your recipe.")
        self.upload_image_frame_heading.grid(row = 0, column = 0, 
                                             sticky = "NESW",
                                             columnspan = 2,
                                             padx = 10, pady = 10)
        
        # Create and pack next button
        self.upload_image_frame_nextbutt = Button(self.upload_image_frame,
                                                  text = "Next",
                                                  command=lambda: self.show_frame("SaveRecipeToJsonFrame"))
        self.upload_image_frame_nextbutt.grid(row = 1, column = 0,
                                              sticky = "NESW",
                                              padx = 10, pady = 10)
        
        # Create and pack upload button
        self.upload_image_frame_upbutt = Button(self.upload_image_frame,
                                                text = "Upload",
                                                command = self.upload_file)
        self.upload_image_frame_upbutt.grid(row = 1, column = 1,
                                            sticky = "NESW",
                                            padx = 10, pady = 10)

        return self.upload_image_frame
    
    def create_SaveRecipeToJsonFrame(self):
        '''This frame is where the user will dump the info to json'''
        self.save_recipe_to_json_frame = Frame(self.main_container)
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
                                                      text = "Press the save button to add you recipe.")
        self.save_recipe_to_json_frame_heading.grid(row = 0, column = 0,
                                                    sticky = "NESW",
                                                    columnspan = 2,
                                                    padx = 10, pady = 10)
        
        # Create and pack savebutton
        self.save_recipe_to_json_frame_savebutt = Button(self.save_recipe_to_json_frame,
                                                         text = "Save recipe",
                                                         command = self.dump_new_recipe_to_json)
        self.save_recipe_to_json_frame_savebutt.grid(row = 1, column = 0,
                                                     sticky = "NESW",
                                                     padx = 10, pady = 10)
        
        return self.save_recipe_to_json_frame    
    
    
    def create_HomeEditRecipesFrame(self):
        '''Creates homepage frame for adding recipes'''
        self.home_edit_recipes_frame = Frame(self.main_container)
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
                                                     text = "Edit recipes")
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
                                                             values = self.list_recipes_combobox_name)
        self.home_edit_recipes_frame_combobox.grid(row = 1, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack "edit!" button
        self.home_edit_recipes_frame_editbutt = Button(self.home_edit_recipes_frame,
                                                       text = "Edit!",
                                                       command = self.find_selected_recipe)
        self.home_edit_recipes_frame_editbutt.grid(row = 2, column = 0,
                                                   sticky = "NESW",
                                                   padx = 10, pady = 10)
        
        # Create and pack back button 
        self.home_edit_recipes_frame_backbutt = Button(self.home_edit_recipes_frame,
                                                               text = "Back",
                                                               command=lambda: self.show_frame("HomePageFrame"))
        self.home_edit_recipes_frame_backbutt.grid(row = 3, column = 0,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)        
        
        
        return self.home_edit_recipes_frame
    
    
    def create_HomeEditSpecificRecipeFrame(self):
        '''This serves as the main page for when the user selects a recipe they 
        want to edit'''
        self.home_edit_specific_recipe_frame = Frame(self.main_container)
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
                                                             text = "Editings details for recipe named:")
        self.home_edit_specific_recipe_frame_heading.grid(row = 0, column = 0,
                                                         sticky = "NESW",
                                                         padx = 10)
        
        # Create and pack recipe name
        self.home_edit_specific_recipe_frame_displayname = Label(self.home_edit_specific_recipe_frame,
                                                                 textvariable = self.display_recipe_name_edit_homepage)

        self.home_edit_specific_recipe_frame_displayname.grid(row = 1, column = 0,
                                                              sticky = "NESW",
                                                              padx = 10)
        
        # Create and pack delete recipe button
        self.home_edit_specific_recipe_frame_delbutt = Button(self.home_edit_specific_recipe_frame,
                                                              text = "Delete recipe",
                                                              command = self.delete_recipe)
        self.home_edit_specific_recipe_frame_delbutt.grid(row = 2, column = 0,
                                                          sticky = "NESW",
                                                          padx = 10, pady = 10)
        
        # Create and pack back button 
        self.home_edit_specific_recipe_frame_backbutt = Button(self.home_edit_specific_recipe_frame,
                                                               text = "Back",
                                                               command=lambda: self.show_frame("HomeEditRecipesFrame"))
        self.home_edit_specific_recipe_frame_backbutt.grid(row = 3, column = 0,
                                                           sticky = "NESW",
                                                           padx = 10, pady = 10)
        
        return self.home_edit_specific_recipe_frame
    
# Main program
if __name__ == "__main__":
    app = Program()
    app.run()