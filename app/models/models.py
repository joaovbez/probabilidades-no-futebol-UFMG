from __future__ import annotations

from ..utils.config import P
import numpy as np
import random

class Match():
    def __init__(self, home, away, result): 
        self.home = home
        self.away = away

        if result != '':
            self.result = result
        else:
            self.result = None
        
        self.probability_array = None
        
    def define_probability_array(self, probability_array):
        self.probability_array = probability_array
        
    def run_predict_result(self):
        if self.result is not None:
            raise ValueError(f'A partida já tem um resultado registrado')
        
        probability_array = self.probability_array
        result = None
        random_number = random.random()
        
        if 0 <= random_number <= probability_array[0]: # vitoria do mandante
            self.result = self.home
        elif probability_array[0] <= random_number <= probability_array[0] + probability_array[1]: # empate
            self.result = "draw"
        elif probability_array[0] + probability_array[1] <= random_number <= 1: # vitoria do visitante
            self.result = self.away
        
        return result
    

class Team():
    def __init__(self, name, strength_vector):
        self.name = name
        self.strength_vector = strength_vector
        self.performance = 1/2
        self.points = 0
        self.wins = 0
        self.draws = 0
        self.losses = 0
        self.matches = []

    def register_result(self, match: Match):
        if match.result == self.name:
            self.points += 3
            self.wins += 1
        elif match.result == "draw":
            self.points += 1
            self.draws += 1
        else:
            self.losses += 1
        
        self.matches.append(match)
    
    def update_performance(self):
        matches = self.matches
        max_points = len(matches)*3
        real_points = self.points

        self.performance = real_points / max_points

    def update_strength_vector(self, match: Match, opponent: Team):
        actual_strength_vector = np.array(self.strength_vector)
        victory_array = np.array([1,0,0])
        lose_array = np.array([0,0,1])
        draw_array = np.array([0,1,0])
        half_victory_array = np.array([1/2,1/2,0])
        half_lose_array = np.array([0,1/2,1/2])

        r = opponent.performance

        if match.result == self.name:
            actual_strength_vector = (P*actual_strength_vector + r*victory_array)/(P + r)
        elif match.result != "draw":
            actual_strength_vector = (P*actual_strength_vector + (1-r)*lose_array)/(P + (1 - r))
        else:
            if r <= 1/2:
                actual_strength_vector = (P*actual_strength_vector + (1-2*r)*half_lose_array + 2*r*draw_array)/(P + 1)
            else: 
                actual_strength_vector = (P*actual_strength_vector + (2*r - 1)*half_victory_array + 2*(1 - r)*draw_array)/(P + 1)

        self.strength_vector = actual_strength_vector.tolist()
