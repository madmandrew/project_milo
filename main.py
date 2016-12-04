from sklearn.neural_network import MLPClassifier
from pymongo import MongoClient

def get_team_name_lookup():
    teamNameMap = {"N Colorado": "Northern Colorado", "Boston Univ": "Boston College", "VA Commonwealth": "VCU",
                   "St Peter's": "Saint Peter's", "St John's": "St. John's", "BYU": "Brigham Young",
                   "Santa Barbara": "UC Santa Barbara", "WKU": "Western Kentucky", "S Dakota St": "South Dakota",
                   "St Louis": "Saint Louis", "Southern Miss": "Southern Mississippi",
                   "St Bonaventure": "St. Bonaventure", "Loyola MD": "Loyola Marymount", "NC State": "North Carolina",
                   "St Mary's CA": "Saint Mary's", "NC A&T": "North Carolina A&T", "Albany NY": "Albany",
                   "Miami FL": "Miami (FL)", "Southern Univ": "Southern", "Mississippi": "Mississippi State",
                   "Northwestern LA": "Northwestern State", "FL Gulf Coast": "Florida Gulf Coast",
                   "SF Austin": "Stephen F. Austin", "W Michigan": "Western Michigan", "E Kentucky": "Eastern Kentucky",
                   "Coastal Car": "Coastal Carolina", "G Washington": "George Washington",
                   "NC Central": "North Carolina Central", "St Joseph's PA": "Saint Joseph's",
                   "WI Milwaukee": "Milwaukee", "N Dakota St": "North Dakota State", "ULL": "Louisiana-Lafayette ",
                   "American Univ": "American University", "Cal Poly SLO": "Cal Poly", "TX Southern": "Texas Southern",
                   "E Washington": "Eastern Washington", "SMU": "Southern Methodist", "WI Green Bay": "Green Bay",
                   "CS Bakersfield": "Cal State Bakersfield", "Ark Little Rock": "Little Rock",
                   "MTSU": "Middle Tennessee State", "UT San Antonio": "Texas-San Antonio",
                   "Indiana St": "Indiana State", "San Diego St": "San Diego State", "Penn St": "Penn State",
                   "Morehead St": "Morehead State", "Florida St": "Florida State", "Kansas St": "Kansas State",
                   "Utah St": "Utah State", "Michigan St": "Michigan State", "Iowa St": "Iowa State",
                   "Wichita St": "Wichita State", "New Mexico St": "New Mexico State",
                   "Long Beach St": "Long Beach State", "Murray St": "Murray State", "Colorado St": "Colorado State",
                   "Norfolk St": "Norfolk State", "Ohio St": "Ohio State", "Oklahoma St": "Oklahoma State",
                   "Weber St": "Weber State", "Arizona St": "Arizona State", "Georgia St": "Georgia State",
                   "Oregon St": "Oregon State", "Fresno St": "Fresno State"}
    return teamNameMap

def get_training_data(year, isTestData):
    """Pull data from the db and creates training features based on match ups"""
    teamNameLookup = get_team_name_lookup()

    # Connect to db
    client = MongoClient('localhost:27017')
    db = client.march_madness

    training_features = []
    training_targets = []

    # For each match in march madness of the given year (find all the teams that played in the tournament that year)
    for match in db.tournament_stats.find({'Bracket Year': year}):
        # if its training data we only grab first round matches
        if (not isTestData or int(match['Match Number']) < 33):

            team_name_one = teamNameLookup[match['Team 1']] if match['Team 1'] in teamNameLookup else match['Team 1']
            team_name_two = teamNameLookup[match['Team 2']] if match['Team 2'] in teamNameLookup else match['Team 2']

            # Grab the regular season stats of the two teams that played each other
            team_one = db.reg_season_stats.find_one({'Year': year, "Team": team_name_one})
            team_two = db.reg_season_stats.find_one({'Year': year, "Team": team_name_two})

            if team_one is None:
                print(match['Team 1'])
            if team_two is None:
                print(match['Team 2'])

            # Make sure they were actually playing each other that round
            if (team_one is not None and team_two is not None):
                # Add them to the data (the two team's stats and who won
                match_up = (team_one, team_two)
                training_features.append(match_up)
                training_targets.append(match['Winner'])

    return training_features, training_targets

def convert_and_order_data(feature, target):
    """
    This method orders the teams data to make sure inputs are consistent (since documents/dictionaries are unordered

    Also change winning team to a 0 or 1
    """
    input = []

    if(target == feature[0]["Team"]):
        target = 0
    else:
        target = 1

    input.append(float(feature[0]['PPG']))
    input.append(float(feature[0]['GP']))
    input.append(float(feature[0]['MPG']))
    input.append(float(feature[0]['FGM']))
    input.append(float(feature[0]['FGA']))
    input.append(float(feature[0]['FG%']))
    input.append(float(feature[0]['3PM']))
    input.append(float(feature[0]['3PA']))
    input.append(float(feature[0]['3P%']))
    input.append(float(feature[0]['FTM']))
    input.append(float(feature[0]['FTA']))
    input.append(float(feature[0]['FT%']))
    input.append(float(feature[0]['TOV']))
    input.append(float(feature[0]['PF']))
    input.append(float(feature[0]['ORB']))
    input.append(float(feature[0]['DRB']))
    input.append(float(feature[0]['RPG']))
    input.append(float(feature[0]['APG']))
    input.append(float(feature[0]['SPG']))
    input.append(float(feature[0]['BPG']))

    input.append(float(feature[1]['PPG']))
    input.append(float(feature[1]['GP']))
    input.append(float(feature[1]['MPG']))
    input.append(float(feature[1]['FGM']))
    input.append(float(feature[1]['FGA']))
    input.append(float(feature[1]['FG%']))
    input.append(float(feature[1]['3PM']))
    input.append(float(feature[1]['3PA']))
    input.append(float(feature[1]['3P%']))
    input.append(float(feature[1]['FTM']))
    input.append(float(feature[1]['FTA']))
    input.append(float(feature[1]['FT%']))
    input.append(float(feature[1]['TOV']))
    input.append(float(feature[1]['PF']))
    input.append(float(feature[1]['ORB']))
    input.append(float(feature[1]['DRB']))
    input.append(float(feature[1]['RPG']))
    input.append(float(feature[1]['APG']))
    input.append(float(feature[1]['SPG']))
    input.append(float(feature[1]['BPG']))

    return input, target

def train_neural_network():

    training_years = ['2011', '2012', '2013', '2014', '2015']

    # Create the neural network
    # http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
    neural_network = MLPClassifier(hidden_layer_sizes=(10, 2), activation='logistic', solver='lbfgs', alpha=1e-05,
                                   learning_rate_init=0.001,
                                   random_state=1)

    for year in training_years:
        training_features, training_targets = get_training_data(year, isTestData=False)

        nn_inputs = []
        nn_targets = []

        # For each match-up
        for index, match_up in enumerate(training_features):
            # Format the data for the Neural Network
            feature, target = convert_and_order_data(match_up, training_targets[index])
            # Set it to send to the neural network
            nn_inputs.append(feature)
            nn_targets.append(target)

        # Train the neural Network
        neural_network.fit(nn_inputs, nn_targets)

def predict():
    training_features, training_targets = get_training_data('2016', isTestData=True)

    print("TEST")


if __name__ == "__main__":
    print("Starting Neural Network")
    train_neural_network()
    predict()
