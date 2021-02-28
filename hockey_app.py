import csv
import pandas as pd
import os

# Output config
INPUT_DIR = '../big_data_cup_2021/'
OUTPUT_DIR = './output/'
BATCH_DIR = './batch/'
TMP_DIR = './tmp/'
# create batch paths
os.makedirs(OUTPUT_DIR + BATCH_DIR, exist_ok=True)




###########################################################
###########################################################
###############                             ###############
###############          MAIN APP           ###############
###############                             ###############
###########################################################
###########################################################

def main():
    # load in data, parse it in pandas df
    fn = 'hackathon_nwhl.csv'
    df = initialize_data(fn)


    #######################################################
    #######################################################
    # Sample Usage
    #######################################################
    # select team of interest -- globals for lists of team names
    team = womens_teams[0] # team = 'Erie Otters'

    # select game of interest (single int: 0 or list: [1,2] acceptable here)
    game_no = None 

    # select opposition of interest (list or None also accepted)
    opposing =  None # 'Olympic (Women) - Olympic Athletes from Russia'

    # header fields of interest to record in output file
    fields_of_interest = ['Event', 'Home Team', 'Away Team', 'game_date']
    
    # summary stat of interest (see Summary Statistics)
    stat = 'zone-entry' 
    
    recorded_fields = list(set(preserve_fields[stat].copy() + fields_of_interest)) # processing..
    processed = extract(
        df, 
        team, 
        recorded_fields, 
        opposing, 
        game_no
    ) # prrrrocessssssinnnnng......
    print(summarize(processed, team, stat)) # blamo




    #######################################################
    #######################################################
    # Batch Usage
    #######################################################
    batch_analyze(
        df, 
        nwhl_teams, 
        ['play','faceoff', 'takeaway'], 
        batch_name = 'nwhl'
    )



    

###########################################################
###########################################################
###############                             ###############
###############     SUMMARY STATISTICS      ###############
###############                             ###############
###########################################################
###########################################################

def summarize(pdf, team, stat):
    return summary_stats[stat](team, pdf)


def play(team, pdf):
    stat = 'play'
    play_types = event_types[stat]
    counts = []

    for play in play_types:
        all_plays = pdf.loc[pdf['Event'] == play]
        team_plays = all_plays.loc[all_plays['Team'] == team]
        counts.append(len(team_plays.index))
        
    return {
        "total_plays" : sum(counts),
        "comp_plays" : counts[0],
        "inc_plays" : counts[1],
        "play_comp_perc" : counts[0] / sum(counts)
    }


def faceoff(team, pdf):
    stat = 'faceoff'
    faceoff_type = event_types[stat][0] # only one

    all_faceoffs = pdf.loc[pdf['Event'] == faceoff_type]
    team_faceoffs = all_faceoffs.loc[all_faceoffs['Team'] == team]
    total_faceoffs = len(all_faceoffs.index)
    faceoffs_won = len(team_faceoffs.index)

    return {
        "total_faceoffs" : total_faceoffs,
        "faceoffs_won" : faceoffs_won,
        "faceoff_win_perc" : faceoffs_won / total_faceoffs
    }


def penalty(team, pdf):
    stat = 'penalty'
    penalty_type = event_types[stat][0] # only one

    all_penalties = pdf.loc[pdf['Event'] == penalty_type]
    penalties_for = all_penalties.loc[all_penalties['Team'] != team]
    penalties_against = all_penalties.loc[all_penalties['Team'] == team]

    return {
        'penalties_for' : len(penalties_for.index),
        'penalties_against' : len(penalties_against.index)
    }



def takeaway(team, pdf):
    stat = 'takeaway'
    takeaway_type = event_types[stat][0] # only one

    all_takeaways = pdf.loc[pdf['Event'] == takeaway_type]
    takeaways_for = all_takeaways.loc[all_takeaways['Team'] == team]
    takeaways_against = all_takeaways.loc[all_takeaways['Team'] != team]

    return {
        'takeaways_for' : len(takeaways_for.index),
        'takeaways_against' : len(takeaways_against.index)
    }


