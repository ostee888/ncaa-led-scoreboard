import requests
from datetime import datetime, timedelta

def get_game_data(team_name="Michigan Tech"):
    # Get the current time in Mountain Time
    current_time_mt = datetime.utcnow() - timedelta(hours=7)
    
    while True:
        try:
            # Construct the endpoint URL with the current date
            endpoint = f"https://ncaa-api.henrygd.me/scoreboard/icehockey-men/d1/{current_time_mt.strftime('%Y/%m/%d')}"

            # Send a GET request to the endpoint
            response = requests.get(endpoint)
            
            # Check if the request was successful
            if response.status_code == 200:
                data = response.json()  # Parse the JSON response

                # Iterate over the games to find the one involving the specified team
                for game in data.get("games", []):
                    # Extract away and home team short names
                    away_short_name = game["game"]["away"]["names"]["short"]
                    home_short_name = game["game"]["home"]["names"]["short"]

                    # Check if either the away or home team short name exactly matches the specified team name
                    if away_short_name == team_name or home_short_name == team_name:
                        # Extract game information
                        game_id = game["game"]["gameID"]
                        away_team = game["game"]["away"]["names"]["char6"]
                        away_score = game["game"]["away"]["score"]
                        home_team = game["game"]["home"]["names"]["char6"]
                        home_score = game["game"]["home"]["score"]
                        winner = home_team if game["game"]["home"]["winner"] else away_team
                        loser = away_team if game["game"]["home"]["winner"] else home_team
                        start_time = game["game"]["startTime"]
                        start_date = game["game"]["startDate"]
                        current_period = game["game"]["currentPeriod"]
                        game_state = game["game"]["gameState"]
                        game_time = game["game"]["contestClock"]

                        #Shortens names to 3 charachters
                        away_team = away_team[:3]
                        home_team = home_team[:3]

                        # Return the game information and the date it was found
                        return game_id, away_team, away_score, home_team, home_score, winner, loser, start_time, start_date, current_period, game_state, game_time, current_time_mt

                # If no game involving the specified team is found, increment the date by one day
                current_time_mt += timedelta(days=1)
            
            elif response.status_code == 404:
                # If the resource is not found (404), increment the date by one day
                current_time_mt += timedelta(days=1)
            else:
                print("Error:", response.status_code)
                return None  # Return None if the request was not successful
        
        except requests.exceptions.RequestException as e:
            print("Request error:", e)
            # Increment the date by one day
            current_time_mt += timedelta(days=1)

# Example usage:
#game_data = get_game_data()
#print(game_data)  # Replace this with whatever you want to do with the game data
