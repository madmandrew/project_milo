from sklearn.neural_network import MLPClassifier
from pymongo import MongoClient
import random

class MadnessPredictor(object):
    def __init__(self, layers):
        # Create the neural network
        # http://scikit-learn.org/stable/modules/generated/sklearn.neural_network.MLPClassifier.html#sklearn.neural_network.MLPClassifier
        self.neural_network = MLPClassifier(hidden_layer_sizes=(layers), activation='logistic', solver='lbfgs', alpha=1e-05,
                                       learning_rate_init=0.001,
                                       random_state=1, max_iter=1300)
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

        match_results = {}
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
                    match_results[match['Match Number']] = match['Winner']

        return training_features, training_targets, match_results

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
            training_features, training_targets, match_results = self.get_training_data(year, isTestData=False)

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

    def display_bracket(self, match_results, champion):
        lines = [""] * 32 * 3

        padding = 15
        round_index = [0, 1, 3, 6, 12, 24]
        for matchNumber in range(1, 64):
            if matchNumber < 33:
                index = round_index[0]
                lines[index] = match_results[matchNumber][0].ljust(padding, '-')
                lines[index + 1] = "{}|".format(" " * padding)
                lines[index + 2] = match_results[matchNumber][1].ljust(padding, '-')
                round_index[0] += 3
            if matchNumber > 32 and matchNumber < 49:
                index = round_index[1]
                lines[index] += match_results[matchNumber][0].ljust(padding, '-')
                lines[index + 1] += "{}|".format(" " * padding)
                lines[index + 2] += "{}|".format(" " * padding)
                lines[index + 3] += match_results[matchNumber][1].ljust(padding, '-')
                if matchNumber != 48:
                    lines[index + 4] += "{}".format(" " * padding)
                    lines[index + 5] += "{}".format(" " * padding)
                round_index[1] += 6
            if matchNumber > 48 and matchNumber < 57:
                index = round_index[2]
                lines[index] += match_results[matchNumber][0].ljust(padding, '-')
                for i in range(1, 6):
                    lines[index + i] += "{}|".format(" " * padding)
                lines[index + 6] += match_results[matchNumber][1].ljust(padding, '-')
                if matchNumber != 56:
                    for i in range(7, 12):
                        lines[index + i] += "{}".format(" " * padding)
                round_index[2] += 12
            if matchNumber > 56 and matchNumber < 61:
                index = round_index[3]
                lines[index] += match_results[matchNumber][0].ljust(padding, '-')
                for i in range(1, 12):
                    lines[index + i] += "{}|".format(" " * padding)
                lines[index + 12] += match_results[matchNumber][1].ljust(padding, '-')
                if matchNumber != 60:
                    for i in range(13, 24):
                        lines[index + i] += "{}".format(" " * padding)
                round_index[3] += 24
            if matchNumber > 60 and matchNumber < 63:
                index = round_index[4]
                lines[index] += match_results[matchNumber][0].ljust(padding, '-')
                for i in range(1, 21):
                    lines[index + i] += "{}|".format(" " * padding)
                lines[index + 24] += match_results[matchNumber][1].ljust(padding, '-')
                if matchNumber != 62:
                    for i in range(25, 48):
                        lines[index + i] += "{}".format(" " * padding)
                round_index[4] += 48
            if matchNumber == 63:
                lines[22] += match_results[matchNumber][0].ljust(padding, '-')
                for i in range(1, 48):
                    lines[22 + i] += "{}|".format(" " * padding)
                lines[71] += match_results[matchNumber][1].ljust(padding, '-')

        lines[43] += "---{}".format(champion)
        for line in lines:
            print(line)

    # training_features, training_targets
    def get_next_round_matches(self, bracket_year, round_number, match_results):
        # TODO make connection in object so we dont keep reconnecting
        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []

        matchNumbers = [1, 33, 49, 57, 61, 63, 64]
        previous_match_number = matchNumbers[round_number - 2]
        for currentMatchNumber in range(matchNumbers[round_number - 1], matchNumbers[round_number]):
            team_name_1 = match_results[str(previous_match_number)]
            previous_match_number += 1
            team_name_2 = match_results[str(previous_match_number)]
            previous_match_number += 1

            team_1 = db.reg_season_stats.find_one({'Year': bracket_year, "Team": team_name_1})
            team_2 = db.reg_season_stats.find_one({'Year': bracket_year, "Team": team_name_2})

            if team_1 is None:
                print("Error: {} missing".format(team_name_1))
            if team_2 is None:
                print("Error: {} missing".format(team_name_2))

            match_up = (team_1, team_2)
            training_features.append(match_up)

        return training_features

    def get_nn_inputs(self, training_features, training_targets):
        nn_inputs = []
        for index, match_up in enumerate(training_features):
            feature, target = self.convert_and_order_data(match_up, training_targets[index])
            # Set it to send to the neural network
            nn_inputs.append(feature)
        return nn_inputs

    def predict_year(self, year, print_team_names):
        training_features, training_targets, match_results = self.get_training_data(year, isTestData=True)
        validation_features, validation_targets, match_results = self.get_training_data(year, isTestData=False)

        nn_inputs = self.get_nn_inputs(training_features, training_targets)
        cbs_score_index = [1, 2, 4, 8, 16, 32]
        cbs_score = 0
        espn_score_index = [10, 20, 40, 80, 160, 320]
        espn_score = 0
        correct = 0
        match_index = 1
        predicted_results = {}
        all_results_for_display = {}
        champion = None
        # this will go through rounds 1-6 and do predictions
        for round_number in range(1, 7):
            predictions = self.neural_network.predict(nn_inputs)
            round_correct = 0
            round_total = len(predictions)

            for index, result in enumerate(predictions):
                # TODO I could just use the team data here... rather then hitting DB again oops
                predictedWinnerName = training_features[index][result]['Team']
                all_results_for_display[match_index] = [training_features[index][0]['Team'], training_features[index][1]['Team']]
                predicted_results[str(match_index)] = predictedWinnerName

                if round_number == 6:
                    champion = predictedWinnerName

                actualWinnerName = match_results[str(match_index)]
                match_index += 1

                if actualWinnerName in self.team_name_lookup:
                    actualWinnerName = self.team_name_lookup[actualWinnerName]

                prediction_result = "--"
                if predictedWinnerName == actualWinnerName:
                    cbs_score += cbs_score_index[round_number - 1]
                    espn_score += espn_score_index[round_number - 1]
                    correct += 1
                    round_correct += 1
                    prediction_result = "++"

                if (print_team_names):
                    print("{}, {}, Predicted: {} | Actual {}".format(result, prediction_result, predictedWinnerName, actualWinnerName))

            if (print_team_names):
                print("\nRound {} Accuracy {}/{} | {}%\n".format(round_number, round_correct, round_total, (round_correct / round_total) * 100))
            else:
                print("Round {} Accuracy {}/{} | {}%".format(round_number, round_correct, round_total, (round_correct / round_total) * 100))

            if round_number != 6:
                training_features = self.get_next_round_matches(bracket_year=year, round_number=(round_number + 1), match_results=predicted_results)
                nn_inputs = self.get_nn_inputs(training_features, validation_targets)

        overall_accuracy = (correct / 63) * 100
        print("Overall Accuracy {}/{} | {}%".format(correct, 63, overall_accuracy))
        print("CBS score: {}".format(cbs_score))
        print("ESPN score: {}".format(espn_score))
        self.display_bracket(all_results_for_display, champion)
        return overall_accuracy, espn_score


