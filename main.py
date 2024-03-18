import liveGameData
from matrixFunctions import compose_image , add_logo_to_image, add_text_to_image, create_blank_image
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from datetime import datetime
from PIL import Image
import requests
from io import BytesIO
import os
import time
import sched
#os.system("clear")

#TO RUN IN BACKGROUND:
#nohup sudo python3 main.py
#TO STOP
#pkill -f main.py



# Configuration for the RGB matrix
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat-pwm'
options.gpio_slowdown = 4
options.limit_refresh_rate_hz = 120
options.brightness = 75

# Create matrix object
matrix = RGBMatrix(options=options)

# Setup schedulers
scheduler = sched.scheduler(time.time, time.sleep)
counter = 0

teamName = "Michigan Tech"
logo_url1 = "https://ccha.com/images/2021/5/11/Michigan_Tech_Logo_31.png"
logo_url2 = "https://upload.wikimedia.org/wikipedia/en/thumb/e/e9/Bemidji_State_Beavers_logo.svg/1200px-Bemidji_State_Beavers_logo.png"

while True:

    
    #Gets Current Game Data
    game_id, away_team, away_score, home_team, home_score, winner, loser, start_time, start_date, current_period, game_state, clock, game_date = liveGameData.get_game_data(teamName)
    
    #Processing
    if (home_team == "MIT"):
        home_team = "MTU"
    if (away_team == "MIT"):
        away_team = "MTU"
    
    #Formatting Game Date
    game_date = game_date.strftime("%m/%d")
    print(game_date)  # Output: 03/22
    if game_date.startswith('0'): #gets rid of 0
        game_date = game_date[1:]
    
    #Formatting Game Time
    raw_start_time = start_time
    start_time = start_time.replace(" ET", "")
    start_time = datetime.strptime(start_time, "%I:%M%p")
    start_time = start_time.strftime("%-I:%M")


    
    os.system("clear")
    print("Period:", current_period)
    print(game_id)
    print("Away", away_team)
    print(away_score)
    print("Home", home_team)
    print(home_score)
    print("Game Time:", raw_start_time)
    print("State", game_state)
    print("Date Of Game", game_date)
    print(clock)
    print(counter)
    #print(type(home_score))
    

    
    #Created Blank Image
    composed_image = create_blank_image(matrix.width, matrix.height) 

    # Add Images
    add_logo_to_image(composed_image, logo_url1, (-1,16), 48)
    add_logo_to_image(composed_image, logo_url2, (61,16), 38)


    #Add Text
    #add_text_to_image(composed_image, away_team, (14,4), 5)
    add_text_to_image(composed_image, "vs", (32,16), 8, 6)
    add_text_to_image(composed_image, game_date, (33,3), 5, 1)
    add_text_to_image(composed_image, start_time, (33,26), 5, 1)
    matrix.SetImage(composed_image)

    
    
    #composed_image = compose_image(matrix, [away_team, home_team, away_score, home_score, current_period, gameTime], [(10, 4), (54, 4), (10, 20), (54, 20), (32,4), (32,11)], [logo_url1, logo_url2], [(27, 16), (62, 16)], [56, 42])
    # Display the composed image on the matrix
    #matrix.SetImage(composed_image)


    
    #display_text(matrix,away_team,2,0,5)
    #display_text(matrix,home_team,50,0,5)
    #overlay_images(matrix, [logo_url1, logo_url2], [(2, 16), (62, 16)], [56, 42])
    #image = Image.new("RGB", (matrix.width, matrix.height), color="black")
    #display_text(matrix, [away_team, home_team, away_score, home_score, current_period, gameTime], [(10, 4), (54, 4), (10, 20), (54, 20), (32,4), (32,11)], 5)
    #overlay_images(matrix, [logo_url1, logo_url2], [(2, 16), (62, 16)], [56, 42])

    #if (game_state == "pre"): #Before Game
        #print("test")
    #if (game_state == "live"): #In Progress
        #overlay_images(matrix, teamLogo,(0,0), 40)
        #overlay_images(matrix, [logo_url1, logo_url2], [(2, 16), (62, 16)], [56, 42])
         #display_text_on_image(image, [away_team, home_team, away_score, home_score, current_period, gameTime], [(10, 4), (54, 4), (10, 20), (54, 20), (32,4), (32,11)], 5)
        ####

    
    counter = counter+1
    time.sleep(2)
    