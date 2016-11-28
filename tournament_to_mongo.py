"""Run this file to insert the tournament data into the database"""

from pymongo import MongoClient
import csv

csv_files = ['./csv_files/bracket_results/2010_bracket_results.csv',
             './csv_files/bracket_results/2011_bracket_results.csv',
             './csv_files/bracket_results/2012_bracket_results.csv',
             './csv_files/bracket_results/2013_bracket_results.csv',
             './csv_files/bracket_results/2014_bracket_results.csv',
             './csv_files/bracket_results/2015_bracket_results.csv',
             './csv_files/bracket_results/2016_bracket_results.csv']

client = MongoClient('localhost:27017')
db = client.march_madness

for file in csv_files:
     with open(file) as csvfile:
        reader = csv.DictReader(csvfile)
        for document in reader:
            # Does this document already exist?
            if db.tournament_stats.find_one({"Year": file[28:32], "Team1": document["Team 1"]}) is None:
                db.tournament_stats.insert(document)