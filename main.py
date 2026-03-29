from configparser import ConfigParser
from TFT_Functions import *
config = ConfigParser()
config.read('config.ini')





if __name__ == '__main__':
    # api key, hidden in .ini file
    api_key = config['parameters']['key']
    # set environment
    env = config['parameters']['env']
    # basic flag for username
    summoner_flag = True
    # summoner name and tag loop
    while summoner_flag:
        # user input for summoner name
        user = input('Username: ')
        # user input for summoner tag
        tag = input('Tag: ')
        # attempt to retrieve summoner puuid via try block
        try:
            # set variable = to summoner puuid
            puuid = user_puuid(user, tag, api_key)
            # if puuid is returned, set flag too false to break out of loop
            if puuid:
                summoner_flag = False
        # if nothing is returned, set flag to true to restate user and tag input
        except:
            summoner_flag = True
            print('User not found')
    # set variable equal to list of *last 20* match id's
    match_ids = tft_matches(puuid, api_key)
    # print out testing statements if testing along with normal prints
    if env == 'test':
        info_test(user, tag, api_key, puuid)
    # open a blank dictionary for summoner match data
    game_data = {}
    # make the length of match id's into a variable to keep track of how many need to be processed still
    matches_left = len(match_ids)
    # loop through match_id's, recording summoner data from each match into a dictionary
    for match_id in match_ids:
        # let summoner know how many more matches need to process before data return
        print(f"{matches_left} match(es) left to process")
        # returns all participant data from match currently being read
        game_info = match_info(match_id, api_key)['info']['participants']
        # loop through participants in match until correct summoner is found, then data for that summoner is returned
        for participant in game_info:
            if participant.get('puuid') == puuid:
                # once correct puuid is found in match, push summoner data to dictionary with match_id as its key
                game_data[match_id] = participant
                # every time a match is processed, take 1 off counter variable before moving to next match
                matches_left -= 1
                break
    # print data to verify in test
    if env == 'test':
        match = match_ids[1]
        print(game_data[match])
    match_avg_placement(game_data, env)