#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 13:38:51 2023

@author: benoit.jomain
"""
from numpy import zeros
class deplacement:
    """Classe qui instancie une grille et qui gère les déplacements d'un robot"""

    def __init__(self,lines,columns):
        
        if not isinstance(lines, int) or not isinstance(columns,int):
            raise ValueError("You don't give an integer")
        if (lines or columns) < 2 or (lines or columns) >= 31 :    
            self.lines = 20
            self.columns = 20
            raise ValueError("height error")
        self.lines = lines
        self.columns = columns
        self.pos_X = 0
        self.pos_Y = 0
        self.grid = zeros((self.lines, self.columns),int)
        self.grid[self.pos_X][self.pos_Y] = 1

    def Print(self):
        """Affichage de la grille de déplacement"""
        print("grille")
        for line in self.grid :
            print(line)

    def up(self):
        """Fonction qui vérifie et fait le déplacement up s'il est possible"""
        if self.pos_X > 1 :
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_X -= 1
            self.grid[self.pos_X][self.pos_Y] = 1
        return "ERROR"

    def down(self):
        """Fonction qui vérifie et fait le déplacement down s'il est possible"""
        if self.pos_X < self.lines :
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_X += 1
            self.grid[self.pos_X][self.pos_Y] = 1
        return "ERROR"
        
    def left(self):
        """Fonction qui vérifie et fait le déplacement left s'il est possible"""
        if self.pos_Y > 1 :
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_Y -= 1
            self.grid[self.pos_X][self.pos_Y] = 1
        return "ERROR"

    def right(self):
        """Fonction qui vérifie et fait le déplacement right s'il est possible"""
        if self.pos_Y < self.columns :
            self.grid[self.pos_X][self.pos_Y] = 0
            self.pos_Y += 1
            self.grid[self.pos_X][self.pos_Y] = 1
        return "ERROR"

robot1 = deplacement(10,10)
robot1.Print()
#
#if __name__ == "__main__":
#
#    robot1.down()
#    robot1.Print()
#    robot1.down()
#    robot1.down()
#    robot1.Print()
        
        
        