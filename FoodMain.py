# -*- coding: utf-8 -*-
"""
Created on Sat Jul 28 02:15:09 2018

@author: aap48
"""


class Food():

    """ Class to create food items from. """

    def __init__(self, name='', calories=0, protein=0, carbs=0, fats=0):
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fats = fats

    def __str__(self):
        return self.name
