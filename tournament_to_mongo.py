from pymongo import MongoClient
import csv


def connect_to_db():
    client = MongoClient('localhost:27017')
    db = client.march_madness
    return db


def read_tournament_stats_to_db(db):

    csv_files = ['./csv_files/bracket_results/2010_bracket_results.csv',
                 './csv_files/bracket_results/2011_bracket_results.csv',
                 './csv_files/bracket_results/2012_bracket_results.csv',
                 './csv_files/bracket_results/2013_bracket_results.csv',
                 './csv_files/bracket_results/2014_bracket_results.csv',
                 './csv_files/bracket_results/2015_bracket_results.csv',
                 './csv_files/bracket_results/2016_bracket_results.csv']

    for file in csv_files:
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile)
            for document in reader:
                # Does this document already exist?
                if db.tournament_stats.find_one({"Year": file[28:32], "Team1": document["Team1"]}) == None:
                    db.tournament_stats.insert(document)

if __name__ == "__main__":
    db = connect_to_db()
    read_tournament_stats_to_db(db)