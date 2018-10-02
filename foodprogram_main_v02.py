
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from FoodMain import Food
from FoodListMain import FoodList
from meal_class import Meal
from meal_data import MealData
import pickle
import os


class Program:

    """ Class to act as a food planner program. """

    def __init__(self, root):

        # Load saved foods.
        self.saved_foods = self.load_saved('saved_foods.dat')

        # Create instance of Food list class to store food objects.
        self.food_list = FoodList(self.saved_foods)

        # Create instance of Food class.
        self.food = Food()

        # Create a list to store all saved MealData objects that will be used to create Meal objects.
        self.meal_data_list = self.load_saved('saved_meals.dat')

        # Create list to hold meal classes.
        self.meal_class_list = []

        # Variable to store the last focused meal from the MealTreeWindow.
        self.last_focused_meal = ''

        # Give column and row weight to the main window.
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # Create variables to be used in entry field validation.
        self.num_validate = (root.register(self.validate_num), '%S', '%P')
        self.name_validate = (root.register(self.validate_name), '%P')

        # Establish style.
        self.style = ttk.Style()
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white')
        self.style.configure('Main.TFrame', background='SystemButtonFace')
        self.style.configure('Main.TLabel', background='SystemButtonFace')

        # Create the top frame to house the main buttons.
        self.top_frame = ttk.Frame(root)
        self.top_frame.grid(column=0, row=0, sticky=(W, E), columnspan=2)
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.columnconfigure(2, weight=1)

        # Establish top frame buttons.
        self.home_button = ttk.Button(self.top_frame, text='Home')
        self.meal_button = ttk.Button(self.top_frame, text='Meal Planner')
        self.weight_button = ttk.Button(self.top_frame, text='Weight Tracker')

        # Place top frame widgets.
        self.home_button.grid(column=0, row=0, pady=30, sticky='e')
        self.meal_button.grid(column=1, row=0, padx=20, pady=30)
        self.weight_button.grid(column=2, row=0, pady=30, sticky='w')

        # Open main window.
        self.MainPlannerWindow()

        # Center screen.
        self.center_window(root)

        # Allow program to run continuously.
        root.mainloop()