def programmatic_layer_checker():
    accuracy = 0
    best_accuracy_layers = None
    best_espn_score = 0
    best_espn_layers = None
    for i in range(2, 8):
        for j in range(2, 21):
            layers = [j]*i
            layers.append(2)
            madnessPredictor = MadnessPredictor(layers)
            tempAccuracy, tempEspnScore = madnessPredictor.predict_year('2016', print_team_names=False)
            print("{} accuracy = {}%".format(layers, (tempAccuracy)))
            if (tempAccuracy > accuracy):
                accuracy = tempAccuracy
                best_accuracy_layers = layers
            if (tempEspnScore > best_espn_score):
                best_espn_score = tempEspnScore
                best_espn_layers = layers

    # for iteration in range(1, 50):
    #     for i in range(3, 8):
    #         layers = []
    #         for j in range(1, i):
    #             layers.append(random.randint(1, 20))
    #         layers.append(2)
    #         madnessPredictor = MadnessPredictor(layers)
    #         tempAccuracy, tempEspnScore = madnessPredictor.predict_year('2016', print_team_names=False)
    #         if (tempAccuracy > accuracy):
    #             accuracy = tempAccuracy
    #             best_accuracy_layers = layers
    #         if (tempEspnScore > best_espn_score):
    #             best_espn_score = tempEspnScore
    #             best_espn_layers = layers

    print("Best accuracy: {} | Layers = {}".format(accuracy, best_accuracy_layers))
    print("Best ESPN Score: {} | Layers = {}".format(best_espn_score, best_espn_layers))


if __name__ == "__main__":
    print("Starting Neural Network")
    madnessPredictor = MadnessPredictor([8, 15, 2])
    madnessPredictor.predict_year('2016', print_team_names=True)
    #programmatic_layer_checker()
