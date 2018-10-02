from tkinter import *
from tkinter import ttk
from food import Food

# THIS COULD PROBABLY BE CHANGED. CURRENTLY MAKES A FRAME AND NOT REALLY A MEAL. MEAL DATA IS MORE OF A MEAL.


class Meal:

    """ Class designed to take in information and create a frame in tkinter that visually displays a series of food objects. """

    def __init__(self, meal_list, main_meal_frame, meal_name):
        self.meal_list = meal_list
        self.main_meal_frame = main_meal_frame
        self.meal_name = meal_name

        # DELETE
        self.style = ttk.Style()
        self.style.configure('TFrame', background='white')
        self.style.configure('TLabel', background='white')
        self.style.configure('Main.TFrame', background='SystemButtonFace')
        self.style.configure('Main.TLabel', background='SystemButtonFace')
        self.style.configure('Focus.TFrame', background='LightSteelBlue1')  # LightCyan2
        self.style.configure('Focus.TLabel', background='LightSteelBlue1')  # LightSteelBlue1

        self.current_focus = False
        # self.current_focus = BooleanVar()
        # self.current_focus.set(False)
        # self.current_focus.trace_add('write', self.testing)

    def __str__(self):
        return self.meal_name

    def show_meal(self):

        # Make frame to house widgets.
        self.meal_frame = ttk.Frame(self.main_meal_frame)

        # Make meal title label.
        self.meal_title = ttk.Label(self.meal_frame, text=self.meal_name, font='bold')

        # Make frame to hold food labels.
        self.food_frame = ttk.Frame(self.meal_frame, borderwidth='5', relief='solid')

        # Make frame for food attributes.
        self.att_frame = ttk.Frame(self.meal_frame)

        # Make food attribute labels.
        self.cal_label = ttk.Label(self.att_frame, text='Calories:')
        self.pro_label = ttk.Label(self.att_frame, text='Protein:')
        self.carb_label = ttk.Label(self.att_frame, text='Carbs:')
        self.fat_label = ttk.Label(self.att_frame, text='Fats:')
        self.cal_num = ttk.Label(self.att_frame, text='232')
        self.pro_num = ttk.Label(self.att_frame, text='23')
        self.carb_num = ttk.Label(self.att_frame, text='232')
        self.fat_num = ttk.Label(self.att_frame, text='9')

        # Make a separator.
        self.sep = ttk.Separator(self.meal_frame, orient=HORIZONTAL)

        # Grid meal frame widgets.
        self.meal_frame.pack()
        self.meal_title.grid(column=0, row=0, pady='5 0', padx=10, sticky='w')
        self.sep.grid(column=0, row=2, columnspan=2, padx=5, sticky='ew', pady=5)

        # Grid food frame widgets.
        self.food_frame.grid(column=0, row=1, padx=10, sticky='nw')

        # Grid attribute frame widgets.
        self.att_frame.grid(column=1, row=1, pady='0 10', sticky='nw')
        self.cal_label.grid(column=0, row=0, sticky='w', padx='0 10')
        self.pro_label.grid(column=0, row=1, sticky='w')
        self.carb_label.grid(column=0, row=2, sticky='w')
        self.fat_label.grid(column=0, row=3, sticky='w')
        self.cal_num.grid(column=1, row=0, sticky='w', padx='0 10')
        self.pro_num.grid(column=1, row=1, sticky='w')
        self.carb_num.grid(column=1, row=2, sticky='w')
        self.fat_num.grid(column=1, row=3, sticky='w')

        # Make a blank frame to give food frame appropriate width.
        self.blank_frame = ttk.Frame(self.food_frame, width=250)
        self.blank_frame.pack(side='bottom')

        # Bind hover functionality.
        self.meal_frame.bind("<Enter>", self.enter_frame_color)
        self.meal_frame.bind("<Leave>", self.leave_frame_color)

        # Bind for selection functionality.
        self.meal_frame.bind("<ButtonRelease-1>", self.frame_pressed)
        self.meal_frame.bind("<FocusIn>", self.frame_focus)
        self.meal_frame.bind("<FocusOut>", self.lose_focus)
        # Bind as well so selection works smoothly. (Doesn't work on all widgets in frame.)
        self.food_frame.bind("<ButtonRelease-1>", self.frame_pressed)
        self.att_frame.bind("<ButtonRelease-1>", self.frame_pressed)
        self.blank_frame.bind("<ButtonRelease-1>", self.frame_pressed)
        self.cal_label.bind("<ButtonRelease-1>", self.frame_pressed)
        self.pro_label.bind("<ButtonRelease-1>", self.frame_pressed)
        self.carb_label.bind("<ButtonRelease-1>", self.frame_pressed)
        self.fat_label.bind("<ButtonRelease-1>", self.frame_pressed)
        self.cal_num.bind("<ButtonRelease-1>", self.frame_pressed)
        self.pro_num.bind("<ButtonRelease-1>", self.frame_pressed)
        self.carb_num.bind("<ButtonRelease-1>", self.frame_pressed)
        self.fat_num.bind("<ButtonRelease-1>", self.frame_pressed)
        self.meal_title.bind("<ButtonRelease-1>", self.frame_pressed)

        # Fill list
        self.populate_meal()

    def frame_pressed(self, event):
        self.meal_frame.focus_force()
        self.current_focus = True

    def frame_focus(self, *kwargs):
        if self.current_focus == True:
            self.meal_frame.configure(style='Focus.TFrame')
            self.food_frame.configure(style='Focus.TFrame')
            self.att_frame.configure(style='Focus.TFrame')
            self.blank_frame.configure(style='Focus.TFrame')
            self.cal_label.configure(style='Focus.TLabel')
            self.pro_label.configure(style='Focus.TLabel')
            self.carb_label.configure(style='Focus.TLabel')
            self.fat_label.configure(style='Focus.TLabel')
            self.cal_num.configure(style='Focus.TLabel')
            self.pro_num.configure(style='Focus.TLabel')
            self.carb_num.configure(style='Focus.TLabel')
            self.fat_num.configure(style='Focus.TLabel')
            self.meal_title.configure(style='Focus.TLabel')
            for label in self.label_list:
                label.configure(style='Focus.TLabel')

    def enter_frame_color(self, event):
        if self.current_focus == True:
            pass
        else:
            self.meal_frame.configure(style='Main.TFrame')
            self.food_frame.configure(style='Main.TFrame')
            self.att_frame.configure(style='Main.TFrame')
            self.blank_frame.configure(style='Main.TFrame')
            self.cal_label.configure(style='Main.TLabel')
            self.pro_label.configure(style='Main.TLabel')
            self.carb_label.configure(style='Main.TLabel')
            self.fat_label.configure(style='Main.TLabel')
            self.cal_num.configure(style='Main.TLabel')
            self.pro_num.configure(style='Main.TLabel')
            self.carb_num.configure(style='Main.TLabel')
            self.fat_num.configure(style='Main.TLabel')
            self.meal_title.configure(style='Main.TLabel')
            for label in self.label_list:
                label.configure(style='Main.TLabel')

    def leave_frame_color(self, enter):
        if self.current_focus == True:
            pass
        else:
            self.meal_frame.configure(style='TFrame')
            self.food_frame.configure(style='TFrame')
            self.att_frame.configure(style='TFrame')
            self.blank_frame.configure(style='TFrame')
            self.cal_label.configure(style='TLabel')
            self.pro_label.configure(style='TLabel')
            self.carb_label.configure(style='TLabel')
            self.fat_label.configure(style='TLabel')
            self.cal_num.configure(style='TLabel')
            self.pro_num.configure(style='TLabel')
            self.carb_num.configure(style='TLabel')
            self.fat_num.configure(style='TLabel')
            self.meal_title.configure(style='TLabel')
            for label in self.label_list:
                label.configure(style='TLabel')

    def lose_focus(self, *kwargs):
        self.meal_frame.configure(style='TFrame')
        self.food_frame.configure(style='TFrame')
        self.att_frame.configure(style='TFrame')
        self.blank_frame.configure(style='TFrame')
        self.cal_label.configure(style='TLabel')
        self.pro_label.configure(style='TLabel')
        self.carb_label.configure(style='TLabel')
        self.fat_label.configure(style='TLabel')
        self.cal_num.configure(style='TLabel')
        self.pro_num.configure(style='TLabel')
        self.carb_num.configure(style='TLabel')
        self.fat_num.configure(style='TLabel')
        self.meal_title.configure(style='TLabel')
        for label in self.label_list:
            label.configure(style='TLabel')
        self.current_focus = False
        # self.current_focus.set(False)

    def populate_meal(self):

        calorie_total = 0
        protein_total = 0
        carbs_total = 0
        fats_total = 0

        self.label_list = []

        for food in self.meal_list:
            self.food_label = ttk.Label(self.food_frame, text=f'{food.name}')
            self.food_label.bind("<ButtonRelease-1>", self.frame_pressed)
            self.food_label.pack(anchor='w')
            self.label_list.append(self.food_label)
            calorie_total += int(food.calories)
            protein_total += int(food.protein)
            carbs_total += int(food.carbs)
            fats_total += int(food.fats)

        self.cal_num['text'] = str(calorie_total)
        self.pro_num['text'] = str(protein_total)
        self.carb_num['text'] = str(carbs_total)
        self.fat_num['text'] = str(fats_total)