#################### FUNCTIONS ####################

    def center_window(self, window):
        """ Center window. """

        root.update_idletasks()
        window.geometry(f"{window.winfo_height()}x{window.winfo_width()}")
        window.withdraw()
        window.update_idletasks()
        width = window.winfo_width()
        height = window.winfo_height()
        x = (window.winfo_screenwidth() // 2) - (width // 2)
        y = (window.winfo_screenheight() // 2) - (height // 2)
        window.geometry(f'{width}x{height}+{x}+{y}')
        window.deiconify()

        # This is for testing purposes.
        print('widget height:', window.winfo_height())
        print('widget width:', window.winfo_width())

    def empty_field_check(self, *kwargs):
        """ Check to see if an entry field is empty. Disable 'Add' button if so. """

        if (self.food_name.get() and self.calories.get() and self.protein.get() and self.carbs.get() and self.fats.get()) != '':
            self.create_food_add_button.state(['!disabled'])
        else:
            self.create_food_add_button.state(['disabled'])

    def validate_num(self, S, P):
        """ Validation check to see if entry is a number. """

        return S.isdigit() and len(P) <= 4

    def validate_name(self, P):
        """ Validation check to see if entry is too long. """

        return len(P) <= 35

    def sortby(self, treeview, sortmethod, *kwargs):
        """ Sort a list by determining which Treeview widget is being altered. """

        # Delete all items in tree.
        for child in treeview.get_children(''):
            treeview.delete(child)

        # Sort list and then re-populate tree.
        if sortmethod == 'name':
            self.food_list.sort_name()
        elif sortmethod == 'calories':
            self.food_list.sort_calories()
        elif sortmethod == 'protein':
            self.food_list.sort_protein()
        elif sortmethod == 'carbs':
            self.food_list.sort_carbs()
        elif sortmethod == 'fats':
            self.food_list.sort_fats()

        if treeview == self.food_tree:
            self.activate_buttons()

        self.populate_tree(treeview)

    def confirm_delete_food(self, *kwargs):
        """ Ask for confirmation before deleting food from food_tree. """

        index = self.get_tree_index(self.food_tree)
        selected_food = self.food_list.saved_foods[index].name
        answer = messagebox.askyesno(message=f"Are you sure you want to delete '{selected_food}' from your saved foods?", icon='question', title='Confirm')

        if answer:
            self.delete_food()
        else:
            pass

    def confirm_delete_meal(self, *kwargs):
        """ Ask for confirmation before deleting meal from custom meal_tree. """

        selected_meal = self.last_focused_meal
        answer = messagebox.askyesno(message=f"Are you sure you want to delete '{selected_meal}' from your saved meals?", icon='question', title='Confirm')

        if answer:
            self.delete_meal_frame()
        else:
            pass

    def activate_buttons(self, *kwargs):
        """ Activates 'Edit' and 'Delete' buttons when item in list is clicked. """

        if self.food_tree.focus() == '':
            self.edit_button.state(['disabled'])
            self.del_button.state(['disabled'])
        else:
            self.edit_button.state(['!disabled'])
            self.del_button.state(['!disabled'])

    def delete_food(self, *kwargs):
        """ Finds food in foodlist and deletes item. """

        # Find food list index of the selected food item.
        index = self.get_tree_index(self.food_tree)

        if self.food_tree.focus() == '':
            pass
        else:
            self.food_list.saved_foods.remove(self.food_list.saved_foods[index])
            self.food_tree.delete(self.food_tree.selection()[0])
            self.save_to_file('saved_foods.dat', self.food_list.saved_foods)

    def load_saved(self, filename):
        """ Loads pickled file containing a list. If file does not exist then create an empty list. """

        filepath = filename
        empty = []
        if not os.path.isfile(filepath):
            return empty
        else:
            with open(filepath, 'rb') as file:
                return pickle.load(file)

    def save_to_file(self, filepath, dumped_file):
        """ Save list to file that can be opened and the data can be retrieved from when file is open. Specify file as argument. """

        filename = filepath
        with open(filename, 'wb') as file:
            pickle.dump(dumped_file, file)

    def get_tree_index(self, treeview):
        """ Get the selected items index from a Treeview widget. """

        return treeview.index(treeview.selection()[0])

    def onFrameConfigure(self, *kwargs):
        """ Used for the canvas scrollbar widget. """

        self.meal_canvas.configure(scrollregion=self.meal_canvas.bbox("all"))
        self.meal_canvas.yview_moveto(0)

    def populate_tree(self, treeview):
        """ Transfer items from a list into a tkk.Treeview """

        for food in self.food_list.saved_foods:
            treeview.insert('', 'end', values=(f'{food.name}', f'{food.calories}', f'{food.protein}', f'{food.carbs}', f'{food.fats}'))

    def add_food_to_tree(self):
        """ Add newly created food to bottom of food tree. """

        index = len(self.food_list.saved_foods)
        foods = self.food_list.saved_foods
        self.food_tree.insert('', 'end', values=(f'{foods[index-1].name}', f'{foods[index-1].calories}', f'{foods[index-1].protein}', f'{foods[index-1].carbs}', f'{foods[index-1].fats}'))

        # Check current sort method and sort new addition.
        if self.food_list.current_sort == 'name':
            self.name_sort()
        elif self.food_list.current_sort == 'calories':
            self.calories_sort()
        elif self.food_list.current_sort == 'protein':
            self.protein_sort()
        elif self.food_list.current_sort == 'carbs':
            self.carbs_sort()
        elif self.food_list.current_sort == 'fats':
            self.fats_sort()
        else:
            pass

    def create_food(self):
        """
        Assigns attributes to Food class from user input in entry fields
        and saves to saved_foods in FoodList class.
        """

        # Assign food attributes from entry field inputs in CreateFoodPopUp.
        self.food.name = self.food_name.get()
        self.food.calories = self.calories.get()
        self.food.protein = self.protein.get()
        self.food.carbs = self.carbs.get()
        self.food.fats = self.fats.get()

        # Save Food object to FoodList class' saved_foods list.
        self.food_list.saved_foods.append(self.food)

        # Save food to file.
        self.save_to_file('saved_foods.dat', self.food_list.saved_foods)

        # Add food to food_tree.
        self.add_food_to_tree()
        self.add_food_window.destroy()

    def edit_food(self):
        """
        Assigns attributes to food class from user input in entry fields
        and saves to saved foods in FoodList class. Deletes old version of food object.
        """

        # Remove old food object from the FoodList class and the Treeview.
        index = self.edit_index
        self.food_list.saved_foods.remove(self.food_list.saved_foods[index])
        self.food_tree.delete(self.food_tree.selection()[0])

        # Save updated file.
        self.save_to_file('saved_foods.dat', self.food_list.saved_foods)

        # Assign food attributes from entry field inputs in CreateFoodPopUp.
        self.food.name = self.food_name.get()
        self.food.calories = self.calories.get()
        self.food.protein = self.protein.get()
        self.food.carbs = self.carbs.get()
        self.food.fats = self.fats.get()

        # Save Food object to FoodList classes saved_foods list.
        self.food_list.saved_foods.append(self.food)

        # Save food to file.
        self.save_to_file('saved_foods.dat', self.food_list.saved_foods)

        # Add food to food_tree.
        self.add_food_to_tree()
        self.edit_food_window.destroy()

    def focus_check(self, *kwargs):
        """ Check to see if meal frame has been clicked. """

        # Variable that will be 'True' if a Meal has focus in meal_class_list.
        focus_check = ''

        # Variable to store Meal object that has focus.
        focused_meal = []  # MAY GET RID OF. SEEMS TO HAVE NO USE.

        # Variable that stores string of meal that has focus of time focus_get() being called.
        self.last_focused_meal = ''

        # Iterate through all Meal objects to see if any have been selected.
        for meal in self.meal_class_list:

            if meal.current_focus:
                focus_check = 'True'
                focused_meal.append(meal)  # MAY GET RID OF. SEEMS TO HAVE NO USE.
                self.last_focused_meal = root.focus_get()  # MAY GET RID OF THIS AS WELL. SEEMS TO HAVE NO USE.
                focused = str(self.last_focused_meal)

                # Check last character of focused. This will return the meal frame number or 'e' if first frame.
                if focused[-1:] == 'e':
                    index = 0

                    # Assign variable the selected Meal objects meal name from the object in meal_class_list.
                    self.last_focused_meal = self.meal_class_list[index].meal_name
                else:
                    index = int(focused[-1:]) - 1

                    # Assign variable the selected Meal objects meal name from the object in meal_class_list.
                    self.last_focused_meal = self.meal_class_list[index].meal_name

        if focus_check == 'True':
            self.meal_edit_button.state(['!disabled'])
            self.meal_del_button.state(['!disabled'])
        else:
            self.meal_edit_button.state(['disabled'])
            self.meal_del_button.state(['disabled'])

    def delete_meal_frame(self, *kwargs):
        """ Delete a meal frame from MealTreeWindow. """

        index = 0

        for meal in self.meal_data_list:

            # Find focused meal in meal_data_list.
            if self.last_focused_meal == meal.meal_name:

                # Delete Meal from both meal containers.
                self.meal_data_list.remove(self.meal_data_list[index])
                self.meal_class_list.remove(self.meal_class_list[index])

            # Increase index if object was not found in iteration.
            index += 1

        self.save_to_file('saved_meals.dat', self.meal_data_list)

        # Destroy frames and call MealTreeWindow to update with current data. (See if a smoother way is possible.)
        self.main_meal_frame.destroy()
        self.MealTreeWindow()

    def add_to_meal_tree(self, *kwargs):
        """ Add food item from food_tree Treeview to meal_tree Treeview. """

        if self.food_tree_createmeal.focus() == '':
            pass

        else:
            index = self.get_tree_index(self.food_tree_createmeal)
            self.meal_tree.insert('', 'end', values=(f'{self.food_list.saved_foods[index].name}',))
            self.meallist_foods.append(self.food_list.saved_foods[index])

            calorie_total = 0
            protein_total = 0
            carbs_total = 0
            fats_total = 0

            for food in self.meallist_foods:
                calorie_total += int(food.calories)
                protein_total += int(food.protein)
                carbs_total += int(food.carbs)
                fats_total += int(food.fats)

            self.meal_cal_num['text'] = str(calorie_total)
            self.meal_pro_num['text'] = str(protein_total)
            self.meal_carb_num['text'] = str(carbs_total)
            self.meal_fat_num['text'] = str(fats_total)

            # CONSIDER CHANGING THE FOR FOOD IN MEALLIST TO A FOODLIST CLASS OBJECT AND ADD
            # A GETCALORIES, GETPROTEIN METHOD. SO IT WOULD BE:
            # meallist_foods = FoodList([])
            # meallist_foods.saved_foods.append(foods[index])
            # self.meal_cal_num['text'] = meallist_foods.getcalories()

    def insert_data_in_edit_meal_fields(self, *kwargs):
        """ Fills entry widgets with the data of the Meal to be edited. """

        meal_index = 0
        self.saved_index = 0
        meal_name = self.last_focused_meal

        # Create variables to store totals which will be assigned to labels.
        calorie_total = 0
        protein_total = 0
        carbs_total = 0
        fats_total = 0

        # Iterate through meals to find the selected meal. Each iteration increases meal_index.
        for meal in self.meal_data_list:

            if self.last_focused_meal == meal.meal_name:
                self.saved_index = meal_index

                # Iterate through Food objects saved to the Meal class in the list of Meal classes.
                for food in self.meal_class_list[self.saved_index].meal_list:

                    # Populate meal_tree Treeview with the Food objects of selected Meal to be edited.
                    self.meal_tree.insert('', 'end', values=(f'{food.name}',))
                    self.meallist_foods.append(food)

                    # Add totals of Food attributes to store in totals labels.
                    calorie_total += int(food.calories)
                    protein_total += int(food.protein)
                    carbs_total += int(food.carbs)
                    fats_total += int(food.fats)

            # Increment meal_index if the last_focused and meal do not match.
            meal_index += 1

        # Assign the Food attribute totals to the corresponding labels.
        self.meal_cal_num['text'] = str(calorie_total)
        self.meal_pro_num['text'] = str(protein_total)
        self.meal_carb_num['text'] = str(carbs_total)
        self.meal_fat_num['text'] = str(fats_total)

    def del_meal_from_tree(self, *kwargs):
        """ Delete meal from meal_tree Treeview widget. """

        if self.meal_tree.focus() == '':
            pass
        else:
            index = self.get_tree_index(self.meal_tree)
            self.meallist_foods.remove(self.meallist_foods[index])
            self.meal_tree.delete(self.meal_tree.selection()[0])

    def add_meal_to_meal_frame(self):

        # Get meal_name and meal_foods(list of food objects) from add_meal method.
        meal_name = self.meal_name.get()
        meal_foods = self.meallist_foods

        # Create an instance of Meal class using the collected data from the add_meal method.
        meal = Meal(meal_foods, self.main_meal_frame, meal_name)
        meal.show_meal()

        # Create an instance of MealData class to store Meal class data. (Meal class can't be pickled due containing Tkinter objects. So it must be re-created using MealData assigned to Meal class.)
        meal_data = MealData(meal_foods, meal_name)

        # Save meal_data to meal_data_list to store data and create meal classes from.
        self.meal_data_list.append(meal_data)
        self.meal_class_list.append(meal)
        self.save_to_file('saved_meals.dat', self.meal_data_list)
        self.add_meal_window.destroy()

        # NEED TO MAKE SURE NEW MEAL IS IN SELF.MEAL_CLASS_LIST

    def add_edited_meal_to_meal_frame(self):

        self.meal_data_list.remove(self.meal_data_list[self.saved_index])
        self.meal_class_list.remove(self.meal_class_list[self.saved_index])

        meal_name = self.meal_name.get()
        meal_foods = self.meallist_foods
        meal = Meal(meal_foods, self.main_meal_frame, meal_name)
        meal.show_meal()
        meal_data = MealData(meal_foods, meal_name)
        self.meal_data_list.insert(self.saved_index, meal_data)
        self.save_to_file('saved_meals.dat', self.meal_data_list)
        self.add_meal_window.destroy()
        self.outside_meal_frame.destroy()
        self.main_meal_frame.destroy()
        self.MealTreeWindow()

        #################### FRAMES AND WINDOWS  ####################

    def MainPlannerWindow(self):
        """ Create frame for the main planner window. """

        # Create home frame.
        self.main_outside_frame = ttk.Frame(root, style='Main.TFrame')
        self.main_outside_frame.grid(column=0, row=1)

        # Create frame to house FoodTreeWindow.
        self.foodtree_window_frame = ttk.Frame(self.main_outside_frame, style='Main.TFrame')
        self.foodtree_window_frame.grid(column=0, row=0, sticky=N)
        self.FoodTreeWindow()

        # Create frame to house MealTreeWindow.
        self.mealtree_window_frame = ttk.Frame(self.main_outside_frame, style='Main.TFrame', borderwidth=1, relief='solid')
        self.mealtree_window_frame.grid(column=1, row=0, pady='10 0')
        self.mealtree_window_bottomframe = ttk.Frame(self.main_outside_frame, style='Main.TFrame')
        self.mealtree_window_bottomframe.grid(column=1, row=1)
        self.MealTreeWindow()

    def FoodTreeWindow(self):
        """ Frames containing the food list. """

        # Create main frame.
        self.main_frame = ttk.Frame(self.foodtree_window_frame, style='Main.TFrame')
        self.main_frame.grid(column=0, row=1)

        # Establish main frame widgets.
        self.food_tree = ttk.Treeview(self.main_frame, selectmode='browse', show='headings')
        self.food_tree['columns'] = ('name', 'calories', 'protein', 'carbs', 'fat')
        self.food_tree.grid(column=0, row=0, padx='10 0', pady='10 20')

        # Create scrollbar widget for food_tree.
        self.food_tree_scrollbar = ttk.Scrollbar(self.main_frame, orient=VERTICAL, command=self.food_tree.yview)
        self.food_tree_scrollbar.grid(column=1, row=0, sticky=NS, padx='0 10', pady='10 20')
        self.food_tree.configure(yscrollcommand=self.food_tree_scrollbar.set)

        # Create frame for buttons.
        self.food_tree_button_frame = ttk.Frame(self.foodtree_window_frame, style='Main.TFrame')
        self.food_tree_button_frame.grid(column=0, row=2)

        # Establish columns for tree widget.
        self.food_tree.column('name', width=200, anchor='w')
        self.food_tree.heading('name', text='Name', command=lambda: self.sortby(self.food_tree, 'name'))

        self.food_tree.column('calories', width=60, anchor='center')
        self.food_tree.heading('calories', text='Calories', command=lambda: self.sortby(self.food_tree, 'calories'))

        self.food_tree.column('protein', width=60, anchor='center')
        self.food_tree.heading('protein', text='Protein', command=lambda: self.sortby(self.food_tree, 'protein'))

        self.food_tree.column('carbs', width=60, anchor='center')
        self.food_tree.heading('carbs', text='Carbs', command=lambda: self.sortby(self.food_tree, 'carbs'))

        self.food_tree.column('fat', width=60, anchor='center')
        self.food_tree.heading('fat', text='Fat', command=lambda: self.sortby(self.food_tree, 'fats'))

        # Create buttons to interact with list.
        self.main_add_button = ttk.Button(self.food_tree_button_frame, text='Add', command=self.CreateFoodPopUp)
        self.main_add_button.grid(column=0, row=1, pady='0 20', sticky='e')

        self.edit_button = ttk.Button(self.food_tree_button_frame, text='Edit', state='disabled', command=self.EditFoodPopUp)
        self.edit_button.grid(column=1, row=1, pady='0 20')

        self.del_button = ttk.Button(self.food_tree_button_frame, text='Delete', state='disabled', command=self.confirm_delete_food)
        self.del_button.grid(column=2, row=1, pady='0 20', sticky='w')

        # Bind action to when item is selected in food_tree to activate the 'Edit' and 'Delete' buttons.
        self.food_tree.bind('<<TreeviewSelect>>', self.activate_buttons)

        # Call function to add food to tree.
        self.populate_tree(self.food_tree)

    def CreateFoodPopUp(self):
        """ Creates window with widgets to input food attributes. """

        # Re-create fresh food object to prevent carrying over of attributes.
        self.food = Food()

        # Create new window.
        self.add_food_window = Toplevel(root)

        # Create main from for widgets.
        self.create_food_main_frame = ttk.Frame(self.add_food_window, style='Main.TFrame')
        self.create_food_main_frame.grid(column=0, row=0)

        # Create bottom frame.
        self.bottom_frame = ttk.Frame(self.add_food_window, style='Main.TFrame')
        self.bottom_frame.grid(column=0, row=1)

        # Create variables for food class.
        self.food_name = StringVar()
        self.calories = StringVar()
        self.protein = StringVar()
        self.carbs = StringVar()
        self.fats = StringVar()

        # Create label widgets.
        self.title_label = ttk.Label(self.create_food_main_frame, text='Add Food', font='bold', style='Main.TLabel')
        self.name_label = ttk.Label(self.create_food_main_frame, text='Food Name', style='Main.TLabel')
        self.calories_label = ttk.Label(self.create_food_main_frame, text='Calories', style='Main.TLabel')
        self.protein_label = ttk.Label(self.create_food_main_frame, text='Protein', style='Main.TLabel')
        self.carbs_label = ttk.Label(self.create_food_main_frame, text='Carbs', style='Main.TLabel')
        self.fats_label = ttk.Label(self.create_food_main_frame, text='Fats', style='Main.TLabel')

        # Create entry widgets.
        self.name_entry = ttk.Entry(self.create_food_main_frame, textvariable=self.food_name, validate='key', validatecommand=self.name_validate)
        self.food_name.trace_add('write', self.empty_field_check)
        self.calories_entry = ttk.Entry(self.create_food_main_frame, textvariable=self.calories, validate='key', validatecommand=self.num_validate)
        self.calories.trace_add('write', self.empty_field_check)
        self.protein_entry = ttk.Entry(self.create_food_main_frame, textvariable=self.protein, validate='key', validatecommand=self.num_validate)
        self.protein.trace_add('write', self.empty_field_check)
        self.carbs_entry = ttk.Entry(self.create_food_main_frame, textvariable=self.carbs, validate='key', validatecommand=self.num_validate)
        self.carbs.trace_add('write', self.empty_field_check)
        self.fats_entry = ttk.Entry(self.create_food_main_frame, textvariable=self.fats, validate='key', validatecommand=self.num_validate)
        self.fats.trace_add('write', self.empty_field_check)

        # Create button widgets.
        self.create_food_add_button = ttk.Button(self.bottom_frame, text='Add', state='disabled', command=self.create_food)
        self.cancel_button = ttk.Button(self.bottom_frame, text='Cancel', command=self.add_food_window.destroy)

        # Create separator widget.
        # self.sep = ttk.Separator(self.create_food_main_frame, orient=HORIZONTAL)

        # Grid widgets.
        self.title_label.grid(column=0, row=0, columnspan=2, pady=5)
        # self.sep.grid(column=0, row=1, columnspan=2)
        self.name_label.grid(column=0, row=2, padx='10 0', sticky='e')
        self.name_entry.grid(column=1, row=2, padx=10, pady=2)
        self.calories_label.grid(column=0, row=3, sticky='e')
        self.calories_entry.grid(column=1, row=3, padx=10, pady=2)
        self.protein_label.grid(column=0, row=4, sticky='e')
        self.protein_entry.grid(column=1, row=4, padx=10, pady=2)
        self.carbs_label.grid(column=0, row=5, sticky='e')
        self.carbs_entry.grid(column=1, row=5, padx=10, pady=2)
        self.fats_label.grid(column=0, row=6, sticky='e')
        self.fats_entry.grid(column=1, row=6, padx=10, pady=2)
        self.create_food_add_button.grid(column=0, row=7, pady='15 5', padx='0 15')
        self.cancel_button.grid(column=1, row=7, pady='15 5')

        self.center_window(self.add_food_window)

    def EditFoodPopUp(self):
        """ Creates window with widgets to input food attributes. """

        # Get food from food list to edit.
        self.edit_index = self.get_tree_index(self.food_tree)

        # Re-create fresh food object to prevent carrying over of attributes.
        self.food = Food()

        # Create new window.
        self.edit_food_window = Toplevel(root)

        # Create main from for widgets.
        self.edit_food_main_frame = ttk.Frame(self.edit_food_window, style='Main.TFrame')
        self.edit_food_main_frame.grid(column=0, row=0)

        # Create bottom frame.
        self.bottom_frame = ttk.Frame(self.edit_food_window, style='Main.TFrame')
        self.bottom_frame.grid(column=0, row=1)

        # Create variables for food class with the default values being the foods current values.
        self.food_name = StringVar(value=f'{self.food_list.saved_foods[self.edit_index].name}')
        self.calories = StringVar(value=f'{self.food_list.saved_foods[self.edit_index].calories}')
        self.protein = StringVar(value=f'{self.food_list.saved_foods[self.edit_index].protein}')
        self.carbs = StringVar(value=f'{self.food_list.saved_foods[self.edit_index].carbs}')
        self.fats = StringVar(value=f'{self.food_list.saved_foods[self.edit_index].fats}')

        # Create label widgets.
        self.title_label = ttk.Label(self.edit_food_main_frame, text='Add Food', font='bold')
        self.name_label = ttk.Label(self.edit_food_main_frame, text='Food Name')
        self.calories_label = ttk.Label(self.edit_food_main_frame, text='Calories')
        self.protein_label = ttk.Label(self.edit_food_main_frame, text='Protein')
        self.carbs_label = ttk.Label(self.edit_food_main_frame, text='Carbs')
        self.fats_label = ttk.Label(self.edit_food_main_frame, text='Fats')

        # Create entry widgets and check if fields are blank.
        self.name_entry = ttk.Entry(self.edit_food_main_frame, textvariable=self.food_name, validate='key', validatecommand=self.name_validate)
        self.food_name.trace_add('write', self.empty_field_check)
        self.calories_entry = ttk.Entry(self.edit_food_main_frame, textvariable=self.calories, validate='key', validatecommand=self.num_validate)
        self.calories.trace_add('write', self.empty_field_check)
        self.protein_entry = ttk.Entry(self.edit_food_main_frame, textvariable=self.protein, validate='key', validatecommand=self.num_validate)
        self.protein.trace_add('write', self.empty_field_check)
        self.carbs_entry = ttk.Entry(self.edit_food_main_frame, textvariable=self.carbs, validate='key', validatecommand=self.num_validate)
        self.carbs.trace_add('write', self.empty_field_check)
        self.fats_entry = ttk.Entry(self.edit_food_main_frame, textvariable=self.fats, validate='key', validatecommand=self.num_validate)
        self.fats.trace_add('write', self.empty_field_check)

        # Create button widgets.
        self.create_food_add_button = ttk.Button(self.bottom_frame, text='Add', state='disabled', command=self.edit_food)
        self.cancel_button = ttk.Button(self.bottom_frame, text='Cancel', command=self.edit_food_window.destroy)

        # Create separator widget.
        # self.sep = ttk.Separator(self.edit_food_main_frame, orient=HORIZONTAL)

        # Grid widgets.
        self.title_label.grid(column=0, row=0, columnspan=2, pady=5)
        # self.sep.grid(column=0, row=1, columnspan=2)
        self.name_label.grid(column=0, row=2, padx='10 0', sticky='e')
        self.name_entry.grid(column=1, row=2, padx=10, pady=2)
        self.calories_label.grid(column=0, row=3, sticky='e')
        self.calories_entry.grid(column=1, row=3, padx=10, pady=2)
        self.protein_label.grid(column=0, row=4, sticky='e')
        self.protein_entry.grid(column=1, row=4, padx=10, pady=2)
        self.carbs_label.grid(column=0, row=5, sticky='e')
        self.carbs_entry.grid(column=1, row=5, padx=10, pady=2)
        self.fats_label.grid(column=0, row=6, sticky='e')
        self.fats_entry.grid(column=1, row=6, padx=10, pady=2)
        self.create_food_add_button.grid(column=0, row=7, pady='15 5', padx='0 15')
        self.cancel_button.grid(column=1, row=7, pady='15 5')

        self.center_window(self.edit_food_window)

    def MealTreeWindow(self):
        """ Create the window that contains the custom made Meal Tree. """

        self.meal_canvas = Canvas(self.mealtree_window_frame, borderwidth=0, width='371', height='650', highlightthickness=0)
        self.main_meal_frame = ttk.Frame(self.meal_canvas)
        self.meal_scrollbar = Scrollbar(root, orient=VERTICAL, command=self.meal_canvas.yview)
        self.meal_canvas.configure(yscrollcommand=self.meal_scrollbar.set)

        self.meal_scrollbar.grid(column=1, row=1, sticky=NS, pady='10 50')
        self.meal_canvas.grid(column=0, row=1)
        self.meal_canvas.create_window((4, 4), window=self.main_meal_frame, tags='self.main_meal_frame')

        self.main_meal_frame.bind("<Configure>", self.onFrameConfigure)

        self.meal_bottom_frame = ttk.Frame(self.mealtree_window_bottomframe, style='Main.TFrame')
        self.meal_bottom_frame.grid(column=0, row=2)

        self.meal_add_button = ttk.Button(self.meal_bottom_frame, text='Add', command=self.CreateMealPopUp)
        self.meal_add_button.grid(column=0, row=1, pady='10 20', sticky='e')

        self.meal_edit_button = ttk.Button(self.meal_bottom_frame, text='Edit', state='disabled', command=self.EditMealPopUp)
        self.meal_edit_button.grid(column=1, row=1, pady='10 20', padx=30)

        self.meal_del_button = ttk.Button(self.meal_bottom_frame, text='Delete', state='disabled', command=self.confirm_delete_meal)
        self.meal_del_button.grid(column=2, row=1, pady='10 20', sticky='w')

        # Check if there is anything currently in meaL_class_list. If so delete it so it does not get duplicated when MealTreeWindow is called.
        if len(self.meal_class_list) > 1:
            self.meal_class_list = []

        # Load saved meals and display in screen.
        for meal in self.meal_data_list:
            loaded_meal = Meal(meal.meal_list, self.main_meal_frame, meal.meal_name)
            self.meal_class_list.append(loaded_meal)
            loaded_meal.show_meal()

        # Check if a meal item is selected.
        root.bind('<ButtonRelease-1>', self.focus_check)

    def CreateMealPopUp(self):
        """ A window that offers users an interface to create a meal consisting of Food objects. """

        # Create main window to house all widgets and frames.
        self.add_meal_window = Toplevel(root)

        # Create variable to hold food objects added to meal tree window.
        self.meallist_foods = []

        # Create heading for window.
        self.meal_heading = ttk.Label(self.add_meal_window, text='Meal Creation', style='Main.TLabel')
        self.meal_heading.grid(column=0, row=0, columnspan=2)

        # Create frame to house the food tree and meal frame.
        self.meal_creation_frame = ttk.Frame(self.add_meal_window, borderwidth=5, relief='solid')
        self.meal_creation_frame.grid(column=0, row=1, padx=10, pady=10, columnspan=2)

        ####################### Saved_foods_frame. #######################
        # Create frame to house the foodtree.
        self.saved_foods_frame = ttk.Frame(self.meal_creation_frame)
        self.saved_foods_frame.grid(column=0, row=0)

        # Create treeview heading.
        self.saved_foods_label = ttk.Label(self.saved_foods_frame, text='Saved Foods')
        self.saved_foods_label.grid(column=0, row=0, pady='0 2')

        # Establish main frame widgets.
        self.food_tree_createmeal = ttk.Treeview(self.saved_foods_frame, selectmode='browse', show='headings')
        self.food_tree_createmeal['columns'] = ('name', 'calories', 'protein', 'carbs', 'fat')
        self.food_tree_createmeal.grid(column=0, row=1, padx='10', pady='10')

        # Establish columns for tree widget.
        self.food_tree_createmeal.column('name', width=200, anchor='w')
        self.food_tree_createmeal.heading('name', text='Name', command=lambda: self.sortby(self.food_tree_createmeal, 'name'))

        self.food_tree_createmeal.column('calories', width=60, anchor='center')
        self.food_tree_createmeal.heading('calories', text='Calories', command=lambda: self.sortby(self.food_tree_createmeal, 'calories'))

        self.food_tree_createmeal.column('protein', width=60, anchor='center')
        self.food_tree_createmeal.heading('protein', text='Protein', command=lambda: self.sortby(self.food_tree_createmeal, 'protein'))

        self.food_tree_createmeal.column('carbs', width=60, anchor='center')
        self.food_tree_createmeal.heading('carbs', text='Carbs', command=lambda: self.sortby(self.food_tree_createmeal, 'carbs'))

        self.food_tree_createmeal.column('fat', width=60, anchor='center')
        self.food_tree_createmeal.heading('fat', text='Fat', command=lambda: self.sortby(self.food_tree_createmeal, 'fats'))

        # Create button for foodtree.
        self.add_meal_button = ttk.Button(self.saved_foods_frame, text='Add', command=self.add_to_meal_tree)
        self.add_meal_button.grid(column=0, row=2)

        # Create vertical separator.
        self.meal_separator = ttk.Separator(self.meal_creation_frame, orient=VERTICAL)
        self.meal_separator.grid(column=1, row=0, sticky='ns')

        ####################### Meal_info_frame. #######################
        # Create frame to house meal info.
        self.meal_info_frame = ttk.Frame(self.meal_creation_frame)
        self.meal_info_frame.grid(column=2, row=0)

        self.meal_name_label = ttk.Label(self.meal_info_frame, text='Meal Name')
        self.meal_name_label.grid(column=0, row=0)

        self.meal_name = StringVar()
        self.meal_name_entry = ttk.Entry(self.meal_info_frame, textvariable=self.meal_name)
        self.meal_name_entry.grid(column=1, row=0)

        # Create treeview for meals.
        self.meal_tree = ttk.Treeview(self.meal_info_frame, height=10, selectmode='browse', show='headings')
        self.meal_tree.grid(column=0, row=1, padx='10', pady='10', columnspan=2)
        self.meal_tree['columns'] = ('name')
        self.meal_tree.column('name', anchor='w')
        self.meal_tree.heading('name', text='Name')

        # Create a frame to hold the meal nutritional info.
        self.meal_att_frame = ttk.Frame(self.meal_info_frame)
        self.meal_att_frame.grid(column=2, row=1, sticky='n', pady='7 0')
        self.meal_cal_label = ttk.Label(self.meal_att_frame, text='Calories:')
        self.meal_pro_label = ttk.Label(self.meal_att_frame, text='Protein:')
        self.meal_carb_label = ttk.Label(self.meal_att_frame, text='Carbs:')
        self.meal_fat_label = ttk.Label(self.meal_att_frame, text='Fats:')
        self.meal_cal_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_pro_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_carb_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_fat_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_cal_label.grid(column=0, row=0, sticky='w', padx='0 10')
        self.meal_pro_label.grid(column=0, row=1, sticky='w')
        self.meal_carb_label.grid(column=0, row=2, sticky='w')
        self.meal_fat_label.grid(column=0, row=3, sticky='w')
        self.meal_cal_num.grid(column=1, row=0, sticky='w', padx='0 10')
        self.meal_pro_num.grid(column=1, row=1, sticky='w')
        self.meal_carb_num.grid(column=1, row=2, sticky='w')
        self.meal_fat_num.grid(column=1, row=3, sticky='w')

        # Create button for meal treeview.
        self.meal_delete_button = ttk.Button(self.meal_info_frame, text='Delete', command=self.del_meal_from_tree)
        self.meal_delete_button.grid(column=0, row=2, columnspan=2)

        # Create buttons for main window.
        self.save_meal_button = ttk.Button(self.add_meal_window, text='Save', command=self.add_meal_to_meal_frame)
        self.save_meal_button.grid(column=0, row=2, sticky='e', pady='0 10', padx='0 10')

        self.cancel_meal_button = ttk.Button(self.add_meal_window, text='Cancel', command=self.add_meal_window.destroy)
        self.cancel_meal_button.grid(column=1, row=2, sticky='w', pady='0 10', padx='10 0')

        # Call function to add food to tree.
        self.populate_tree(self.food_tree_createmeal)

        # Center window.
        self.center_window(self.add_meal_window)

    def EditMealPopUp(self):

        # Create main window to house all widgets and frames.
        self.add_meal_window = Toplevel(root)

        # Create variable to hold food objects added to meal tree window.
        self.meallist_foods = []

        # Create heading for window.
        self.meal_heading = ttk.Label(self.add_meal_window, text='Meal Creation', style='Main.TLabel')
        self.meal_heading.grid(column=0, row=0, columnspan=2)

        # Create frame to house the food tree and meal frame.
        self.meal_creation_frame = ttk.Frame(self.add_meal_window, borderwidth=5, relief='solid')
        self.meal_creation_frame.grid(column=0, row=1, padx=10, pady=10, columnspan=2)

        ####################### Saved_foods_frame. #######################
        # Create frame to house the foodtree.
        self.saved_foods_frame = ttk.Frame(self.meal_creation_frame)
        self.saved_foods_frame.grid(column=0, row=0)

        # Create treeview heading.
        self.saved_foods_label = ttk.Label(self.saved_foods_frame, text='Saved Foods')
        self.saved_foods_label.grid(column=0, row=0, pady='0 2')

        # Establish main frame widgets.
        self.food_tree_createmeal = ttk.Treeview(self.saved_foods_frame, selectmode='browse', show='headings')
        self.food_tree_createmeal['columns'] = ('name', 'calories', 'protein', 'carbs', 'fat')
        self.food_tree_createmeal.grid(column=0, row=1, padx='10', pady='10')

        # Establish columns for tree widget.
        self.food_tree_createmeal.column('name', width=200, anchor='w')
        self.food_tree_createmeal.heading('name', text='Name', command=lambda: self.sortby(self.food_tree_createmeal, 'name'))

        self.food_tree_createmeal.column('calories', width=60, anchor='center')
        self.food_tree_createmeal.heading('calories', text='Calories', command=lambda: self.sortby(self.food_tree_createmeal, 'calories'))

        self.food_tree_createmeal.column('protein', width=60, anchor='center')
        self.food_tree_createmeal.heading('protein', text='Protein', command=lambda: self.sortby(self.food_tree_createmeal, 'protein'))

        self.food_tree_createmeal.column('carbs', width=60, anchor='center')
        self.food_tree_createmeal.heading('carbs', text='Carbs', command=lambda: self.sortby(self.food_tree_createmeal, 'carbs'))

        self.food_tree_createmeal.column('fat', width=60, anchor='center')
        self.food_tree_createmeal.heading('fat', text='Fat', command=lambda: self.sortby(self.food_tree_createmeal, 'fats'))

        # Create button for foodtree.
        self.add_meal_button = ttk.Button(self.saved_foods_frame, text='Add', command=self.add_to_meal_tree)
        self.add_meal_button.grid(column=0, row=2)

        # Create vertical separator.
        self.meal_separator = ttk.Separator(self.meal_creation_frame, orient=VERTICAL)
        self.meal_separator.grid(column=1, row=0, sticky='ns')

        ####################### Meal_info_frame. #######################
        # Create frame to house meal info.
        self.meal_info_frame = ttk.Frame(self.meal_creation_frame)
        self.meal_info_frame.grid(column=2, row=0)

        self.meal_name_label = ttk.Label(self.meal_info_frame, text='Meal Name')
        self.meal_name_label.grid(column=0, row=0)

        self.meal_name = StringVar(value=f'{self.last_focused_meal}')
        self.meal_name_entry = ttk.Entry(self.meal_info_frame, textvariable=self.meal_name)
        self.meal_name_entry.grid(column=1, row=0)

        # Create treeview for meals.
        self.meal_tree = ttk.Treeview(self.meal_info_frame, height=10, selectmode='browse', show='headings')
        self.meal_tree.grid(column=0, row=1, padx='10', pady='10', columnspan=2)
        self.meal_tree['columns'] = ('name')
        self.meal_tree.column('name', anchor='w')
        self.meal_tree.heading('name', text='Name')

        # Create a frame to hold the meal nutritional info.
        self.meal_att_frame = ttk.Frame(self.meal_info_frame)
        self.meal_att_frame.grid(column=2, row=1, sticky='n', pady='7 0')
        self.meal_cal_label = ttk.Label(self.meal_att_frame, text='Calories:')
        self.meal_pro_label = ttk.Label(self.meal_att_frame, text='Protein:')
        self.meal_carb_label = ttk.Label(self.meal_att_frame, text='Carbs:')
        self.meal_fat_label = ttk.Label(self.meal_att_frame, text='Fats:')
        self.meal_cal_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_pro_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_carb_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_fat_num = ttk.Label(self.meal_att_frame, text='0')
        self.meal_cal_label.grid(column=0, row=0, sticky='w', padx='0 10')
        self.meal_pro_label.grid(column=0, row=1, sticky='w')
        self.meal_carb_label.grid(column=0, row=2, sticky='w')
        self.meal_fat_label.grid(column=0, row=3, sticky='w')
        self.meal_cal_num.grid(column=1, row=0, sticky='w', padx='0 10')
        self.meal_pro_num.grid(column=1, row=1, sticky='w')
        self.meal_carb_num.grid(column=1, row=2, sticky='w')
        self.meal_fat_num.grid(column=1, row=3, sticky='w')

        # Create button for meal treeview.
        self.meal_delete_button = ttk.Button(self.meal_info_frame, text='Delete', command=self.del_meal_from_tree)
        self.meal_delete_button.grid(column=0, row=2, columnspan=2)

        # Create buttons for main window.
        self.save_meal_button = ttk.Button(self.add_meal_window, text='Save', command=self.add_edited_meal_to_meal_frame)  # WILL NEED TO CHANGE THIS SO IT DELETES CURRENT INSTANCE AND INSERTS NEW INSTANCE IN PROPER SPACE.
        self.save_meal_button.grid(column=0, row=2, sticky='e', pady='0 10', padx='0 10')

        self.cancel_meal_button = ttk.Button(self.add_meal_window, text='Cancel', command=self.add_meal_window.destroy)
        self.cancel_meal_button.grid(column=1, row=2, sticky='w', pady='0 10', padx='10 0')

        # Pre-populate fields with data to be edited.
        self.insert_data_in_edit_meal_fields()

        # Call function to add food to tree.
        self.populate_tree(self.food_tree_createmeal)

        # Center window.
        self.center_window(self.add_meal_window)


#########################


if __name__ == "__main__":
        # Run program
    root = Tk()
    root.title('Meal Planner')
    root.iconbitmap(default='transparent.ico')
    program = Program(root)


######## TO DO: ########
## TOP PRIORITY: ##
# EDITED FOODS DO NOT CHANGE SAVED FOODS IN MEALS. (MEALS WOULD NEED TO STORE THE INSTANCE OF THE FOOD OBJECTS)
# EXPAND SCREEN AS CALORIES ARE ADDED TO MEALS. (ISSUE DUE TO CENTERING SCREEN. MAY CONSIDER NOT CENTERING EVERYTHING. WILL PROB HAVE TO DO A CHECK ON CALORIES LENGTH THEN HAVE PRESET WIDTHS FOR CALORIES LENGTH)
# MAKE MEAL NAME CHARACTER LIMIT.
# MAKE SURE NAME IS NOT USED ON ANOTHER FOOD. (WHEN SAVED PRESS HAVE FUNCTION CHECK AT FIRST AND ADD LABEL NEXT TO ENTRY WITH MESSAGE.)
# MAKE SOMETHING APPEAR IN BLANK MEAL PLANNER WINDOW.
# DISABLE SAVE BUTTON UNTIL BOTH MEAL NAME AND AT LEAST ONE FOOD IN MEAL.
# WHEN FOOD IS EDITED HAVE IT RETURN TO ORIGINAL POSITION IN LIST.
# MAKE HOME SCREEN.
# MAKE A NOTEBOOK WIDGET STORING MEALFRAMES DEPENDING ON THE MEAL ATTRIBUTE(BREAKFAST, LUNCH, DINNER, SNACK, ALL).
# MAKE A DAILY FOOD PLAN.

## LOW PRIORITY: ##
# REDESIGN MEAL CLASS AND MEAL DATA CLASS. MEAL CLASS COULD MAINLY BE BROUGHT TO MAIN PROGRAM (UNLESS IT NEEDS TO BE SEPERATE TO CREATE INSTANCES THAN JUST RENAME IT TO MEAL FRAME CLASS) AND MEAL DATA COULD BE ACTUAL MEAL CLASS.
# SEE IF THERE IS A BETTER WAY THAN JUST DESTROYING AND REDRAWING FRAMES.
# TRY TO LEARN WHY VALIDATE WORKS. EX REGISTER/TRACE ADD (IS REGISTER A WAY TO ADD ARGUMENTS TO FUNCTION WITH OUT CALLING THEM WHEN BEING ASSIGNED TO BUTTON, ETC.)
# LEARN WHAT NEEDS TO BE SELF. AND WHAT DOESNT NEED TO BE. (START BY TAKING AWAY SELF FROM VARIABLES NOT REFERENCED LATER IN CLASS)
# MAKE MEAL TITLES ACTUALLY BOLD.

## FINISHING TOUCHES: ##
# CLEAN UP CODE AND COMBINE REUSED CODE INTO METHODS.
# FOCUS ON APPEARANCE OF PROGRAM.
# MAKE SOME OPTIONS SUCH AS HELP, INFO, COLOR SCHEMES.
# CONSIDER ADDING A SEARCH FOOD OPTIONS TO USE FOODS SCRAPED FROM INTERNET.
