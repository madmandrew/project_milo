from sklearn.neural_network import MLPClassifier
from pymongo import MongoClient

def get_training_data(year):
    # Connect to db
    client = MongoClient('localhost:27017')
    db = client.march_madness

    training_features = []
    training_targets = []

    for match in db.tournament_stats.find({'Bracket Year': year}):
        team_one = db.reg_season_stats.find_one({'Year': year, "Team": match['Team 1']})
        team_two = db.reg_season_stats.find_one({'Year': year, "Team": match['Team 2']})

        if (team_one is not None and team_two is not None):
            training_features.append(team_one)
            training_features.append(team_two)
            training_targets.append(match['Winner'])

        #PROBLEM!!! How does the NN know what attributes go with which school?

def train_neural_network():

    training_years = ['2011'] #, '2012', '2013', '2014', '2015', '2016']

    for year in training_years:
        get_training_data(year)


    # Create the neural network
    # http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
    neural_network = MLPClassifier(hidden_layer_sizes=(5, 2), activation='logistic', solver='lbfgs', alpha=1e-05, learning_rate_init=0.001,
                  random_state=1)

    # Train the neural Network
    #neural_network.fit([],[])

if __name__ == "__main__":
    print("Starting Neural Network")
    train_neural_network()