def puck_recovery(team, pdf):
    stat = 'puck-recovery'
    recovery_type = event_types[stat][0] # only one

    all_recoveries = pdf.loc[pdf['Event'] == recovery_type]
    recoveries_for = all_recoveries.loc[all_recoveries['Team'] == team]
    recoveries_against = all_recoveries.loc[all_recoveries['Team'] != team]

    return {
        'recoveries_for' : len(recoveries_for.index),
        'recoveries_against' : len(recoveries_against.index)
    }


def dump_in_n_out(team, pdf):
    stat = 'dump-in-n-out'
    dump_in_n_out_type = event_types[stat][0] # only one
    retained = 'Retained'
    lost = 'Lost'

    all_dumps = pdf.loc[pdf['Event'] == dump_in_n_out_type]
    team_dumps = all_dumps.loc[all_dumps['Team'] == team]
    dumps_retained = team_dumps.loc[team_dumps['Detail 1'] == retained]
    dumps_lost = team_dumps.loc[team_dumps['Detail 1'] != lost]

    return {
        'dumps_retained' : len(dumps_retained.index),
        'dumps_lost' : len(dumps_lost.index)
    }  


def zone_entry(team, pdf):
    stat = 'zone-entry'
    zone_entry_type = event_types[stat][0] # only one

    all_zone_entries = pdf.loc[pdf['Event'] == zone_entry_type]
    zone_entries_for = all_zone_entries.loc[all_zone_entries['Team'] == team]
    zone_entries_against = all_zone_entries.loc[all_zone_entries['Team'] != team]

    return {
        'zone_entries_for' : len(zone_entries_for.index),
        'zone_entries_against' : len(zone_entries_against.index)
    }  









###########################################################
###########################################################
###############                             ###############
###############          CONSTANTS          ###############
###############                             ###############
###########################################################
###########################################################

preserve_fields = {
    'play': ['index', 'Event', 'Team'],
    'faceoff' : ['index', 'Event', 'Team'],
    'penalty' : ['index', 'Event', 'Team'],

    'takeaway' : ['index', 'Event', 'Team'],
    'puck-recovery' : ['index', 'Event', 'Team'],
    'dump-in-n-out' : ['index', 'Event', 'Team', 'Detail 1'],
    'zone-entry': ['index', 'Event', 'Team', 'Detail 1', 'X Coordinate', 'Y Coordinate']    
}


event_types = {
    'play': ['Play', 'Incomplete Play'],
    'faceoff' : ['Faceoff Win'],
    'penalty' : ['Penalty Taken'],

    'takeaway' : ['Takeaway'],
    'puck-recovery' : ['Puck Recovery'],
    'dump-in-n-out' : ['Dump In/Out'],
    'zone-entry': ['Zone Entry']
}

summary_stats = {
    'play': play,
    'faceoff' : faceoff,
    'penalty' : penalty,

    'takeaway' : takeaway,
    'puck-recovery' : puck_recovery,
    'dump-in-n-out' : dump_in_n_out,
    'zone-entry': zone_entry
}




# for hackathon_womens.csv
womens_teams = [

    'Olympic (Women) - Canada',
    'Olympic (Women) - United States',
    'Olympic (Women) - Olympic Athletes from Russia',
    'Olympic (Women) - Finland',
    'St. Lawrence Saints',
    'Clarkson Golden Knights'

]



# for hackathon_scouting.csv
scouting_teams = [

    'Sudbury Wolves',
    'Erie Otters',
    'Hamilton Bulldogs',
    'Windsor Spitfires',
    'Saginaw Spirit',
    'Guelph Storm',
    'Niagara Ice Dogs',
    'Mississauga Steelheads',
    'London Knights',
    'Barrie Colts',
    'Oshawa Generals',
    'Sarnia Sting',
    'Sault Ste. Marie Greyhounds',
    'Kitchener Rangers',
    'Kingston Frontenacs',
    "Ottawa 67's",
    'Flint Firebirds',
    'Owen Sound Attack',
    'North Bay Battalion',

]



