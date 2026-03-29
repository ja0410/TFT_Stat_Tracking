import requests



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

# function with print statements for testing if needed
def info_test(user, tag, api_key, puuid):
    print(user_puuid(user, tag, api_key))
    print(summoner_info(puuid, api_key))
    print(tft_matches(puuid, api_key))

# function for getting summoner placement in the last 20 games, as well as average placement
def match_avg_placement(game_data, env):
    matchplace = 0
    for game in game_data:
        game_results = game_data[game]
        placement = game_results['placement']
        matchplace += int(placement)
        if env == 'test':
            print(placement)
    avg_place = matchplace / 20
    print(avg_place)