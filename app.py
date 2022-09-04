# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
from flask import Flask, render_template


app = Flask(__name__, static_url_path='/static')

TEAM_ICON = {
    "EVE": 11,
    "LIV": 14,
    "BRE": 94,
    "LEE": 2,
    "CHE": 8,
    "WHU": 21,
    "NEW": 4,
    "CRY": 31,
    "NFO": 17,
    "BOU": 91,
    "TOT": 6,
    "FUL": 54,
    "WOL": 39,
    "SOU": 20,
    "AVL": 7,
    "MCI": 43,
    "BHA": 36,
    "LEI": 13,
    "MUN": 1,
    "ARS": 3,
}


@app.route('/')
def index():
    week, match_list = get_match_list()
    return render_template('index.html', week=week, matches=match_list)


def get_match_list():
    url = "https://www.premierleague.com/home"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, 'lxml')
    raw_matches = soup.find_all('a', {'class':'embeddableMatchContainer'})
    week = soup.find('div', {"class": "week"}).text
    match_list = []
    for raw_match in raw_matches:
        home, away = [i.text.strip() for i in raw_match.find_all('span', {'class':'teamName'})]
        score = raw_match.find('span', {'class':'score'})
        match_list.append({
            'home': home,
            'home_icon': f"t{TEAM_ICON[home]}.png",
            'away': away,
            'away_icon': f"t{TEAM_ICON[away]}.png",
            'score_html': score if score else "<span class='score'>-<span>-</span>-</span>",
        })
    return week, match_list



@app.route('/<path:path>')
def static_file(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    app.run(debug=True)