# for hackathon_nwhl.csv
nwhl_teams = [

    'Boston Pride',
    'Minnesota Whitecaps',
    'Connecticut Whale',
    'Buffalo Beauts',
    'Toronto Six',
    'Metropolitan Riveters'
    
]








###########################################################
###########################################################
###############                             ###############
###############      DATA MANIPULATION      ###############
###############                             ###############
###########################################################
###########################################################

def initialize_data(filename):
    with open(INPUT_DIR + filename, 'r') as csvfile:
        df = pd.read_csv(csvfile, delimiter=',', )

        game_no = []
        indices = []
        curr_game = 1
        last_period = 1
        index = 0
        for curr_period in df['Period']:
            if curr_period == 1 and last_period != 1:
                curr_game += 1
            last_period = curr_period
            game_no.append(curr_game)
            indices.append(index)
            index += 1

        df['game'] = game_no
        df['index'] = indices
        return df



def extract(df, team_name, headers, opposing=None, game_no=None, fn=OUTPUT_DIR+'test.csv', record=True):
    raw = df.copy()
    whole_season = raw.loc[raw['Home Team'] == team_name]
    whole_season = whole_season.append(raw.loc[raw['Away Team'] == team_name])
    if type(opposing) == str:
        opposing = [opposing]
    if type(game_no) == int:
        game_no = [game_no]
    

    processing = pd.DataFrame(columns = raw.columns)
    if opposing:
        for o in opposing:
            processing = processing.append(whole_season.loc[whole_season['Away Team'] == o])
            processing = processing.append(whole_season.loc[whole_season['Home Team'] == o])
   
    if game_no:
        for g in game_no:
            processing = processing.append(whole_season.loc[whole_season['game'] == g])   
        
    comparison = processing.drop_duplicates(subset = ['index'], keep = False).filter(items = headers)
    if comparison.empty:
        comparison = whole_season.filter(items = headers)

    processed = pd.merge(whole_season, comparison, how = 'right').filter(items = headers)
    if record:
        processed.to_csv(fn, quoting=csv.QUOTE_ALL)
    return processed




def batch_analyze(df, batch, stats, fields_of_interest=[], batch_name='batch', record=True):
    batch_name = './' + batch_name + '/'
    stats_fn = 'stats.csv'

    # for singular analysis
    if type(stats) == str:
        stats = [stats]

    # get super set of headers
    super_headers = []
    for stat in stats:
        super_headers.extend(preserve_fields[stat].copy())
    foi = list(set(super_headers + fields_of_interest)) 


    batch_stats = {}
    batch_stats_headers = []
    intermediates = pd.DataFrame(columns = df.columns)
    
    batch_path = OUTPUT_DIR + BATCH_DIR + batch_name
    batch_path_tmp = batch_path + TMP_DIR
    make_path(batch_path_tmp)
    for team in batch:
        sum_stats = {}
        r = True and record
        for stat in stats:
            processed = extract(df, team, foi, fn = f'{batch_path_tmp}{team}-{stat}', record=r)
            sum_stats.update(summarize(processed, team, stat))
            batch_stats_headers.extend(list(sum_stats.keys()))
            r = False
        batch_stats.update({team : sum_stats})

    with open(batch_path + stats_fn, 'w') as statsfile:
        writer = csv.DictWriter(statsfile, fieldnames = ['team'] + list(set(batch_stats_headers)))
        writer.writeheader()
        for team, stats in batch_stats.items():
            stats.update({'team' : team})
            writer.writerow(stats)
  
    


def make_path(path):
    os.makedirs(path, exist_ok=True)



if __name__ == '__main__':
    main()