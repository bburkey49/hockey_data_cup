import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import csv
import os 



def convert_time(str_time):
    mins, sec = map(lambda x: int(x), str_time.split(':'))
    return sec + (mins * 60)


def convert_game_time(str_time, period_no):
    mins, sec = map(lambda x: int(x), str_time.split(':'))
    return (20 * 60 * (period_no-1)) + 20 * 60 - convert_time(str_time)




with open('../big_data_cup_2021/hackathon_womens.csv', 'r') as csvfile:
    df = pd.read_csv(csvfile, delimiter=',', )

    game_no = []
    curr_game = 1
    last_period = 1
    for curr_period in df["Period"]:
        # print((curr_period))
        if curr_period == 1 and last_period != 1:
            curr_game += 1
        last_period = curr_period
        game_no.append(curr_game)

    df['game'] = game_no

    cum_times = []
    cum_time_since_game_start = []
    poss = []
    last_timestamp = 1200
    timer = 0
    prev_game = None
    prev_team = None
    for event, home, away, team_poss, clock, period in zip(df["Event"], df["Home Team"], df["Away Team"], df["Team"], df["Clock"], df["Period"]):
        clock_sec = convert_time(clock)
        timer += abs(clock_sec - last_timestamp)
        if event == "Faceoff Win" or prev_team != team_poss or timer >= 1200:
            timer = 0
        
        sign = 0
        if team_poss == home:
            sign = 1
        elif team_poss == away:
            sign = -1

        cum_times.append(timer * sign)
        cum_time_since_game_start.append(convert_game_time(clock, period))
        last_timestamp = clock_sec
        prev_team = team_poss

    df['time_of_possession'] = cum_times
    df['cum_time_since_game_start'] = cum_time_since_game_start



    newthing = df.loc[df['game'] == 8]


    for top, clock in zip(newthing['time_of_possession'], list(map(convert_time, newthing['Clock']))):
        print(f'CumTime: {top} | Clock: {clock}')

    # plot
    fig, ax = plt.subplots()
    ax.plot(newthing['time_of_possession'], newthing['cum_time_since_game_start'])

    ax.set(xlabel='Time of Possession (s)', ylabel='Time Since Game Start (s)',
        title='Fuck off')
    ax.grid()

    fig.savefig("test.png")
    plt.show()
















    
        