from ..models.models import Team, Match

def get_team(team_name: str, teams: list[Team]) -> Team | None:
    team = next((t for t in teams if t.name == team_name), None)
    if team is None:
        print(f"Nenhum time com o nome {team_name} foi encontrado no Array informado")
    return team

def get_probability_array(home: Team, away: Team) -> list:
    probability_array = [0, 0, 0]

    probability_array[0] = (home.strength_vector[0] + away.strength_vector[2])/2 
    probability_array[1] = (home.strength_vector[1] + away.strength_vector[1])/2 
    probability_array[2] = (home.strength_vector[2] + away.strength_vector[0])/2

    return probability_array 