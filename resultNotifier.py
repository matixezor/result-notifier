import requests
import time
from config import headers, url, my_team, ifttt_webhook_url


def connection_and_parse(url, headers):
    response = requests.get(url, headers=headers)
    response = response.json()
    
    return response["api"]["fixtures"][0]


def join_strings(*args):
    return " ".join(arg for arg in args)

    
def send_ifttt_notification(ifttt_webhook_url, match_result):
    result_with_team_names = join_strings(
        match_result["home_team"],
        match_result["score"],
        match_result["away_team"]
        )
    data = {
        "value1": match_result["league"],
        "value2": result_with_team_names
        }
    
    requests.post(ifttt_webhook_url, json=data)


def get_match_timestamp_and_id(url, headers, my_team):
    url += "team/" + my_team + "/next/1"
    response = connection_and_parse(url, headers)
    
    return {
        "fixtureID": str(response["fixture_id"]),
        "timestamp": response["event_timestamp"]
        }


def wait_till_full_time(match_timestamp):
    curr_timestamp = time.time()
    time_to_wait = match_timestamp - curr_timestamp + 7200
    time.sleep(time_to_wait)
    

def get_match_result(url, headers, fixture_id):
    url += "id/" + fixture_id
    response = connection_and_parse(url, headers)

    while response["statusShort"] not in ["AEN", "PEN", "FT"]:
        # in case there's extra time or penalties sleep 15 min
        time.sleep(900)
        response = connection_and_parse(url, headers)        
    
    return {
        "league": response["league"]["name"],
        "home_team": response["homeTeam"]["team_name"],
        "away_team": response["awayTeam"]["team_name"],
        "score": str(response["goalsHomeTeam"]) + '-' + str(response["goalsAwayTeam"])
        }

    
def main(headers, url, my_team, ifttt_webhook_url):
    while True:
        match_timestamp_and_id = get_match_timestamp_and_id(url, headers, my_team)
        wait_till_full_time(match_timestamp_and_id["timestamp"])
        match_result = get_match_result(url, headers, match_timestamp_and_id["fixtureID"])

        send_ifttt_notification(ifttt_webhook_url, match_result)


if __name__== "__main__" :
    main(headers, url, my_team, ifttt_webhook_url)
