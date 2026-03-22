import requests
from configparser import ConfigParser
import json
from datetime import datetime

config = ConfigParser()
config.read('config.ini')

# after getting username and tag, get summoners unique puuid
def user_puuid(user, tag, api_key):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user}/{tag}"

    payload = {}
    headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()['puuid']

# use the puuid gathered in above function to get user data (level, icon, etc.)
def summoner_info(puuid, api_key):
    url = f"https://na1.api.riotgames.com/tft/summoner/v1/summoners/by-puuid/{puuid}"

    payload = {}
    headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

# get last 20 matches of tft playing by summoner
def tft_matches(puuid, api_key):
    url = f"https://americas.api.riotgames.com/tft/match/v1/matches/by-puuid/{puuid}/ids?start=0&count=20"
    payload = {}
    headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()

# using match id of above function, get match data NOTE: large, 1600 line return, parse out only data you need for simplicity
def match_info(match_id, api_key):
    url = f'https://americas.api.riotgames.com/tft/match/v1/matches/{match_id}'

    payload = {}
    headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}
    response = requests.request("GET", url, headers=headers, data=payload)
    return response.json()


def info_test(user, tag, api_key, puuid, game_info):
    print(user_puuid(user, tag, api_key))
    print(summoner_info(puuid, api_key))
    print(tft_matches(puuid, api_key))
    print(game_info)

if __name__ == '__main__':
    # api key, hidden in .ini file
    api_key = config['parameters']['key']
    # set environment
    env = config['parameters']['env']
    # user input for summoner name
    user = input('Username: ')
    # user input for summoner tag
    tag = input('Tag: ')
    # set variable = to summoner puuid
    puuid = user_puuid(user, tag, api_key)
    # set variable equal to list of *last 20* match id's
    match_ids = tft_matches(puuid, api_key)
    if env == 'test':
        info_test(user, tag, api_key, puuid, match_ids)
    game_data = {}
    for match_id in match_ids:
        print(match_id)
        game_info = match_info(match_id, api_key)['info']['participants']
        for participant in game_info:
            if participant.get('puuid') == puuid:
                game_data[match_id] = participant
                break
        print(game_data)