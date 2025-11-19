from .utils.config import TOTAL_SIMULATIONS
from .utils.data import teams_dict
from .services.constructors import matches_dict_constructor, team_constructor, match_constructor
from .services.selectors import get_team, get_probability_array
from .models.models import Team, Match

from pathlib import Path
import pdfplumber
import numpy as np

def run_past_match(match: Match, home:Team, away:Team):    
    home.register_result(match)
    away.register_result(match)

    home.update_strength_vector(match, opponent=away)
    away.update_strength_vector(match, opponent=home)

    home.update_performance()
    away.update_performance()

def run_future_match(match: Match, home:Team, away:Team):
    probability_array = get_probability_array(home, away)
    match.define_probability_array(probability_array=probability_array)
    match.run_predict_result()
    run_past_match(match=match, home=home, away=away)

if __name__ == '__main__':

    yes = 0
    total = 1
    
    for i in range(1, 100):
        teams = team_constructor(teams_dict=teams_dict)
        matches_dict = matches_dict_constructor(teams_dict=teams_dict)
        matches = match_constructor(matches_dict=matches_dict)
        home = None
        away = None
        for match in matches:
            home = get_team(team_name=match.home, teams=teams)
            away = get_team(team_name=match.away, teams=teams)
            if match.result is not None:
                run_past_match(match=match, home=home, away=away)
            else:
                run_future_match(match=match, home=home, away=away)
        
        teams.sort(key=lambda x: x.points)
        internacional = None
        for index, team in enumerate(teams):
            if team.name == 'INTERNACIONAL' and index <= 3:
                yes += 1
                print(f"Simulação de nº{total}, INTERNACIONAL foi rebaixado {yes} vezes. Nesta simulacao ficou em {20-index}º")
            elif team.name == 'INTERNACIONAL':
                print(f"Simulação de nº{total}, INTERNACIONAL foi rebaixado {yes} vezes. Nesta simulacao ficou em {20-index}º")            
        total += 1

    
    print(f"A probabilidade do internacional ser rebaixado é {yes}/{total} = {yes/total}")