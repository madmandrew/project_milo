from sklearn.neural_network import MLPClassifier
from pymongo import MongoClient
import random

class MadnessPredictor(object):
    def __init__(self, layers):
        # Create the neural network
        # http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
        self.neural_network = MLPClassifier(hidden_layer_sizes=(layers), activation='logistic', solver='lbfgs', alpha=1e-05,
                                       learning_rate_init=0.001,
                                       random_state=1)
        self.team_name_lookup = self.get_team_name_lookup()
        self.train_neural_network()

    def get_team_name_lookup(self):
        teamNameMap = {"N Colorado": "Northern Colorado", "Boston Univ": "Boston College", "VA Commonwealth": "VCU",
                       "St Peter's": "Saint Peter's", "St John's": "St. John's", "BYU": "Brigham Young",
                       "Santa Barbara": "UC Santa Barbara", "WKU": "Western Kentucky", "S Dakota St": "South Dakota",
                       "St Louis": "Saint Louis", "Southern Miss": "Southern Mississippi",
                       "St Bonaventure": "St. Bonaventure", "Loyola MD": "Loyola Marymount",
                       "NC State": "North Carolina",
                       "St Mary's CA": "Saint Mary's", "NC A&T": "North Carolina A&T", "Albany NY": "Albany",
                       "Miami FL": "Miami (FL)", "Southern Univ": "Southern", "Mississippi": "Mississippi State",
                       "Northwestern LA": "Northwestern State", "FL Gulf Coast": "Florida Gulf Coast",
                       "SF Austin": "Stephen F. Austin", "W Michigan": "Western Michigan",
                       "E Kentucky": "Eastern Kentucky",
                       "Coastal Car": "Coastal Carolina", "G Washington": "George Washington",
                       "NC Central": "North Carolina Central", "St Joseph's PA": "Saint Joseph's",
                       "WI Milwaukee": "Milwaukee", "N Dakota St": "North Dakota State", "ULL": "Louisiana-Lafayette ",
                       "American Univ": "American University", "Cal Poly SLO": "Cal Poly",
                       "TX Southern": "Texas Southern",
                       "E Washington": "Eastern Washington", "SMU": "Southern Methodist", "WI Green Bay": "Green Bay",
                       "CS Bakersfield": "Cal State Bakersfield", "Ark Little Rock": "Little Rock",
                       "MTSU": "Middle Tennessee State", "UT San Antonio": "Texas-San Antonio",
                       "Indiana St": "Indiana State", "San Diego St": "San Diego State", "Penn St": "Penn State",
                       "Morehead St": "Morehead State", "Florida St": "Florida State", "Kansas St": "Kansas State",
                       "Utah St": "Utah State", "Michigan St": "Michigan State", "Iowa St": "Iowa State",
                       "Wichita St": "Wichita State", "New Mexico St": "New Mexico State",
                       "Long Beach St": "Long Beach State", "Murray St": "Murray State",
                       "Colorado St": "Colorado State",
                       "Norfolk St": "Norfolk State", "Ohio St": "Ohio State", "Oklahoma St": "Oklahoma State",
                       "Weber St": "Weber State", "Arizona St": "Arizona State", "Georgia St": "Georgia State",
                       "Oregon St": "Oregon State", "Fresno St": "Fresno State"}
        return teamNameMap

    def get_training_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year})
        """Pull data from the db and creates training features based on match ups"""


        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (not isTestData or int(match['Match Number']) < 33):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def get_second_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year, 'Round Number': '2'})
        """Pull data from the db and creates training features based on match ups"""



        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (int(match['Match Number']) < 49 and int(match['Match Number']) > 32):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def get_third_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year, 'Round Number': '3'})
        """Pull data from the db and creates training features based on match ups"""



        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (int(match['Match Number']) < 57 and int(match['Match Number']) > 48):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def get_fourth_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year, 'Round Number': '4'})
        """Pull data from the db and creates training features based on match ups"""



        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (int(match['Match Number']) < 61 and int(match['Match Number']) > 56):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def get_fifth_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year, 'Round Number': '5'})
        """Pull data from the db and creates training features based on match ups"""



        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (int(match['Match Number']) < 63 and int(match['Match Number']) > 60):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def get_sixth_data(self, year, isTestData):

        # Connect to db
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []


        temp = db.tournament_stats.find({'Bracket Year': year, 'Round Number': '5'})
        """Pull data from the db and creates training features based on match ups"""



        # For each match in march madness of the given year (find all the teams that played in the tournament that year)
        for match in db.tournament_stats.find({'Bracket Year': year}):
            # if its training data we only grab first round matches
            if (int(match['Match Number']) < 64 and int(match['Match Number']) > 62):

                team_name_one = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else match['Team 1']
                team_name_two = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else match['Team 2']

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

    def convert_and_order_data(self, feature, target):
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

    def train_neural_network(self):

        training_years = ['2011', '2012', '2013', '2014', '2015']

        for year in training_years:
            training_features, training_targets = self.get_training_data(year, isTestData=False)

            nn_inputs = []
            nn_targets = []

            # For each match-up
            for index, match_up in enumerate(training_features):
                # Format the data for the Neural Network
                feature, target = self.convert_and_order_data(match_up, training_targets[index])
                # Set it to send to the neural network
                nn_inputs.append(feature)
                nn_targets.append(target)

            # Train the neural Network
            self.neural_network.fit(nn_inputs, nn_targets)

    def predict_year(self, year, print_team_names):

        training_features, training_targets = self.get_training_data(year, isTestData=True)

        validation_features, validation_targets = self.get_training_data(year, isTestData=False)

        nn_inputs = []
        for index, match_up in enumerate(training_features):
            feature, target = self.convert_and_order_data(match_up, training_targets[index])
            # Set it to send to the neural network
            nn_inputs.append(feature)
            #winnerIndex = self.neural_network.predict(feature)[0]
            #winnerName = match_up[winnerIndex]['Team']
            #print("Predicted: {} | Actual: {}".format(winnerName, training_targets[index]))
        print("\n          training_features                 \n")
        for temp in training_features:
            print(temp)
        print("\n          NN_inputs                 \n")
        for temp in nn_inputs:
            print(temp)

        ########## Round One ##########

        round_one_results = self.neural_network.predict(nn_inputs)
        correct = 0
        total = len(round_one_results)

        print("\n Round One \n")

        for index, result in enumerate(round_one_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index, " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index, " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))

        ########## Round Two ##########

        round_two = []

        tempList = []
        for i, winner in enumerate(round_one_results):
            temp = []
            if (winner == 0):
                temp = nn_inputs[i][:20]
            else:
                temp = nn_inputs[i][20:]

            for list in temp:
                tempList.append(list)

            if (i % 2 == 1):
                round_two.append(tempList)
                tempList = []

        round_two_results = self.neural_network.predict(round_two)
        training_features, training_targets = self.get_second_data(year, isTestData=True)

        print("\n Round Two \n")

        for index, result in enumerate(round_two_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index, " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index, " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))


        ########## Round Three ##########

        round_three = []

        for i, winner in enumerate(round_two_results):
            temp = []
            if (winner == 0):
                temp = round_two[i][:20]
            else:
                temp = round_two[i][20:]

            for list in temp:
                tempList.append(list)

            if (i % 2 == 1):
                round_three.append(tempList)
                tempList = []

        round_three_results = self.neural_network.predict(round_three)
        training_features, training_targets = self.get_third_data(year, isTestData=True)

        print("\n Round Three \n")

        for index, result in enumerate(round_three_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index,
                      " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index,
                      " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))

        ########## Round Four ##########

        round_four = []

        for i, winner in enumerate(round_three_results):
            temp = []
            if (winner == 0):
                temp = round_three[i][:20]
            else:
                temp = round_three[i][20:]

            for list in temp:
                tempList.append(list)

            if (i % 2 == 1):
                round_four.append(tempList)
                tempList = []

        round_four_results = self.neural_network.predict(round_four)
        training_features, training_targets = self.get_fourth_data(year, isTestData=True)

        print("\n Round Four \n")

        for index, result in enumerate(round_four_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index,
                      " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index,
                      " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))

        ########## Round Five ##########

        round_five = []

        for i, winner in enumerate(round_four_results):
            temp = []
            if (winner == 0):
                temp = round_four[i][:20]
            else:
                temp = round_four[i][20:]

            for list in temp:
                tempList.append(list)

            if (i % 2 == 1):
                round_five.append(tempList)
                tempList = []

        round_five_results = self.neural_network.predict(round_five)
        training_features, training_targets = self.get_fifth_data(year, isTestData=True)

        print("\n Round Five \n")

        for index, result in enumerate(round_five_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index,
                      " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index,
                      " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))

        ########## Round Six ##########

        round_six = []

        for i, winner in enumerate(round_five_results):
            temp = []
            if (winner == 0):
                temp = round_five[i][:20]
            else:
                temp = round_five[i][20:]

            for list in temp:
                tempList.append(list)

            if (i % 2 == 1):
                round_six.append(tempList)
                tempList = []

        round_six_results = self.neural_network.predict(round_six)
        training_features, training_targets = self.get_sixth_data(year, isTestData=True)

        print("\n Round Six \n")

        for index, result in enumerate(round_six_results):
            predictedWinnerName = training_features[index][result]['Team']
            actualWinnerName = training_targets[index]
            if actualWinnerName in self.team_name_lookup:
                actualWinnerName = self.team_name_lookup[actualWinnerName]

            if (print_team_names):
                pass
                # print("Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            if predictedWinnerName == actualWinnerName:
                correct += 1
                print(index,
                      " correct... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))
            else:
                print(index,
                      " wrong... Predicted: {} | Actual: {}".format(predictedWinnerName, actualWinnerName))



        total = len(round_one_results) + len(round_two_results) + len(round_three_results) + len(round_four_results) + len(round_five_results)+ len(round_six_results)
        print("{} / {} correct {}%".format(correct, total, (correct / total) * 100))
        return (correct / total)


def programmatic_layer_checker():
    accuracy = 0
    bestLayers = None
    # for i in range(2, 8):
    #     for j in range(2, 21):
    #         layers = [j]*i
    #         layers.append(2)
    #         madnessPredictor = MadnessPredictor(layers)
    #         tempAccuracy = madnessPredictor.predict_year('2016')
    #         print("{} accuracy = {}%".format(layers, (tempAccuracy * 100)))
    #         if (tempAccuracy > accuracy):
    #             accuracy = tempAccuracy
    #             bestLayers = layers

    for iteration in range(1, 50):
        for i in range(3, 8):
            layers = []
            for j in range(1, i):
                layers.append(random.randint(1, 20))
            layers.append(2)
            madnessPredictor = MadnessPredictor(layers)
            tempAccuracy = madnessPredictor.predict_year('2016', print_team_names=False)
            print("{} accuracy = {}%".format(layers, (tempAccuracy * 100)))
            if (tempAccuracy > accuracy):
                accuracy = tempAccuracy
                bestLayers = layers

    print("Best accuracy: {} | Layers = {}".format(accuracy, bestLayers))

if __name__ == "__main__":
    print("Starting Neural Network")
    madnessPredictor = MadnessPredictor([16, 16, 16, 2])
    madnessPredictor.predict_year('2016', print_team_names=True)
    #programmatic_layer_checker()
