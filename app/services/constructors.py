from ..models.models import Team
from ..models.models import Match

from pathlib import Path
import pdfplumber
import re


def matches_dict_constructor(teams_dict: list[dict]) -> list[dict]:
    BASE_DIR = Path(__file__).resolve().parent.parent
    pdf_path = BASE_DIR / "../app/tabela_detalhada_campeonato_brasileiro_serie_a_2025.pdf"
    texto_completo = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            texto_completo += page.extract_text() + "\n"

    chunks = texto_completo.split('Ref')
    matches_dict = []
    for chunk in chunks:
        texto = chunk.strip()
        if not texto:
            continue

        found = []
        for team in teams_dict:
            idx = texto.find(team['name'])
            if idx != -1:
                found.append((idx, team['name']))
        
        if len(found) < 2:
            continue
        
        found.sort(key=lambda x: x[0])

        home = found[0][1]
        away = found[1][1]

        m_placar = re.search(r"(\d+)\s*x\s*(\d+)", texto)
        
        result = None
        if m_placar is not None:
            gols_mandante = int(m_placar.group(1))
            gols_visitante = int(m_placar.group(2))    
            if gols_mandante > gols_visitante:
                result = home
            elif gols_mandante < gols_visitante:
                result = away
            else:
                result = "draw"
                
        matches_dict.append({'home': home, 'away': away, 'result': result})
    
    return matches_dict

def team_constructor(teams_dict: list[dict]) -> list[Team]:
    teams_class = []
    for t in teams_dict:
        team = Team(name=t['name'], strength_vector=[1/3, 1/3, 1/3])
        teams_class.append(team)
    
    return teams_class

def match_constructor(matches_dict: list[dict]) -> list[Match]:
    matches_class = []
    for m in matches_dict:
        match = Match(home=m['home'], away = m['away'], result=m['result'])
        matches_class.append(match)
    
    return matches_class

