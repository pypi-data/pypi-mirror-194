# -*- coding: utf-8 -*-
"""
Created on Fri Feb  3 16:53:41 2023

@author: mathi
"""
from numpy import zeros
from math import ceil

class Grid: 
    """Classe qui crée une grille selon le nombre de colonnes et de lignes passés par l'utilisateur
       il permet également au robot d'effectuer des déplacements"""
    def __init__(self,nb_lines,nb_colums):
        if isinstance(nb_lines,int) and isinstance(nb_colums,int) :
            if nb_lines < 20 and nb_lines > 1 and nb_colums < 20 and nb_colums > 1:
                self.nb_lines = nb_lines
                self.nb_colums = nb_colums
            if nb_lines > 20 or nb_lines < 1 or nb_colums > 20 or nb_colums < 1: 
                self.nb_lines = 10
                self.nb_colums = 10 
                raise ValueError("You cannot enter this value for lines/colums")
        else : 
            raise ValueError("Value is not an instance of int")
                
        self.grid = zeros((self.nb_lines,self.nb_colums), int)
        self.robot_x = ceil(self.nb_lines/2)
        self.robot_y = ceil(self.nb_colums/2)
        self.robot_position = self.grid[self.robot_x][self.robot_y] = 1

    def refresh(self) : 
        """Mets l'ancienne position du robot à 0 sur la grille"""
        self.robot_position = self.grid[self.robot_x][self.robot_y] = 0
    
    def actualisation(self) : 
        """Mets la position du robot actuelle à 1 sur la grille"""
        self.robot_position = self.grid[self.robot_x][self.robot_y] = 1
        
            
    def move_to_right(self):
        """methode pour déplacer le robot d'une case à droite"""
        if self.robot_y < self.nb_colums - 1: 
            self.refresh()
            self.robot_y += 1
            self.actualisation()
        else :
            return "strike the edge !"

    def move_to_left(self):
        """methode pour déplacer le robot d'une case à gauche"""
        if self.robot_y > 0:
            self.refresh()
            self.robot_y -= 1
            self.actualisation()
        else :
            return "strike the edge !"

    def move_to_up(self):
        """methode pour déplacer le robot d'une case vers le haut"""
        if self.robot_x > 0:
            self.refresh()
            self.robot_x -= 1
            self.actualisation()
        else :
            return "strike the edge !"
    
    def move_to_down(self):
        """methode pour déplacer le robot d'une case vers le bas"""
        if self.robot_x < self.nb_lines - 1:
            self.refresh()
            self.robot_x += 1
            self.actualisation()
        else :
            return "strike the edge !"
            
