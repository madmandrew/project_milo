import pandas
from pymongo import MongoClient
from sklearn import cross_validation
from sklearn import svm                                        # SVM
from sklearn.tree import DecisionTreeClassifier                # Decision Tree
from sklearn.neighbors import KNeighborsClassifier             # KNN
from sklearn.neural_network import MLPClassifier               # Neural Network
from sklearn.ensemble import AdaBoostClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.ensemble import RandomForestClassifier

import inspect
from sklearn.utils.testing import all_estimators

class EnsembleLearning(object):
    def __init__(self, ada_boost=False, bagging=False, random_forests=False, neural_network=False):
        self.team_name_lookup = self.get_team_name_lookup()
        self.predict_year = '2016'
        training_features, training_targets = self.get_data()

        if ada_boost:
            print("Ada Boost: ", end="")
            self.ada_boost_train(training_features, training_targets)
            self.predict(ada_boost=True)
        if bagging:
            print("Bagging: ", end="")
            self.bagging_train(training_features, training_targets)
            self.predict(bagging=True)
        if random_forests:
            print("Random Forests: ", end="")
            self.random_forest_train(training_features, training_targets)
            self.predict(random_forests=True)
        if neural_network:
            print("Neural Network: ", end="")
            self.neural_network_train(training_features, training_targets)
            self.predict(neural_network=True)



    def neural_network_train(self, X, Y):
        network = MLPClassifier(hidden_layer_sizes=[16, 16, 16, 2], activation='logistic', solver='lbfgs', alpha=1e-05,
                      learning_rate_init=0.001, max_iter=1300, random_state=1)

        self.neural_network = network.fit(X, Y)

    def random_forest_train(self, X, Y):

        forest = RandomForestClassifier(n_estimators=1000, max_features=3)

        self.random_forest = forest.fit(X, Y)

    def bagging_train(self, X, Y):

        # Default is Decision Tree
        # bagging = BaggingClassifier()

        # Neural Network
        bagging = BaggingClassifier(MLPClassifier(hidden_layer_sizes=[50, 2], activation='logistic', solver='lbfgs', alpha=1e-05,
                                       learning_rate_init=0.0001, max_iter=200, random_state=1))

        # SVC
        # bagging =  BaggingClassifier(svm.SVC())

        self.bagging = bagging.fit(X, Y)

    def ada_boost_train(self, X, Y):

        # Default is Decision Tree
        # bdt = AdaBoostClassifier(algorithm="SAMME", n_estimators=200)

        # SVM
        bdt = AdaBoostClassifier(svm.SVC(), algorithm="SAMME", n_estimators=200)

        self.ada_boost = bdt.fit(X, Y)

    def predict(self, ada_boost=False, bagging=False, random_forests=False, neural_network=False):
        if ada_boost:
            algorithm = self.ada_boost
        if bagging:
            algorithm = self.bagging
        if random_forests:
            algorithm = self.random_forest
        if neural_network:
            algorithm = self.neural_network

        testing_features, testing_targets = self.get_data(training_data=False)

        num_correct = 0
        for index, guess in enumerate(algorithm.predict(testing_features)):
            if guess == testing_targets[index]:
                num_correct += 1

        print(num_correct / len(testing_targets))

    def get_data(self, training_data=True):

        if training_data:
            years = ['2011', '2012', '2013', '2014', '2015']
        else:
            years = ['2016']

        client = MongoClient('localhost:27017')
        db = client.march_madness

        training_features = []
        training_targets = []

        for year in years:
            # For each match in march madness of the given year (find all the teams that played in the tournament that year)
            for match in db.tournament_stats.find({'Bracket Year': year}):
                team_one_name = self.team_name_lookup[match['Team 1']] if match['Team 1'] in self.team_name_lookup else \
                match['Team 1']
                team_two_name = self.team_name_lookup[match['Team 2']] if match['Team 2'] in self.team_name_lookup else \
                match['Team 2']

                # Grab the regular season stats of the two teams that played each other
                team_one_stats = db.reg_season_stats.find_one({'Year': year, "Team": team_one_name})
                team_two_stats = db.reg_season_stats.find_one({'Year': year, "Team": team_two_name})

                # Order the attributes by sticking it into an array. Map winner to team one or team two (0 or 1)
                training_feature, training_target = self.convert_and_order_data((team_one_stats, team_two_stats), match['Winner'])

                # Add them to the data (the two team's stats and who won
                training_features.append(training_feature)
                training_targets.append(training_target)

        return training_features, training_targets

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
    def convert_and_order_data(self, feature, target):
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

if __name__ == "__main__":
    print("Starting Ensemble Learning")

    EnsembleLearning(ada_boost=True, bagging=True, random_forests=True, neural_network=True)
