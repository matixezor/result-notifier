import time
from typing import Dict, Any, Union

import requests

from config import headers, url, my_team, ifttt_webhook_url


def connection_and_parse(url: str, headers: Dict[str, str]) -> Dict[str, Any]:
    response = requests.get(url, headers=headers)
    response = response.json()

    return response["api"]["fixtures"][0]


def join_strings(*args: str) -> str:
    return " ".join(arg for arg in args)


def send_ifttt_notification(ifttt_webhook_url: str, match_result: Dict[str, str]):
    result_with_team_names = join_strings(
        match_result["home_team"],
        match_result["score"],
        match_result["away_team"]
    )
    data = {
        "value1": match_result["league"],
        "value2": result_with_team_names,
        "value3": match_result["goals"]
    }

    requests.post(ifttt_webhook_url, json=data)


def get_match_timestamp_and_id(url: str, headers: Dict[str, str], my_team: str) -> Dict[str, Union[str, int]]:
    url += "team/" + my_team + "/next/1"
    response = connection_and_parse(url, headers)

    return {
        "fixtureID": str(response["fixture_id"]),
        "timestamp": response["event_timestamp"]
    }


def wait_till_full_time(match_timestamp: int):
    curr_timestamp = time.time()
    time_to_wait = match_timestamp - curr_timestamp + 7200
    time.sleep(time_to_wait)


def get_match_result(url: str, headers: Dict[str, str], fixture_id: str) -> Dict[str, str]:
    url += "id/" + fixture_id
    response = connection_and_parse(url, headers)

    while response["statusShort"] not in ["AEN", "PEN", "FT"]:
        # in case there's extra time or penalties sleep 15 min
        time.sleep(900)
        response = connection_and_parse(url, headers)

    goals = ''
    if response["goalsHomeTeam"] + response["goalsAwayTeam"] != 0:
        for event in response["events"]:
            if event["type"] == "Goal" and event["detail"] != "Missed Penalty":
                time = event["elapsed"] + event["elapsed_plus"] if event["elapsed_plus"] else event["elapsed"]
                
                player = event["player"] if event["detail"] != "Own Goal" else f"{event['player']} (OG)"
                player += " (P)" if event["detail"] == "Penalty" else ""
                
                goals += f"{time} - {player}\n"

    return {
        "league": response["league"]["name"],
        "home_team": response["homeTeam"]["team_name"],
        "away_team": response["awayTeam"]["team_name"],
        "score": str(response["goalsHomeTeam"]) + '-' + str(response["goalsAwayTeam"]),
        "goals": goals
    }


def main(headers: Dict[str, str], url: str, my_team: str, ifttt_webhook_url: str):
    while True:
        match_timestamp_and_id = get_match_timestamp_and_id(url, headers, my_team)
        wait_till_full_time(match_timestamp_and_id["timestamp"])
        match_result = get_match_result(url, headers, match_timestamp_and_id["fixtureID"])

        send_ifttt_notification(ifttt_webhook_url, match_result)


if __name__ == "__main__":
    main(headers, url, my_team, ifttt_webhook_url)
