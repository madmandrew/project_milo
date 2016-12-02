from sklearn.neural_network import MLPClassifier
from pymongo import MongoClient

def get_training_data(year):
    """Pull data from the db and creates training features based on match ups"""

    # Connect to db
    client = MongoClient('localhost:27017')
    db = client.march_madness

    training_features = []
    training_targets = []

    # For each match in march madness of the given year (find all the teams that played in the tournament that year)
    for match in db.tournament_stats.find({'Bracket Year': year}):
        # Grab the regular season stats of the two teams that played each other
        team_one = db.reg_season_stats.find_one({'Year': year, "Team": match['Team 1']})
        team_two = db.reg_season_stats.find_one({'Year': year, "Team": match['Team 2']})

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

    training_years = ['2011', '2012', '2013', '2014', '2015', '2016']

    # Create the neural network
    # http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
    neural_network = MLPClassifier(hidden_layer_sizes=(10, 2), activation='logistic', solver='lbfgs', alpha=1e-05,
                                   learning_rate_init=0.001,
                                   random_state=1)

    for year in training_years:
        training_features, training_targets = get_training_data(year)

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

if __name__ == "__main__":
    print("Starting Neural Network")
    train_neural_network()
