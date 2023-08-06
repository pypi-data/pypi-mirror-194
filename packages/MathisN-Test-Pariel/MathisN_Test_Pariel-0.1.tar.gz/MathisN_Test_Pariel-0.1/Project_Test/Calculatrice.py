#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 27 15:09:53 2023

@author: mathis.nenach
"""

class Calculatrice:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def addition(self):
        return self.x + self.y
    
    def soustraction(self):
        return self.x - self.y
    
    def multiplication(self):
        return self.x * self.y
    
    def division(self):
        if self.y == 0:
            return "Impossible de diviser par zéro"
        else:
            return self.x / self.y