if __name__ == "__main__":

    # Create food objects for testing.
    food1 = Food('Chicken', 150, 25, 5, 10)
    food2 = Food('Rice', 200, 5, 30, 5)
    food3 = Food('Broccoli', 80, 4, 10, 2)
    food4 = Food('Salad', 180, 15, 34, 25)
    meal_list = [food1, food2, food3, food4]

    food5 = Food('Pizza', 324, 25, 5, 10)
    food6 = Food('Pasta', 244, 5, 30, 5)
    food7 = Food('Ravioli', 170, 4, 10, 2)
    food8 = Food('Bread', 180, 15, 34, 25)
    meal_list2 = [food5, food6, food7, food8]

    root = Tk()
    main_meal_frame = ttk.Frame(root)
    main_meal_frame.pack()

    meal = Meal(meal_list, main_meal_frame, 'meal1')
    meal2 = Meal(meal_list2, main_meal_frame, 'meal2')
    meal.show_meal()
    meal2.show_meal()

    # Run main loop.
    root.mainloop()


# POSSIBLY LOOK INTO DRAG AND DROP FUNCTIONALITY.
# WILL BE PUTTING THIS INTO NOTEBOOK WIDGETS BY ORDER OF:
# IF BREAKFAST, SNACK, LUNCH, DINNER, PREWORKOUT, POSTWORKOUT, OTHER
# MAKE LOOK BETTER BY CHANGING FONTS AND COLORS.

# MAKE MEAL LIST CLASS
