import requests
from lxml import html
from bs4 import BeautifulSoup as Soup
import json
import sys

cbsUrl = 'https://www.cbssports.com/nfl/draft/prospect-rankings/'

req = requests.get(cbsUrl)
soup = Soup(req.text)
count = 0

maxPlayers = int(input("Enter max number of players to grab: "))

playerStruct = { 'players': {},
        'ids': []

}


for row in soup.find_all('tbody'):

    names = row.find_all('td', {'class': 'cell-bold-text cell-player'})
    

    if (names != None):
        if (count > maxPlayers):
            break
        for row2 in names:
            if (count > maxPlayers):
                break
            rank = row2.find_next_siblings('td')
            school = rank[0].text.strip()
            year = rank[1].text.strip()
            pos = rank[2].text.strip()

            site = ""

            link = row2.find('a')
            if link != None:
                site = link['href']

            content = row2.text.strip()

            id = content.replace(" ", "-")

            playerStruct['players'][id] = {
                'id': id,
                'content': content,
                'pos' : pos,
                'school' : school,
                'site' : site
            }

            playerStruct['ids'].append(id)

            count += 1
    

with open('cbsDraftPlayers-' + str(maxPlayers) + '.json', 'w') as json_file:
    json.dump(playerStruct, json_file)