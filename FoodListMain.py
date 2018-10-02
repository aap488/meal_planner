# -*- coding: utf-8 -*-
"""
Created on Tue Aug  7 05:55:25 2018

@author: aap48
"""


class FoodList:

    def __init__(self, saved_foods):
        self.saved_foods = saved_foods
        self.current_sort = None

    def sort_name(self):
        """ Sort the list stored in saved_foods by the objects name attribute. """

        self.saved_foods.sort(key=lambda food: food.name)
        self.current_sort = 'name'

    def sort_calories(self):
        """ Sort the list stored in saved_foods by the objects calories attribute. """

        self.saved_foods.sort(key=lambda food: int(food.calories), reverse=True)
        self.current_sort = 'calories'

    def sort_protein(self):
        """ Sort the list stored in saved_foods by the objects protein attribute. """

        self.saved_foods.sort(key=lambda food: int(food.protein), reverse=True)
        self.current_sort = 'protein'

    def sort_carbs(self):
        """ Sort the list stored in saved_foods by the objects carbs attribute. """

        self.saved_foods.sort(key=lambda food: int(food.carbs), reverse=True)
        self.current_sort = 'carbs'

    def sort_fats(self):
        """ Sort the list stored in saved_foods by the objects fats attribute. """

        self.saved_foods.sort(key=lambda food: int(food.fats), reverse=True)
        self.current_sort = 'fats'
